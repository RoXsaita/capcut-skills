#!/usr/bin/env python3
"""Negative tests for scripts/validate.py.

A validator nobody has watched fail is a validator that passes because it checks nothing.
Each case here reintroduces one of the defects the real repository had, in a throwaway
copy, and asserts the checker reports it.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CASES: list[tuple[str, str]] = []


def case(name: str):
    def register(fn):
        CASES.append((name, fn))
        return fn
    return register


def sandbox() -> Path:
    """A copy of the repository, minus git, that a case can vandalise."""
    temp = Path(tempfile.mkdtemp(prefix="skills-validate-"))
    shutil.copytree(ROOT, temp / "repo",
                    ignore=shutil.ignore_patterns(".git", "__pycache__"))
    return temp / "repo"


def run(repo: Path) -> tuple[int, str]:
    done = subprocess.run([sys.executable, "scripts/validate.py"], cwd=repo,
                          capture_output=True, text=True, timeout=120)
    return done.returncode, done.stdout + done.stderr


def edit(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    assert old in text, f"fixture drifted: {old!r} not in {path}"
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


@case("a command the CLI does not have")
def _(repo: Path) -> str:
    edit(repo / "capcut-cli" / "SKILL.md",
         "capcutctl profile       #", "capcutctl summarise     #")
    return "not a command in the CLI contract"


@case("a flag the CLI does not have")
def _(repo: Path) -> str:
    edit(repo / "capcut-editing" / "SKILL.md",
         "capcutctl doctor --project NAME\n", "capcutctl doctor --project NAME --repair\n")
    return "has no --repair in the CLI contract"


@case("a layout subcommand that does not exist")
def _(repo: Path) -> str:
    edit(repo / "capcut-editing" / "references" / "edit-plan.md",
         "`capcutctl mograph list`", "`capcutctl layout mosaic`")
    return "is not a subcommand of layout"


@case("an invalid flag on a continued command")
def _(repo: Path) -> str:
    path = repo / "README.md"
    with path.open("a", encoding="utf-8") as handle:
        handle.write("\n```bash\ncapcutctl doctor --project NAME \\\n  --repair\n```\n")
    return "has no --repair in the CLI contract"


@case("an invalid command after a shell separator")
def _(repo: Path) -> str:
    path = repo / "README.md"
    with path.open("a", encoding="utf-8") as handle:
        handle.write("\n```bash\ncapcutctl projects && capcutctl summarise\n```\n")
    return "not a command in the CLI contract"


@case("an invalid command in a blockquoted code fence")
def _(repo: Path) -> str:
    path = repo / "README.md"
    with path.open("a", encoding="utf-8") as handle:
        handle.write("\n> ```bash\n> capcutctl summarise\n> ```\n")
    return "not a command in the CLI contract"


@case("an invalid flag after a quoted shell separator")
def _(repo: Path) -> str:
    path = repo / "README.md"
    with path.open("a", encoding="utf-8") as handle:
        handle.write("\n```bash\ncapcutctl doctor --project 'A&B; C # D' --repair\n```\n")
    return "has no --repair in the CLI contract"


@case("the false dry-run guarantee, reintroduced")
def _(repo: Path) -> str:
    edit(repo / "capcut-cli" / "SKILL.md",
         "**`--dry-run` is a guarantee about transactional commands only:**",
         "Everything that writes takes `--dry-run`.\n\n**Also**")
    return "repeats the false guarantee"


@case("frontmatter name that does not match the directory")
def _(repo: Path) -> str:
    edit(repo / "capcut-cli" / "SKILL.md", "name: capcut-cli", "name: capcut-cli-tool")
    return "but the directory is"


@case("a Files table entry pointing at a file that is gone")
def _(repo: Path) -> str:
    (repo / "capcut-editing" / "references" / "pitfalls.md").unlink()
    return "which does not exist"


@case("a broken relative link")
def _(repo: Path) -> str:
    edit(repo / "README.md", "](CONTRIBUTING.md)", "](CONTRIBUTING-GUIDE.md)")
    return "broken link to"


@case("a vendored contract from a different CLI version")
def _(repo: Path) -> str:
    edit(repo / ".capcut" / "cli-compatibility.json",
         '"cliVersion": "0.1.1"', '"cliVersion": "0.9.9"')
    return "refresh both together"


@case("a contract synced from a dirty CLI tree")
def _(repo: Path) -> str:
    path = repo / ".capcut" / "cli-compatibility.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["contractSyncedFrom"]["commit"] = "abc1234-dirty"
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return "synced from uncommitted CLI changes"


@case("a vendored contract of the wrong shape")
def _(repo: Path) -> str:
    edit(repo / ".capcut" / "cli-compatibility.json",
         '"requiredContractVersion": 2', '"requiredContractVersion": 1')
    return "requiredContractVersion 1"


@case("a hand-edited or stale generated reference")
def _(repo: Path) -> str:
    edit(repo / "capcut-cli" / "reference.md", "Blocking ready-to-post check", "Optional check")
    return "stale: the summary of `gate`"


@case("a reference generated from another CLI version")
def _(repo: Path) -> str:
    edit(repo / "capcut-cli" / "reference.md", "from CLI 0.1.1", "from CLI 0.0.9")
    return "was not generated from the vendored contract"


@case("the happy path growing past its budget")
def _(repo: Path) -> str:
    path = repo / "capcut-editing" / "references" / "grammar.md"
    path.write_text(path.read_text(encoding="utf-8") + "\nfiller\n" * 900, encoding="utf-8")
    return "the budget is"


@case("a retired rule that contradicts the style profile")
def _(repo: Path) -> str:
    path = repo / "capcut-editing" / "references" / "pitfalls.md"
    with path.open("a", encoding="utf-8") as handle:
        handle.write("\n- Hard cuts only. No captions anywhere.\n")
    return "contradicts the style profile"


@case("a cta-card over the face as the default CTA, or supers instead of captions")
def _(repo: Path) -> str:
    path = repo / "capcut-editing" / "references" / "grammar.md"
    with path.open("a", encoding="utf-8") as handle:
        handle.write("\n| CTA | full face | `cta-card` + endcard | select |\n"
                     "- Full captions are not the house style.\n")
    return "the house CTA is full face"


@case("Remotion as the default for drawn B-roll")
def _(repo: Path) -> str:
    path = repo / "capcut-motion" / "references" / "remotion.md"
    with path.open("a", encoding="utf-8") as handle:
        handle.write("\n3. **Remotion for the rest**: collages, a process climbing.\n")
    return "Remotion is a last resort"


# ------------------------------------------------------------------ scripts/sync-cli.sh

SYNC_CASES: list[tuple[str, object]] = []


def sync_case(name: str):
    def register(fn):
        SYNC_CASES.append((name, fn))
        return fn
    return register


def git(cli: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(cli), "-c", "user.name=test", "-c", "user.email=test@example.invalid",
                    *args], check=True, capture_output=True, text=True)


def stub_cli(repo: Path) -> Path:
    """A throwaway CLI clone whose `contract` prints exactly what the skills vendor."""
    cli = repo.parent / "cli"
    (cli / "bin").mkdir(parents=True)
    (cli / "src").mkdir()
    (cli / "docs").mkdir()
    contract = (repo / ".capcut" / "cli-contract.json").read_text(encoding="utf-8")
    shutil.copy(repo / ".capcut" / "cli-contract.json", cli / "bin" / "contract.json")
    shutil.copy(repo / "capcut-cli" / "reference.md", cli / "bin" / "reference.md")
    (cli / "docs" / "cli-contract.json").write_text(contract, encoding="utf-8")
    (cli / "bin" / "capcutctl.mjs").write_text(
        "import fs from 'node:fs';\n"
        "const file = process.argv.includes('--markdown') ? 'reference.md' : 'contract.json';\n"
        "process.stdout.write(fs.readFileSync(new URL(`./${file}`, import.meta.url)));\n",
        encoding="utf-8")
    (cli / "src" / "cli.mjs").write_text("export {};\n", encoding="utf-8")
    version = json.loads(contract)["cliVersion"]
    (cli / "package.json").write_text(json.dumps({"version": version}) + "\n", encoding="utf-8")
    subprocess.run(["git", "init", "-q", "-b", "main", str(cli)], check=True)
    git(cli, "add", "-A")
    git(cli, "commit", "-q", "-m", "stub")
    return cli


def run_sync(repo: Path, *args: str) -> tuple[int, str]:
    done = subprocess.run(["bash", "scripts/sync-cli.sh", *args], cwd=repo,
                          capture_output=True, text=True, timeout=120)
    return done.returncode, done.stdout + done.stderr


@sync_case("a clean CLI tree syncs")
def _(repo: Path, cli: Path):
    return run_sync(repo, str(cli)), None


@sync_case("an uncommitted src/ edit is refused")
def _(repo: Path, cli: Path):
    (cli / "src" / "cli.mjs").write_text("export const changed = 1;\n", encoding="utf-8")
    return run_sync(repo, str(cli)), "uncommitted changes"


@sync_case("--allow-dirty stamps -dirty, which validate rejects")
def _(repo: Path, cli: Path):
    (cli / "src" / "new.mjs").write_text("export {};\n", encoding="utf-8")
    return run_sync(repo, "--allow-dirty", str(cli)), "synced from uncommitted CLI changes"


@sync_case("a detached HEAD is refused")
def _(repo: Path, cli: Path):
    git(cli, "checkout", "-q", "--detach")
    return run_sync(repo, str(cli)), "detached HEAD"


@sync_case("a committed contract that differs from the generated one is refused")
def _(repo: Path, cli: Path):
    (cli / "docs" / "cli-contract.json").write_text("{}\n", encoding="utf-8")
    git(cli, "commit", "-q", "-am", "stale contract")
    return run_sync(repo, str(cli)), "differs from"


def sync_main() -> int:
    if not shutil.which("node") or not shutil.which("git"):
        print("skipped     sync-cli.sh cases (node and git are required)")
        return 0
    failures = 0
    for name, scenario in SYNC_CASES:
        repo = sandbox()
        try:
            (code, output), expected = scenario(repo, stub_cli(repo))
            if expected is None and code != 0:
                print(f"REFUSED     {name}\n{output}", file=sys.stderr)
                failures += 1
            elif expected is not None and code == 0:
                print(f"NOT CAUGHT  {name}", file=sys.stderr)
                failures += 1
            elif expected is not None and expected not in output:
                print(f"WRONG REASON {name}\n  wanted: {expected}\n  got:\n{output}", file=sys.stderr)
                failures += 1
            else:
                print(f"ok          {name}")
        finally:
            shutil.rmtree(repo.parent, ignore_errors=True)
    print(f"\n{len(SYNC_CASES) - failures}/{len(SYNC_CASES)} sync-cli.sh cases pass")
    return failures


# ------------------------------------------------ capcut-motion/kit/scripts/render-alpha.sh

RENDER_ALPHA = ROOT / "capcut-motion" / "kit" / "scripts" / "render-alpha.sh"


def stub_bin(where: Path, marker: Path) -> Path:
    """npx, capcutctl, ffprobe and lockf that only record they ran: nothing real renders."""
    bin_dir = where / "bin"
    bin_dir.mkdir()
    stubs = {
        # npx remotion render ENTRY COMP OUT ...: mark the call and leave a file at OUT.
        "npx": f'echo "npx $*" >> "{marker}"; touch "$5"\n',
        "capcutctl": f'echo "capcutctl $*" >> "{marker}"\n',
        "ffprobe": "exit 0\n",
        "lockf": f'echo "lockf $1 $2" >> "{marker}"; shift 2; exec "$@"\n',
    }
    for name, body in stubs.items():
        path = bin_dir / name
        path.write_text("#!/usr/bin/env bash\n" + body, encoding="utf-8")
        path.chmod(0o755)
    return bin_dir


def render_alpha(out: str, cwd: Path, bin_dir: Path, **env: str) -> tuple[int, str]:
    environ = {**os.environ, "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}", **env}
    done = subprocess.run(["bash", str(RENDER_ALPHA), "src/index.ts", "Shot", out], cwd=cwd,
                          env=environ, capture_output=True, text=True, timeout=60)
    return done.returncode, done.stdout + done.stderr


def kit_main() -> int:
    if not shutil.which("python3"):
        print("skipped     render-alpha.sh cases (python3 is required on PATH)")
        return 0
    failures = 0
    # The durable directory cannot be a mkdtemp() default: that is the system temp root,
    # which the script refuses by design.
    durable = Path(tempfile.mkdtemp(dir=Path.home(), prefix=".skills-kit-"))
    scratch = Path(tempfile.mkdtemp(prefix="skills-kit-"))
    try:
        marker = durable / "marker.log"
        bin_dir = stub_bin(durable, marker)
        refused = ["/private/tmp/x/scratchpad/a.mov", "/private/var/folders/ab/T/a.mov",
                   "scratchpad/a.mov", "/tmp/a.mov", str(scratch / "a.mov")]
        for out in refused:
            marker.unlink(missing_ok=True)
            code, output = render_alpha(out, durable, bin_dir)
            created = (durable / out).parent.exists() if not out.startswith("/") else False
            if code != 2 or marker.exists() or created:
                print(f"NOT REFUSED render-alpha.sh {out} (exit {code})\n{output}", file=sys.stderr)
                failures += 1
            else:
                print(f"refused     render-alpha.sh {out}")
        cases = [("renders/a.mov", {}, "npx remotion render"),
                 ("renders/b.mov", {"CAPCUTCTL_HEAVY_LOCK": str(durable / "heavy.lock")}, "lockf -k")]
        for out, env, expected in cases:
            marker.unlink(missing_ok=True)
            code, output = render_alpha(out, durable, bin_dir, **env)
            log = marker.read_text(encoding="utf-8") if marker.exists() else ""
            if code != 0 or expected not in log or "--layer top" not in output:
                print(f"BLOCKED     render-alpha.sh {out} (exit {code})\n{output}{log}", file=sys.stderr)
                failures += 1
            else:
                print(f"rendered    render-alpha.sh {out}")
    finally:
        shutil.rmtree(durable, ignore_errors=True)
        shutil.rmtree(scratch, ignore_errors=True)
    return failures


def main() -> int:
    # The unmodified repository must pass, or every case below proves nothing.
    code, output = run(ROOT)
    if code != 0:
        print(f"the repository itself does not validate:\n{output}", file=sys.stderr)
        return 1

    failures = sync_main() + kit_main()
    missed = 0
    for name, mutate in CASES:
        repo = sandbox()
        try:
            expected = mutate(repo)
            code, output = run(repo)
            if code == 0:
                print(f"NOT CAUGHT  {name}", file=sys.stderr)
                missed += 1
            elif expected not in output:
                print(f"WRONG REASON {name}\n  wanted: {expected}\n  got:\n{output}",
                      file=sys.stderr)
                missed += 1
            else:
                print(f"caught      {name}")
        finally:
            shutil.rmtree(repo.parent, ignore_errors=True)

    print(f"\n{len(CASES) - missed}/{len(CASES)} regressions caught")
    return 1 if failures + missed else 0


if __name__ == "__main__":
    sys.exit(main())
