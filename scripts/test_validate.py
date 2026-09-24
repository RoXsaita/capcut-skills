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
