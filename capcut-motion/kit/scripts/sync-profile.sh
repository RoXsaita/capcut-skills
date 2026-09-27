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

node -e '
const p = require(process.argv[1]);
const files = [p.tokens.font, p.tokens.scene && p.tokens.scene.mono]
  .filter(Boolean).flatMap(f => Object.values(f.files || {}).flat());
console.log(files.join("\n"));
' "$(cd "$project/src/motion" && pwd)/profile.json" | while read -r file; do
  [ -n "$file" ] || continue
  if [ -f "$fonts/$file" ]; then cp "$fonts/$file" "$project/public/fonts/"
  else echo "missing font file: $fonts/$file (put it in public/fonts yourself)" >&2; fi
done
echo "$project/src/motion/profile.json"
