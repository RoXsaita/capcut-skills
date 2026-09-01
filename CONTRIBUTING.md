# Contributing

These are agent skills. A change here that documents a CLI flag which does
not exist yet is a bug — land the CLI change in
[capcut-editor-cli](https://github.com/RoXsaita/capcut-editor-cli) first, or
as a pair.

That is now enforced rather than remembered. `scripts/validate.py` checks every
`capcutctl` command and flag in these documents against
`.capcut/cli-contract.json`, the CLI's own published surface, and CI runs it on
every pull request:

```bash
python3 scripts/validate.py
```

If your change documents a new CLI capability, the CLI change must be pushed
first; then refresh `.capcut/cli-contract.json` (`capcutctl contract >
.capcut/cli-contract.json`) and the `contractSyncedFrom` block in
`.capcut/cli-compatibility.json` in the same pull request, and link the two PRs
to each other.

## Ground rules

- One job per pull request. Never force-push `main`.
- Do not add personal media paths, draft titles, transcripts, or QA frames.
- `style.md` is the default house style. Keep measured rules; do not turn it
  into a live production diary.
- `capcut-editing/scripts/` is legacy. Prefer extending `capcutctl` over adding
  Python there. Top-level `scripts/` is this repository's own checkers and is not
  legacy — that is where a new validation rule goes.

## Install

Symlink the four skill directories into the agent you use:

```bash
for AGENT in ~/.claude ~/.codex ~/.grok ~/.hermes; do
  [ -d "$AGENT" ] || continue
  mkdir -p "$AGENT/skills"
  for S in capcut-cli capcut-editing capcut-editing-talking-head capcut-editing-screen-recording; do
    ln -sfn "$PWD/$S" "$AGENT/skills/$S"
  done
done
```

`capcutctl` itself is the other repo. See its SETUP.md.

## License

By contributing you agree that your work is licensed under the MIT License
in `LICENSE`.
