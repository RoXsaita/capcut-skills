# capcut-skills

**Unofficial.** Not affiliated with ByteDance or CapCut. MIT licensed — see [LICENSE](LICENSE) and [NOTICE](NOTICE).

Agent skills for producing production-grade, highly animated CapCut shorts with `capcutctl`.

| Skill | Use it for |
|---|---|
| `capcut-editing` | **Start here.** The whole procedure: style question, A-roll cut and sign-off, shot list, `edit.json`, `build`, `gate`, review, hand-off |
| `capcut-cli` | The rules `capcutctl` enforces, and `reference.md` — the generated command reference |
| `capcut-motion-design` | Motion design: full-frame scenes (openers, hook slams, transitions, reveals, name cards) and overlay graphics — the catalog, the grammar, the promotion bar |
| `capcut-motion-graphics` | Drawn B-roll that does not look generated: the rulebook, named easings, the Remotion kit, alpha render → `capcutctl add --generated` |

Install by symlink into the agent's skills directory; see [the install steps](CONTRIBUTING.md#install).
Set up the CLI with its [SETUP.md](https://github.com/RoXsaita/capcut-editor-cli/blob/main/SETUP.md).

**Agents: before the first write, ask which style to use** — the bundled house profile, a profile
harvested from the user's own drafts (`capcutctl harvest --profile`), or blank. See
`capcut-editing/SKILL.md`.

The taste lives in the CLI's `presets/profile.json` (tokens, camera, seams, sound, density targets,
motion grammar), not in these documents: `capcutctl build` applies it and `capcutctl gate` enforces it.
`docs/` holds history that is not on an agent's path (the private recorder, retired scripts).

## Which `capcutctl` these skills describe

`.capcut/cli-compatibility.json` names the CLI commit and contract revision these documents are
written against, `.capcut/cli-contract.json` is a verbatim copy of that CLI's published command
surface (`capcutctl contract`), and `capcut-cli/reference.md` is its rendered form
(`capcutctl contract --markdown`). Refresh all three with `scripts/sync-cli.sh PATH_TO_CLI`.
The `CLI drift` workflow compares them with the CLI's `main` weekly.

`scripts/validate.py` checks documented `capcutctl` command names and flags in code
blocks and inline code against that contract, including shell continuation lines. It catches unknown commands
and flags; it does not validate argument values, execute examples or prove behavioral claims. It
also checks skill frontmatter, the files each `Files` table
lists, and every relative link. CI runs it, plus `scripts/test_validate.py`, which
reintroduces each defect the checker exists to catch and asserts it is still caught.

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
