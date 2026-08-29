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

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Pull requests welcome. Never force-push `main`.
Do not commit live media paths, transcripts, or QA frames.

Companion repo: [`capcut-editor-cli`](https://github.com/RoXsaita/capcut-editor-cli).
A CLI change and the skill that documents it should land as a pair.
