# Contributing

These are agent skills. A change here that documents a CLI flag which does
not exist yet is a bug — land the CLI change in
[capcut-editor-cli](https://github.com/RoXsaita/capcut-editor-cli) first, or
as a pair.

## Ground rules

- One job per pull request. Never force-push `main`.
- Do not add personal media paths, draft titles, transcripts, or QA frames.
- `style.md` is the default house style. Keep measured rules; do not turn it
  into a live production diary.
- `scripts/` is legacy. Prefer extending `capcutctl` over adding Python.

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
