#!/usr/bin/env python3
"""Validate the skills against themselves and against the CLI they document.

CI used to check that four SKILL.md files and two licence files existed. That caught a
deleted skill and nothing else. Everything that actually went wrong was invisible to it:
the `capcutctl` surface moved (`status`, `--wait-for-close`, `init-spec`, `layout screen`,
the media-origin flags) while the command table did not, and `capcut-cli/SKILL.md`
promised that "everything that writes takes --dry-run" when four writing commands do not.

A skill that names a flag the CLI does not have sends an agent into a parse error. One
that misses a command means the agent hand-writes draft_info.json instead — the single
thing every one of these documents exists to prevent.

So this checks:

  frontmatter   every SKILL.md has a usable name/description, and the name matches its
                directory, because that is how an agent loads it
  files         every file a skill's own "Files" table lists exists
  links         every relative markdown link resolves
  cli parity    every `capcutctl` command and flag written in a code block or code span
                (including inside $( ) and backticks), in the kit's shell scripts and in
                its 'capcutctl …' string literals exists in the CLI's published contract,
                and the contract we hold is the version we say we are compatible with
  coverage      every command in the contract is named as `capcutctl <cmd>` somewhere in
                a SKILL.md or references/*.md, or is on UNMENTIONED_OK with the reason
  live cli      with a CLI clone at $CAPCUTCTL_CLI or ../cli, its `contract` and
                `contract --markdown` match what we vendor (warns; fails with --strict
                or CAPCUT_STRICT_DRIFT=1). Without one this says "live CLI not checked"
  hygiene       no retired skill name, every reference opens with an H1, and no
                personal home path, hard-coded hex colour, or token listed in
                $CAPCUT_PERSONAL_TOKENS (comma-separated, kept out of git) in a skill
  reference     capcut-cli/reference.md was generated from the vendored contract: same CLI
                and contract version, and every command's summary and example present
  budget        the happy path stays under HAPPY_PATH_BUDGET lines
  profile       no skill restates a rule the style profile has since replaced

Run:  python3 scripts/validate.py [--strict]   (exit 1 on any finding)
"""
from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ["capcut-cli", "capcut-editing", "capcut-motion"]
REFERENCE = ROOT / "capcut-cli" / "reference.md"
# What an agent reads on the happy path. Every line here is context spent before the first
# edit; the old four-skill set was ~4,600 lines and 37 commits stale.
HAPPY_PATH = ["capcut-editing/SKILL.md", "capcut-cli/SKILL.md",
              "capcut-editing/references/edit-plan.md", "capcut-editing/references/grammar.md"]
HAPPY_PATH_BUDGET = 1200
# Rules that used to live in prose and now contradict the style profile the CLI enforces.
CONTRADICTIONS = [
    (r"hard cuts only", "the profile decides seams (seams.hardCutsByDefault); `build` applies motivated seams"),
    (r"no transition effects,? ever", "the profile decides seams; motivated seams are the house default"),
    (r"captions happen outside capcut", "the profile decides captions (captions.mode: keywords)"),
    (r"no captions(/subtitles)? anywhere", "keyword supers are part of the profile's grammar"),
    (r"preferred: remotion", "footage stays CapCut-native; rendered media is mograph graphics only"),
    (r"`cta-card`\s*\+\s*endcard", "the house CTA is full face + the endcard keyword; cta-card is opt-in only"),
    (r"full captions are not the house style|keyword supers, not captions",
     "word captions are required (one style); keyword supers are emphasis on top"),
    (r"remotion[^|\n]*normal case|normal case[^|\n]*remotion|remotion for the rest",
     "drawn B-roll is native mograph first; Remotion is a last resort"),
]
CONTRACT = ROOT / ".capcut" / "cli-contract.json"
COMPAT = ROOT / ".capcut" / "cli-compatibility.json"
# Contract commands no skill has to name, and why. Everything else must appear as
# `capcutctl <cmd>` in a SKILL.md or references/*.md, so a sync that brings in a command
# cannot pass while the skills never mention it.
UNMENTIONED_OK = {
    "oracle": "dev-only round-trip capture/diff of a disposable project, never a real edit",
    "version": "prints the installed version; `preflight` and `contract` already carry it",
}
# The skills before the 2026-09 merge. An agent told to load one finds nothing.
RETIRED_SKILLS = ["capcut-editing-talking-head", "capcut-editing-screen-recording"]
RETIRED_EXEMPT = {"CONTRIBUTING.md"}  # explains the merge, so it names them on purpose
# The brand comes from the creator's profile, never from a skill. Neutral placeholders a skill
# may still write: the CLI's shipped default profile colours, black and white.
HEX = re.compile(r"(?<![\w&/])#[0-9A-Fa-f]{6}(?![\w-])")
NEUTRAL_HEX = {"#3D3D3D", "#FFB020", "#0B0B14", "#FFFFFF", "#000000"}
# A creator's own handles and brand words never live in this public repo, not even in the
# guard: list them, comma-separated, in $CAPCUT_PERSONAL_TOKENS (shell profile, never git).
PERSONAL_TOKENS_ENV = "CAPCUT_PERSONAL_TOKENS"
PERSONAL = [
    (re.compile(r"/Users/[^/\s`]+"), "a personal home path"),
    *[(re.compile(re.escape(token.strip()), re.I), "a personal token")
      for token in os.environ.get(PERSONAL_TOKENS_ENV, "").split(",") if token.strip()],
]
STRICT_DRIFT_ENV = "CAPCUT_STRICT_DRIFT"
SYNC_SCRIPT = ROOT / "scripts" / "sync-cli.sh"

findings: list[str] = []
# Live-CLI drift: printed as warnings, promoted to findings by --strict.
drift: list[str] = []
live_status = "live CLI not checked"


def fail(where: str, message: str) -> None:
    findings.append(f"{where}: {message}")


def skill_docs() -> list[Path]:
    """What an agent reads as a skill: each SKILL.md and its references/ (not reference.md)."""
    return sorted([*ROOT.glob("*/SKILL.md"), *ROOT.glob("*/references/*.md")])


def markdown_files() -> list[Path]:
    return sorted(p for p in ROOT.rglob("*.md") if ".git" not in p.parts)


# --------------------------------------------------------------------------- frontmatter

# Deliberately not a YAML dependency: the frontmatter here is two keys, and a validator
# that needs `pip install` before it can run is a validator nobody runs.
def read_frontmatter(path: Path) -> dict[str, str] | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None
    block, fields, key = text[4:end], {}, None
    for line in block.split("\n"):
        match = re.match(r"^([a-z][a-z0-9_-]*):\s*(.*)$", line)
        if match:
            key = match.group(1)
            fields[key] = match.group(2).strip()
        elif key and line.strip():
            # A folded scalar (`description: >`) continues on indented lines.
            fields[key] = (fields[key] + " " + line.strip()).strip()
    return fields


def check_frontmatter() -> None:
    for skill in SKILLS:
        path = ROOT / skill / "SKILL.md"
        where = f"{skill}/SKILL.md"
        if not path.exists():
            fail(where, "missing")
            continue
        fields = read_frontmatter(path)
        if fields is None:
            fail(where, "no --- frontmatter block")
            continue
        name = fields.get("name", "")
        if name != skill:
            fail(where, f"frontmatter name is {name!r}, but the directory is {skill!r} — "
                        "an agent loads the skill by directory, so these must match")
        description = fields.get("description", "").strip().lstrip(">").strip()
        if len(description) < 40:
            fail(where, "description is missing or too short to route on")
        if len(description) > 1600:
            fail(where, f"description is {len(description)} chars; keep the hub routable")


# -------------------------------------------------------------------------------- files

def check_referenced_files() -> None:
    """Every file a skill's own Files table lists must exist in that skill."""
    for skill in SKILLS:
        path = ROOT / skill / "SKILL.md"
        if not path.exists():
            continue
        lines = path.read_text(encoding="utf-8").split("\n")
        inside = False
        for number, line in enumerate(lines, 1):
            if re.match(r"^##+\s", line):
                # "## Files" in three skills, "## Reference files" in the hub. Match on the
                # word, not one spelling of the heading.
                inside = bool(re.search(r"\bfiles\b", line, re.I))
                continue
            if not inside or not line.startswith("|"):
                continue
            cell = re.match(r"^\|\s*`([^`]+)`\s*\|", line)
            if not cell:
                continue
            target = cell.group(1)
            if not (ROOT / skill / target).exists():
                fail(f"{skill}/SKILL.md:{number}",
                     f"the Files table lists `{target}`, which does not exist")


def check_links() -> None:
    """Relative markdown links must resolve."""
    for path in markdown_files():
        text = path.read_text(encoding="utf-8")
        for number, line in enumerate(text.split("\n"), 1):
            for target in re.findall(r"\]\(([^)]+)\)", line):
                if target.startswith(("http://", "https://", "#", "mailto:")):
                    continue
                resolved = (path.parent / target.split("#", 1)[0]).resolve()
                if not resolved.exists():
                    fail(f"{path.relative_to(ROOT)}:{number}", f"broken link to {target}")


# --------------------------------------------------------------------------- cli parity

def scan_regions(path: Path):
    """Yield (line number, code text) for every fenced block line and inline code span.

    Prose is excluded on purpose. "`presets/layouts.json` in the capcutctl repo" is a
    sentence, not an invocation, and a validator that reads it as `capcutctl repo` cries
    wolf until someone turns it off.
    """
    fence = False
    pending, start = "", 0
    for number, line in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
        line = re.sub(r"^\s*(?:>\s?)+", "", line)
        if line.lstrip().startswith("```"):
            if pending:
                yield start, pending
                pending = ""
            fence = not fence
            continue
        code = line
        if fence:
            if not pending:
                start = number
            pending += code.rstrip().removesuffix("\\") + " "
            if not code.rstrip().endswith("\\"):
                yield start, pending
                pending = ""
        else:
            for span in re.findall(r"`([^`\n]+)`", code):
                yield number, span
    if pending:
        yield start, pending


def check_cli_parity() -> None:
    if not CONTRACT.exists():
        fail(".capcut/cli-contract.json", "missing — copy it from the CLI's docs/")
        return
    if not COMPAT.exists():
        fail(".capcut/cli-compatibility.json", "missing")
        return
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    compat = json.loads(COMPAT.read_text(encoding="utf-8"))

    # The contract we hold must be the one we claim to be written against.
    if contract.get("contractVersion") != compat.get("requiredContractVersion"):
        fail(".capcut/cli-compatibility.json",
             f"requiredContractVersion {compat.get('requiredContractVersion')} but the "
             f"vendored contract is version {contract.get('contractVersion')}")
    synced_commit = str((compat.get("contractSyncedFrom") or {}).get("commit") or "")
    if synced_commit.endswith("-dirty"):
        fail(".capcut/cli-compatibility.json",
             f"contractSyncedFrom.commit {synced_commit!r} was synced from uncommitted CLI "
             "changes — commit them in the CLI and run scripts/sync-cli.sh from a clean tree")
    synced = (compat.get("contractSyncedFrom") or {}).get("cliVersion")
    if synced and synced != contract.get("cliVersion"):
        fail(".capcut/cli-compatibility.json",
             f"contractSyncedFrom.cliVersion {synced!r} but the vendored contract says "
             f"{contract.get('cliVersion')!r} — refresh both together")

    commands = contract["commands"]
    for path in markdown_files():
        for number, region in scan_regions(path):
            scan_invocations(region, commands, f"{path.relative_to(ROOT)}:{number}")
    # The kit's shell scripts print and run capcutctl lines an agent copies verbatim.
    for path in sorted(ROOT.rglob("*.sh")):
        if ".git" in path.parts or path == SYNC_SCRIPT:
            continue
        for number, line in shell_lines(path):
            scan_invocations(line, commands, f"{path.relative_to(ROOT)}:{number}")
    # And the kit's TypeScript draws command lines on screen ('capcutctl cut …').
    for path in sorted([*ROOT.glob("capcut-motion/kit/**/*.ts"), *ROOT.glob("capcut-motion/kit/**/*.tsx")]):
        for number, line in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
            for _, literal in re.findall(r"""(['"`])(capcutctl\s[^'"`\n]*)\1""", line):
                scan_invocations(literal, commands, f"{path.relative_to(ROOT)}:{number}")


def shell_lines(path: Path):
    """Yield (line number, logical line) for a shell script: comments out, `\\` joined."""
    pending, start = "", 0
    for number, line in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
        if not pending:
            start = number
            if line.lstrip().startswith("#"):
                continue
        pending += line.rstrip().removesuffix("\\") + " "
        if not line.rstrip().endswith("\\"):
            yield start, pending
            pending = ""
    if pending:
        yield start, pending


def _closing_paren(text: str, index: int) -> int | None:
    """Index of the `)` closing a `$(` whose body starts at `index`, honouring quotes."""
    depth, quote = 1, None
    while index < len(text):
        char = text[index]
        if quote == "'":
            quote = None if char == "'" else quote
        elif char == "\\":
            index += 1
        elif char == '"':
            quote = None if quote == '"' else '"'
        elif char == "'" and quote is None:
            quote = "'"
        elif char == "(" and quote is None:
            depth += 1
        elif char == ")" and quote is None:
            depth -= 1
            if depth == 0:
                return index
        index += 1
    return None


def split_substitutions(region: str) -> tuple[str, list[str]]:
    """Lift each `$( … )` and backtick body out of `region`.

    shlex reads `x=$(capcutctl bogus)` as the words `x=$(capcutctl` and `bogus)`, and a quoted
    "$(capcutctl …)" as one word, so neither was ever checked. Each body comes back to be
    scanned on its own, and the region keeps a placeholder word in its place. A `)` inside a
    quoted argument (JSON, a `node -pe` one-liner) does not end the substitution.
    """
    out, bodies, index, quote = [], [], 0, None
    while index < len(region):
        char = region[index]
        if quote == "'":
            quote = None if char == "'" else quote
            out.append(char)
            index += 1
            continue
        if region.startswith("$(", index) and not region.startswith("$((", index):
            end = _closing_paren(region, index + 2)
            if end is None:
                return region, bodies
            bodies.append(region[index + 2:end])
            out.append("_subst_")
            index = end + 1
            continue
        tick = 2 if region.startswith("\\`", index) else 1 if char == "`" else 0
        if tick:
            end = region.find("`", index + tick)
            if end == -1:
                return region, bodies
            bodies.append(region[index + tick:end].removesuffix("\\"))
            out.append("_subst_")
            index = end + 1
            continue
        if char == "\\":
            out.append(region[index:index + 2])
            index += 2
            continue
        if char == '"':
            quote = None if quote == '"' else '"'
        elif char == "'" and quote is None:
            quote = "'"
        out.append(char)
        index += 1
    return "".join(out), bodies


def scan_invocations(region: str, commands: dict, where: str) -> None:
    if not re.search(r"\bcapcutctl\s+[a-z]", region):
        return
    region, bodies = split_substitutions(region)
    for body in bodies:
        scan_invocations(body, commands, where)
    if not re.search(r"\bcapcutctl\s+[a-z]", region):
        return
    lexer = shlex.shlex(region, posix=True, punctuation_chars="|;&")
    lexer.whitespace_split = True
    try:
        tokens = list(lexer)
    except ValueError as error:
        fail(where, f"invalid quoted CLI example: {error}")
        return
    for index, token in enumerate(tokens[:-1]):
        if token != "capcutctl" or not re.fullmatch(r"[a-z][a-z0-9-]*", tokens[index + 1]):
            continue
        name = tokens[index + 1]
        rest = []
        for value in tokens[index + 2:]:
            if value == "capcutctl" or set(value) <= set("|;&"):
                break
            rest.append(value)
        entry = commands.get(name)
        if entry is None:
            fail(where, f"`capcutctl {name}` is not a command in the CLI contract")
            continue
        allowed = set(entry["options"])
        subcommands = set(entry.get("subcommands", []))
        # A placeholder (`capcutctl layout …`, `capcutctl trim PROJECT`) is not a claim
        # about a subcommand. Only a real lowercase token is.
        first = rest[0] if rest else ""
        looks_like_subcommand = bool(re.fullmatch(r"[a-z][a-z0-9-]*", first))
        if subcommands and looks_like_subcommand and first not in subcommands:
            fail(where, f"`capcutctl {name} {first}` is not a subcommand of {name} "
                        f"({', '.join(sorted(subcommands))})")
        for flag in re.findall(r"--[a-z][a-z0-9-]*", " ".join(rest)):
            if flag not in allowed:
                fail(where, f"`capcutctl {name}` has no {flag} in the CLI contract")


def check_commands_mentioned() -> None:
    """A command no skill names is a command an agent never reaches for."""
    if not CONTRACT.exists():
        return
    commands = json.loads(CONTRACT.read_text(encoding="utf-8")).get("commands", {})
    corpus = "\n".join(path.read_text(encoding="utf-8") for path in skill_docs())
    for name in sorted(commands):
        if name in UNMENTIONED_OK:
            continue
        if not re.search(rf"\bcapcutctl\s+{re.escape(name)}(?![\w-])", corpus):
            fail(".capcut/cli-contract.json",
                 f"`capcutctl {name}` is in the CLI contract but no SKILL.md or references/*.md "
                 "names it — document it, or add it to UNMENTIONED_OK in scripts/validate.py "
                 "with the reason")
    for name in sorted(set(UNMENTIONED_OK) - set(commands)):
        fail("scripts/validate.py", f"UNMENTIONED_OK lists `{name}`, which the contract no longer has")


def check_hygiene() -> None:
    """Retired skill names, reference headings, and the creator's brand leaking into a skill."""
    for path in markdown_files():
        relative = path.relative_to(ROOT)
        if str(relative) in RETIRED_EXEMPT:
            continue
        for number, line in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
            for retired in RETIRED_SKILLS:
                if re.search(rf"(?<![\w-]){re.escape(retired)}(?![\w-])", line):
                    fail(f"{relative}:{number}", f"names the retired skill {retired!r}; the "
                                                 "skills are capcut-cli, capcut-editing and capcut-motion")
    for path in sorted(ROOT.glob("*/references/*.md")):
        first = next((line for line in path.read_text(encoding="utf-8").split("\n") if line.strip()), "")
        if not first.startswith("# "):
            fail(str(path.relative_to(ROOT)), "the first line is not a `# ` heading; an agent "
                                              "opening a reference reads its title first")
    for path in skill_docs():
        relative = path.relative_to(ROOT)
        for number, line in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
            for colour in HEX.findall(line):
                if colour.upper() not in NEUTRAL_HEX:
                    fail(f"{relative}:{number}", f"hard-codes the colour {colour}; colours come "
                                                 "from the profile (`capcutctl profile`, tokens.color)")
            for pattern, what in PERSONAL:
                if pattern.search(line):
                    fail(f"{relative}:{number}", f"contains {what}; the skills are public and "
                                                 "creator-neutral, the brand lives in the profile")


# ------------------------------------------------------------------------------ live cli

def find_live_cli() -> tuple[Path | None, str]:
    """The CLI entry to compare against, and how to name it: $CAPCUTCTL_CLI, else ../cli."""
    configured = os.environ.get("CAPCUTCTL_CLI", "").strip()
    if configured:
        path = Path(configured).expanduser()
        entry = path if path.is_file() else path / "bin" / "capcutctl.mjs"
        return (entry if entry.is_file() else None), "$CAPCUTCTL_CLI"
    entry = ROOT.parent / "cli" / "bin" / "capcutctl.mjs"
    return (entry if entry.is_file() else None), "../cli"


def contract_drift(vendored: dict, live: dict) -> list[str]:
    """What changed between the vendored contract and the live one, command by command."""
    changes = [f"{key} {vendored.get(key)!r} vendored, {live.get(key)!r} live"
               for key in ("contractVersion", "cliVersion") if vendored.get(key) != live.get(key)]
    for key in sorted((set(vendored) | set(live)) - {"contractVersion", "cliVersion", "commands"}):
        if vendored.get(key) != live.get(key):
            changes.append(f"the contract's {key} section changed")
    old, new = vendored.get("commands", {}), live.get("commands", {})
    if sorted(set(new) - set(old)):
        changes.append("commands added: " + ", ".join(sorted(set(new) - set(old))))
    if sorted(set(old) - set(new)):
        changes.append("commands removed: " + ", ".join(sorted(set(old) - set(new))))
    for name in sorted(set(old) & set(new)):
        before, after = old[name], new[name]
        for field in ("options", "subcommands"):
            gained = sorted(set(after.get(field) or []) - set(before.get(field) or []))
            lost = sorted(set(before.get(field) or []) - set(after.get(field) or []))
            if gained:
                changes.append(f"`{name}` {field} added: {', '.join(gained)}")
            if lost:
                changes.append(f"`{name}` {field} removed: {', '.join(lost)}")
        for field in ("summary", "example"):
            if before.get(field) != after.get(field):
                changes.append(f"`{name}` {field} changed: {after.get(field)!r}")
        rest = sorted(key for key in set(before) | set(after)
                      if key not in ("options", "subcommands", "summary", "example")
                      and before.get(key) != after.get(key))
        if rest:
            changes.append(f"`{name}` {', '.join(rest)} changed")
    return changes


def check_cli_live() -> None:
    """Compare the vendored contract and reference with a live CLI, when one is at hand.

    CI has only the vendored copy, and a copy can only agree with itself. The CLI drift
    workflow diffs against CLI main on a schedule; this does the same locally, by name.
    """
    global live_status
    entry, label = find_live_cli()
    if entry is None:
        if label == "$CAPCUTCTL_CLI":
            drift.append("live CLI: $CAPCUTCTL_CLI has no bin/capcutctl.mjs")
        live_status = "live CLI not checked (set CAPCUTCTL_CLI to a capcut-editor-cli clone)"
        return
    if not shutil.which("node") or not CONTRACT.exists():
        live_status = f"live CLI not checked ({label}: node not found)"
        return
    outputs = []
    with tempfile.TemporaryDirectory(prefix="skills-validate-home-") as home:
        # A temp HOME: the contract must not depend on whoever runs this, or their profile.
        env = {**os.environ, "HOME": home}
        for args in (["contract"], ["contract", "--markdown"]):
            try:
                done = subprocess.run(["node", str(entry), *args], env=env, capture_output=True,
                                      text=True, timeout=120)
            except (OSError, subprocess.TimeoutExpired) as error:
                drift.append(f"live CLI ({label}): `capcutctl {' '.join(args)}` did not run: {error}")
                live_status = f"live CLI ({label}) did not run"
                return
            if done.returncode != 0:
                first = (done.stderr.strip().split("\n") or [""])[0]
                drift.append(f"live CLI ({label}): `capcutctl {' '.join(args)}` exited "
                             f"{done.returncode}: {first}")
                live_status = f"live CLI ({label}) failed"
                return
            outputs.append(done.stdout)
    try:
        live = json.loads(outputs[0])
    except ValueError as error:
        drift.append(f"live CLI ({label}): `capcutctl contract` is not JSON: {error}")
        live_status = f"live CLI ({label}) failed"
        return
    changes = contract_drift(json.loads(CONTRACT.read_text(encoding="utf-8")), live)
    for change in changes:
        drift.append(f"live CLI ({label}) vs .capcut/cli-contract.json: {change}")
    if REFERENCE.exists() and REFERENCE.read_text(encoding="utf-8") != outputs[1]:
        lines = sum(1 for line in difflib.unified_diff(
            REFERENCE.read_text(encoding="utf-8").split("\n"), outputs[1].split("\n"), n=0)
            if line[:1] in "+-" and not line.startswith(("+++", "---")))
        drift.append(f"live CLI ({label}) vs capcut-cli/reference.md: `contract --markdown` "
                     f"differs on {lines} line(s)")
    live_status = (f"live CLI ({label}) drifted; refresh with scripts/sync-cli.sh" if drift
                   else f"live CLI ({label}) matches")


def check_dry_run_claim() -> None:
    """The claim that broke: "Everything that writes takes --dry-run" was false."""
    contract = json.loads(CONTRACT.read_text(encoding="utf-8")) if CONTRACT.exists() else {}
    guarantee = (contract.get("dryRun") or {}).get("guarantee")
    for path in markdown_files():
        text = path.read_text(encoding="utf-8")
        for number, line in enumerate(text.split("\n"), 1):
            if re.search(r"every(thing)?\b[^.]*\bwrites\b[^.]*--dry-run", line, re.I):
                fail(f"{path.relative_to(ROOT)}:{number}",
                     "this repeats the false guarantee that everything which writes takes "
                     f"--dry-run. The CLI's actual claim is: {guarantee!r}")


def check_reference() -> None:
    """The command reference is generated; prove it came from the contract we vendor."""
    if not REFERENCE.exists():
        fail("capcut-cli/reference.md", "missing — `capcutctl contract --markdown > capcut-cli/reference.md`")
        return
    if not CONTRACT.exists():
        return
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    text = REFERENCE.read_text(encoding="utf-8")
    header = re.search(r"from CLI (\S+), contract v(\d+)", text)
    if not header or header.group(1) != contract.get("cliVersion") \
            or int(header.group(2)) != contract.get("contractVersion"):
        fail("capcut-cli/reference.md", "was not generated from the vendored contract — regenerate "
                                        "both together with scripts/sync-cli.sh")
    for name, entry in contract.get("commands", {}).items():
        summary, example = entry.get("summary"), entry.get("example")
        if summary and summary not in text:
            fail("capcut-cli/reference.md", f"stale: the summary of `{name}` differs from the contract")
        if example and example.replace("|", "\\|") not in text:
            fail("capcut-cli/reference.md", f"stale: the example for `{name}` differs from the contract")


def check_budget() -> None:
    total = 0
    for relative in HAPPY_PATH:
        path = ROOT / relative
        if path.exists():
            total += len(path.read_text(encoding="utf-8").split("\n"))
    if total > HAPPY_PATH_BUDGET:
        fail("happy path", f"{total} lines across {', '.join(HAPPY_PATH)}; the budget is "
                           f"{HAPPY_PATH_BUDGET}. Move detail into a reference an agent opens on demand.")


def check_profile_contradictions() -> None:
    for path in markdown_files():
        if "docs" in path.relative_to(ROOT).parts:
            continue
        for number, line in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
            for pattern, why in CONTRADICTIONS:
                if re.search(pattern, line, re.I):
                    fail(f"{path.relative_to(ROOT)}:{number}", f"contradicts the style profile: {why}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the skills against themselves and the CLI.")
    parser.add_argument("--strict", action="store_true",
                        help=f"fail on live-CLI drift (also {STRICT_DRIFT_ENV}=1); it warns by default")
    strict = parser.parse_args(argv).strict or os.environ.get(STRICT_DRIFT_ENV) == "1"
    check_reference()
    check_budget()
    check_profile_contradictions()
    check_frontmatter()
    check_referenced_files()
    check_links()
    check_cli_parity()
    check_commands_mentioned()
    check_hygiene()
    check_dry_run_claim()
    check_cli_live()
    if strict:
        findings.extend(drift)
    elif drift:
        print(f"{len(drift)} CLI drift warning(s) (--strict or {STRICT_DRIFT_ENV}=1 fails on them):\n",
              file=sys.stderr)
        for warning in drift:
            print(f"  {warning}", file=sys.stderr)
        print(file=sys.stderr)
    if findings:
        print(f"{len(findings)} finding(s):\n", file=sys.stderr)
        for finding in sorted(set(findings)):
            print(f"  {finding}", file=sys.stderr)
        return 1
    print("skills validate: frontmatter, files, links, parity with the vendored CLI contract, command "
          "coverage, generated reference, hygiene, budget and profile all pass; " + live_status)
    return 0


if __name__ == "__main__":
    sys.exit(main())
