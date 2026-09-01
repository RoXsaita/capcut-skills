#!/usr/bin/env python3
"""Negative tests for scripts/validate.py.

A validator nobody has watched fail is a validator that passes because it checks nothing.
Each case here reintroduces one of the defects the real repository had, in a throwaway
copy, and asserts the checker reports it.
"""
from __future__ import annotations

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
         "capcutctl projects  ", "capcutctl summarise  ")
    return "not a command in the CLI contract"


@case("a flag the CLI does not have")
def _(repo: Path) -> str:
    edit(repo / "capcut-cli" / "SKILL.md",
         "capcutctl doctor   --project NAME", "capcutctl doctor   --project NAME --repair")
    return "has no --repair in the CLI contract"


@case("a layout subcommand that does not exist")
def _(repo: Path) -> str:
    edit(repo / "capcut-cli" / "SKILL.md",
         "capcutctl layout list", "capcutctl layout mosaic")
    return "is not a subcommand of layout"


@case("the false dry-run guarantee, reintroduced")
def _(repo: Path) -> str:
    edit(repo / "capcut-cli" / "SKILL.md",
         "**`--dry-run` is a guarantee about transactional edit commands**",
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


@case("a vendored contract of the wrong shape")
def _(repo: Path) -> str:
    edit(repo / ".capcut" / "cli-compatibility.json",
         '"requiredContractVersion": 1', '"requiredContractVersion": 2')
    return "requiredContractVersion 2"


def main() -> int:
    # The unmodified repository must pass, or every case below proves nothing.
    code, output = run(ROOT)
    if code != 0:
        print(f"the repository itself does not validate:\n{output}", file=sys.stderr)
        return 1

    failures = 0
    for name, mutate in CASES:
        repo = sandbox()
        try:
            expected = mutate(repo)
            code, output = run(repo)
            if code == 0:
                print(f"NOT CAUGHT  {name}", file=sys.stderr)
                failures += 1
            elif expected not in output:
                print(f"WRONG REASON {name}\n  wanted: {expected}\n  got:\n{output}",
                      file=sys.stderr)
                failures += 1
            else:
                print(f"caught      {name}")
        finally:
            shutil.rmtree(repo.parent, ignore_errors=True)

    print(f"\n{len(CASES) - failures}/{len(CASES)} regressions caught")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
