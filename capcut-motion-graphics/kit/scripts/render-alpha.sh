#!/usr/bin/env bash
# Render a Remotion composition to ProRes 4444 with alpha, then print the
# capcutctl line that places it as generated B-roll.
#
#   kit/scripts/render-alpha.sh <entry> <compositionId> <out.mov> [--opaque]
#
# For alpha the composition must render on a transparent stage
# (`<Stage transparent>`); an opaque black stage exports as black, not clear.
# `--opaque` skips the alpha pixel format for graphics that fill their slot
# (the top half of a split-screen, say) and do not need it.
#
# The output is a *generated* asset: there is no editable original to relink,
# so `capcutctl add` needs `--generated`. Keep the .mov somewhere durable — not
# /tmp — or `add` refuses it as EPHEMERAL_MEDIA.
set -euo pipefail

entry="${1:?entry file, e.g. src/index.ts}"
comp="${2:?composition id}"
out="${3:?output .mov path}"
mode="${4:-}"

case "$out" in
  /tmp/*|"${TMPDIR:-/nonexistent}"*) echo "refusing to render into a temporary directory: capcutctl add will reject it" >&2; exit 2;;
esac

args=(--codec prores --prores-profile 4444 --image-format png --log=error)
if [ "$mode" != "--opaque" ]; then
  args+=(--pixel-format yuva444p10le)
fi

mkdir -p "$(dirname "$out")"
npx remotion render "$entry" "$comp" "$out" "${args[@]}"

if command -v ffprobe >/dev/null 2>&1; then
  ffprobe -v error -select_streams v:0 -show_entries stream=codec_name,pix_fmt,width,height,nb_frames,r_frame_rate -of default=nw=1 "$out"
fi

cat <<EOF

Place it (fill in project, time and duration; the track is created if missing):

  capcutctl add --project NAME --media "$out" --at START --dur SECONDS --track broll --volume 0 --generated --desc "$comp"

Then inspect the composite, not the .mov:

  capcutctl qa --project NAME --times START,MID,END
EOF
