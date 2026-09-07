# Retired Python helpers

The maintained tooling is in [capcut-editor-cli](https://github.com/RoXsaita/capcut-editor-cli).
These one-off helpers were removed because they bypassed project transactions, used
production-specific edit lists, or duplicated indexes and previews that had since been fixed
in the CLI. They are available in Git history for historical comparison; do not run them
against a current project.

| Retired helpers | Maintained replacement |
|---|---|
| `vo_plan.py`, `vo_cut.py`, `vo_rebuild_capcut.py`, `beats.py` | `capcutctl cut` for the reviewed A-roll plan and build |
| `build.py`, `to_overlays.py` | `capcutctl new`, `add` and transactional `apply` |
| `capcut.py` | `capcutctl scenes`, `doctor`, `snapshot`, `apply` and `preview` |
| `presets.py`, `layout_preview.py` | `capcutctl layout` and `qa` |
| `render.py`, `full.py` | `capcutctl preview` for a proxy of the actual current project |
| `match.py` | `capcutctl find --shows --strip` with verified OCR caches |
| `audio_index.py` | `capcutctl cut`; its maintained implementation is `tools/audio_index.py` in the CLI repo |

The CLI owns runtime dependencies; follow its SETUP.md and `capcutctl preflight`.
This skills repository requires only Python 3.11+ to run its top-level validation scripts.
