# capcut-skills

Agent skills for editing CapCut projects with `capcutctl`. The hub is `capcut-editing/`; start there.

| Skill | Use it for |
|---|---|
| `capcut-cli` | what `capcutctl` already does — read this before hand-writing JSON |
| `capcut-editing` | format, style, pitfalls, project state |
| `capcut-editing-talking-head` | cutting the face, layouts |
| `capcut-editing-screen-recording` | B-roll, `rl2`, OCR matching |

Install by symlink into the agent's skills dir, e.g. `~/.grok/skills/`, `~/.claude/skills/`, `~/.codex/skills/`.

## Working together

Private repo, two people. Collaborator with Write is the whole access model.

- Pull `main` before you start.
- Short-lived branches. Open a PR even if you merge it yourself — that is the paper trail, not a gate. Self-merge is fine.
- Direct commits to `main` are ok for a typo or a one-liner you would not mind landing on you with no warning.
- Never force-push `main`.
- One job per PR. Say so in chat if you are about to touch the same files.

This repo is one of three:

- [`capcut-editor-cli`](https://github.com/RoXsaita/capcut-editor-cli) — `capcutctl`
- [`capcut-skills`](https://github.com/RoXsaita/capcut-skills) — this repo
- [`recording-layout-v2`](https://github.com/RoXsaita/recording-layout-v2) — `rl2`, the recorder

A CLI change and the skill that documents it should land as a pair. Same if a skill points at `rl2`.
