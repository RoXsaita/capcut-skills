#!/usr/bin/env bash
# Render a Remotion composition to ProRes 4444 with PREMULTIPLIED alpha, then print the
# capcutctl lines that place it as generated B-roll.
#
#   kit/scripts/render-alpha.sh <entry> <compositionId> <out.mov> [--opaque]
#
# For alpha the composition must render on a transparent stage
# (`<Stage transparent>`); an opaque black stage exports as black, not clear.
# `--opaque` skips the alpha pixel format for graphics that fill their slot
# (the top half of a split-screen, say) and do not need it.
#
# The output is a *generated* asset: there is no editable original to relink,
# so `capcutctl add` needs `--generated`. Keep the .mov somewhere durable:
# `add` refuses temp dirs and agent scratchpads (EPHEMERAL_MEDIA), and so does
# this script, before it renders anything.
#
# Set CAPCUTCTL_HEAVY_LOCK to a lock file to serialise the render and the alpha pass
# with other heavy jobs (`lockf -k`, when lockf exists).
set -euo pipefail

entry="${1:?entry file, e.g. src/index.ts}"
comp="${2:?composition id}"
out="${3:?output .mov path}"
mode="${4:-}"

# The same rule as the CLI's origin check: resolve symlinks, then refuse the system temp
# roots, $TMPDIR, and any path with a `scratchpad` or `.scratch` part.
reason="$(python3 - "$out" <<'PY'
import os, sys
real = os.path.realpath(sys.argv[1])
roots = ["/tmp", "/private/tmp", "/var/folders", "/private/var/folders"]
if os.environ.get("TMPDIR"):
    roots.append(os.path.realpath(os.environ["TMPDIR"]))
for root in roots:
    root = os.path.realpath(root)
    if real == root or real.startswith(root.rstrip("/") + "/"):
        print(f"{real} is under the temporary directory {root}")
        break
else:
    if any(part in ("scratchpad", ".scratch") for part in real.split(os.sep)):
        print(f"{real} is inside an agent scratchpad")
PY
)"
if [ -n "$reason" ]; then
  echo "refusing to render: $reason; capcutctl add would reject it as EPHEMERAL_MEDIA. Render somewhere durable." >&2
  exit 2
fi

args=(--codec prores --prores-profile 4444 --image-format png --log=error)
if [ "$mode" != "--opaque" ]; then
  args+=(--pixel-format yuva444p10le)
fi

lock=()
if [ -n "${CAPCUTCTL_HEAVY_LOCK:-}" ] && command -v lockf >/dev/null 2>&1; then
  lock=(lockf -k "$CAPCUTCTL_HEAVY_LOCK")
fi

mkdir -p "$(dirname "$out")"
${lock[@]+"${lock[@]}"} npx remotion render "$entry" "$comp" "$out" "${args[@]}"

# CapCut composites ProRes alpha as PREMULTIPLIED. Remotion writes straight alpha, so every glow
# and soft edge keeps full colour under near-zero alpha and CapCut paints it as a coloured haze.
# Premultiply in place; capcutctl refuses to leave a leaking file (and gate fails one).
if [ "$mode" != "--opaque" ]; then
  ${lock[@]+"${lock[@]}"} capcutctl alpha "$out" --force-running >/dev/null
fi

if command -v ffprobe >/dev/null 2>&1; then
  ffprobe -v error -select_streams v:0 -show_entries stream=codec_name,pix_fmt,width,height,nb_frames,r_frame_rate -of default=nw=1 "$out"
fi

cat <<EOF

Place it (fill in project, time and duration; the track is created if missing).

A top-half graphic goes under the face, and \`capcutctl layout auto\` opens the split onto it:

  capcutctl add --project NAME --media "$out" --at START --dur SECONDS --track broll --volume 0 --generated --desc "$comp"

A full-frame graphic goes over the face, below the mograph and caption lanes (no layout auto):

  capcutctl add --project NAME --media "$out" --at START --dur SECONDS --track gfx --layer top --volume 0 --generated --desc "$comp"

Then inspect the composite, not the .mov:

  capcutctl qa --project NAME --times START,MID,END
EOF
