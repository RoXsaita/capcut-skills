# capcut-skills

**Unofficial.** Not affiliated with ByteDance or CapCut. MIT licensed — see [LICENSE](LICENSE) and [NOTICE](NOTICE).

Agent skills for editing CapCut projects with `capcutctl`. The hub is `capcut-editing/`; start there.

| Skill | Use it for |
|---|---|
| `capcut-cli` | what `capcutctl` already does — read this before hand-writing JSON |
| `capcut-editing` | format, style, pitfalls, project state |
| `capcut-editing-talking-head` | cutting the face, layouts |
| `capcut-editing-screen-recording` | B-roll, OCR matching, `capcutctl find` |

Install by symlink into the agent's skills dir, e.g. `~/.grok/skills/`, `~/.claude/skills/`, `~/.codex/skills/`.

See [capcut-editor-cli SETUP.md](https://github.com/RoXsaita/capcut-editor-cli/blob/main/SETUP.md).

**Agents: before the first write, ask which style to use** — bundled house style
(Suheil / suheilai), harvest the user's own CapCut drafts, or start blank. See
the CLI README → *Style — ask once*, and `capcut-editing/SKILL.md`.

## Which `capcutctl` these skills describe

`.capcut/cli-compatibility.json` names the CLI version and contract revision these
documents are written against, and `.capcut/cli-contract.json` is a verbatim copy of that
CLI's published command surface (`capcutctl contract`).

`scripts/validate.py` checks that contract in both directions. No skill may name a
command, subcommand or flag the CLI does not have; and no command or subcommand the CLI
*does* have may go unmentioned by every skill. The second direction is the one that broke
before — `status`, `init-spec` and `layout screen` were all real and all missing here, and
an absence is invisible to any check that only reads what the docs say. A command that
genuinely should not be documented goes in `undocumentedCommands` in
`.capcut/cli-compatibility.json` with a reason, and that list is checked too.

Flags are required to be *correct*, not to be exhaustive: these skills teach judgement and
route to `capcutctl help` for the full surface, so coverage stops at commands.

It also checks skill frontmatter, the files each `Files` table lists, and every relative
link. CI runs it, plus `scripts/test_validate.py`, which reintroduces each defect the
checker exists to catch and asserts it is still caught.

```bash
python3 scripts/validate.py        # exit 1 on any finding
python3 scripts/test_validate.py   # the checker's own regression cases
```

When the CLI's surface changes, refresh both files together:

```bash
capcutctl contract > .capcut/cli-contract.json
# then update contractSyncedFrom in .capcut/cli-compatibility.json, and re-run validate.py
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Pull requests welcome. Never force-push `main`.
Do not commit live media paths, transcripts, or QA frames.

Companion repo: [`capcut-editor-cli`](https://github.com/RoXsaita/capcut-editor-cli).
A CLI change and the skill that documents it should land as a pair.
