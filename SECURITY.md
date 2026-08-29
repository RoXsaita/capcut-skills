# Security policy

These skills tell an agent how to drive `capcutctl`, which writes CapCut
project JSON on disk. A bad instruction can corrupt a draft.

## Reporting

Please **do not** open a public issue for secret leakage, prompt-injection
into these skill files that would cause destructive writes, or anything that
would put a private media path or transcript into a public repo.

https://github.com/RoXsaita/capcut-skills/security/advisories/new

## Do not commit

- Live camera / screen-recording paths
- Transcripts, EDLs, or QA frames
- `.env` / API keys (music generation lives in the CLI)
- `presets/harvest.json` (that file belongs to the CLI repo and is gitignored there)

`references/project-state.md` must stay generic. Current sources belong in
the user's own notes, not in this repository.
