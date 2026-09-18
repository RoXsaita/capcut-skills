#!/usr/bin/env bash
# Render stills of a Remotion composition at the frames you want to inspect.
# Rendering is the last step; stills are the feedback loop.
#
#   kit/scripts/stills.sh <entry> <compositionId> <outDir> <frame> [frame...]
#   kit/scripts/stills.sh src/index.ts Terminal qa/terminal 12 40 66 120 174
#
# Then look at every frame you asked for. Check, in this order: is anything on
# screen that is not the subject or the type; does every element that is
# moving sit on a named curve; is any move under 1px/frame; is the copy within
# its limit; is the picture identical to what a full render would show (no
# Math.random, no Date.now, no wall clock).
set -euo pipefail

entry="${1:?entry file, e.g. src/index.ts}"
comp="${2:?composition id}"
out="${3:?output directory}"
shift 3
[ "$#" -gt 0 ] || { echo "at least one frame number" >&2; exit 2; }

mkdir -p "$out"
for f in "$@"; do
  npx remotion still "$entry" "$comp" "$out/$comp-$(printf '%04d' "$f").png" --frame "$f" --log=error
  echo "$out/$comp-$(printf '%04d' "$f").png"
done
