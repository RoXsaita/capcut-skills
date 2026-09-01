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

So this checks four things:

  frontmatter   every SKILL.md has a usable name/description, and the name matches its
                directory, because that is how an agent loads it
  files         every file a skill's own "Files" table lists exists
  links         every relative markdown link resolves
  cli parity    every `capcutctl` command and flag written in a code block or code span
                exists in the CLI's published contract, and the contract we hold is the
                version we say we are compatible with

Run:  python3 scripts/validate.py         (exit 1 on any finding)
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ["capcut-cli", "capcut-editing", "capcut-editing-talking-head",
          "capcut-editing-screen-recording"]
CONTRACT = ROOT / ".capcut" / "cli-contract.json"
COMPAT = ROOT / ".capcut" / "cli-compatibility.json"

findings: list[str] = []


def fail(where: str, message: str) -> None:
    findings.append(f"{where}: {message}")


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
    for number, line in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
        if line.lstrip().startswith("```"):
            fence = not fence
            continue
        # Strip trailing comments. Both shell and Python blocks annotate their commands
        # (`capcutctl preflight  # will this machine work?`), and the prose after the hash
        # is exactly the place a sentence like "in the capcutctl repo" turns up. Anchored
        # on space-hash so a URL fragment survives.
        code = re.split(r"\s#", line, maxsplit=1)[0]
        if fence:
            yield number, code
        else:
            for span in re.findall(r"`([^`\n]+)`", code):
                yield number, span


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
    synced = (compat.get("contractSyncedFrom") or {}).get("cliVersion")
    if synced and synced != contract.get("cliVersion"):
        fail(".capcut/cli-compatibility.json",
             f"contractSyncedFrom.cliVersion {synced!r} but the vendored contract says "
             f"{contract.get('cliVersion')!r} — refresh both together")

    commands = contract["commands"]
    for path in markdown_files():
        for number, region in scan_regions(path):
            scan_invocations(region, commands, f"{path.relative_to(ROOT)}:{number}")


def scan_invocations(region: str, commands: dict, where: str) -> None:
    for match in re.finditer(r"\bcapcutctl\s+([a-z][a-z0-9-]*)([^\n|]*)", region):
        name, rest = match.group(1), match.group(2)
        entry = commands.get(name)
        if entry is None:
            fail(where, f"`capcutctl {name}` is not a command in the CLI contract")
            continue
        allowed = set(entry["options"])
        subcommands = set(entry.get("subcommands", []))
        # A placeholder (`capcutctl layout …`, `capcutctl trim PROJECT`) is not a claim
        # about a subcommand. Only a real lowercase token is.
        first = rest.strip().split(" ")[0] if rest.strip() else ""
        looks_like_subcommand = bool(re.fullmatch(r"[a-z][a-z0-9-]*", first))
        if subcommands and looks_like_subcommand and first not in subcommands:
            fail(where, f"`capcutctl {name} {first}` is not a subcommand of {name} "
                        f"({', '.join(sorted(subcommands))})")
        for flag in re.findall(r"--[a-z][a-z0-9-]*", rest):
            if flag not in allowed:
                fail(where, f"`capcutctl {name}` has no {flag} in the CLI contract")


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


def main() -> int:
    check_frontmatter()
    check_referenced_files()
    check_links()
    check_cli_parity()
    check_dry_run_claim()
    if findings:
        print(f"{len(findings)} finding(s):\n", file=sys.stderr)
        for finding in sorted(set(findings)):
            print(f"  {finding}", file=sys.stderr)
        return 1
    print("skills validate: frontmatter, referenced files, links and CLI parity all pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
