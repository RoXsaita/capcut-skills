# Contributing

These are agent skills. A change here that documents a CLI flag which does
not exist yet is a bug — land the CLI change in
[capcut-editor-cli](https://github.com/RoXsaita/capcut-editor-cli) first, or
as a pair.

`scripts/validate.py` checks documented `capcutctl` command names and flags against
`.capcut/cli-contract.json`, the CLI's own published surface, and CI runs it on
every pull request:

```bash
python3 scripts/validate.py
python3 scripts/test_validate.py
```

If your change documents a new CLI capability, the CLI change must be pushed
first; then run `scripts/sync-cli.sh PATH_TO_CLI_CLONE`, which refreshes
`.capcut/cli-contract.json`, the generated `capcut-cli/reference.md` and the
`contractSyncedFrom` block together, and link the two PRs to each other.

If you previously installed the four-skill layout, remove the retired
`capcut-editing-talking-head` and `capcut-editing-screen-recording` links.

## Ground rules

- One job per pull request. Never force-push `main`.
- Do not add personal media paths, draft titles, transcripts, or QA frames.
- The style targets live in the CLI's `presets/profile.json`. `style.md` is
  provenance; keep measured facts there, and never restate a rule the profile
  owns (the validator rejects the retired ones).
- The retired helpers in `docs/retired-scripts.md` are replaced by the CLI.
  Extend `capcutctl` for runtime behavior; top-level `scripts/` contains this
  repository's validation checks.

## Install

From the root of this clone, symlink the four skill directories into the agent you use.
This example selects Codex; set `agent_skills` to another agent's skills directory as needed.
Existing installations are skipped so the command cannot nest links inside an installed skill
or overwrite unrelated customizations. Review an existing entry before replacing it.

```bash
agent_skills="${CODEX_HOME:-$HOME/.codex}/skills"
mkdir -p "$agent_skills"
for skill in capcut-cli capcut-editing capcut-motion; do
  if [ -e "$agent_skills/$skill" ] || [ -L "$agent_skills/$skill" ]; then
    printf 'Skipped existing skill: %s\n' "$agent_skills/$skill"
    continue
  fi
  ln -s "$PWD/$skill" "$agent_skills/$skill"
done
```

`capcutctl` itself is the other repo. See its SETUP.md.

## License

By contributing you agree that your work is licensed under the MIT License
in `LICENSE`.
