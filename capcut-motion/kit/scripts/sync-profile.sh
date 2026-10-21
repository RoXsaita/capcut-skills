#!/usr/bin/env bash
# Bring the creator's profile into a Remotion project, so the kit draws in THEIR brand.
#
#   kit/scripts/sync-profile.sh <remotionProjectDir> [--profile FILE]
#
# Writes <project>/src/motion/profile.json (the merged profile `capcutctl profile` prints:
# shipped defaults + ~/.config/capcutctl/profile.json + --profile) and copies the profile's
# font files into <project>/public/fonts/. theme.ts and fonts.ts read only those two things.
# Re-run it whenever the profile changes; never hand-edit the copy.
set -euo pipefail

project="${1:?Remotion project directory}"
shift
mkdir -p "$project/src/motion" "$project/public/fonts"
capcutctl profile "$@" > "$project/src/motion/profile.json"

bin="$(command -v capcutctl)"
while [ -L "$bin" ]; do
  link="$(readlink "$bin")"
  case "$link" in /*) bin="$link" ;; *) bin="$(dirname "$bin")/$link" ;; esac
done
fonts="$(cd "$(dirname "$bin")/../mograph/fonts" && pwd)"

# Font names come from a profile the creator (or anyone they took one from) wrote: only a bare
# file name with a font extension is copied, never a path out of the fonts folder.
node -e '
const path = require("path");
const p = require(process.argv[1]);
const files = [p.tokens.font, p.tokens.scene && p.tokens.scene.mono]
  .filter(Boolean).flatMap(f => Object.values(f.files || {}).flat());
const safe = files.filter(f => {
  const ok = typeof f === "string" && path.basename(f) === f && !f.startsWith(".")
    && /^[A-Za-z0-9._-]+\.(woff2?|ttf|otf)$/.test(f);
  if (!ok) console.error(`skipped unsafe font name: ${f}`);
  return ok;
});
console.log(safe.join("\n"));
' "$(cd "$project/src/motion" && pwd)/profile.json" | while read -r file; do
  [ -n "$file" ] || continue
  case "$file" in */*|..*) echo "skipped unsafe font name: $file" >&2; continue ;; esac
  if [ -f "$fonts/$file" ]; then cp -- "$fonts/$file" "$project/public/fonts/"
  else echo "missing font file: $fonts/$file (put it in public/fonts yourself)" >&2; fi
done
echo "$project/src/motion/profile.json"
