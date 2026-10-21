#!/usr/bin/env bash
# Refresh everything this repository vendors from the CLI, together:
#   .capcut/cli-contract.json      the machine-readable command surface
#   capcut-cli/reference.md        its rendered command reference
#   .capcut/cli-compatibility.json contractSyncedFrom (commit, branch, CLI version)
# Then validate.
#
# Usage: scripts/sync-cli.sh [--allow-dirty] PATH_TO_CAPCUT_EDITOR_CLI_CLONE
#
# The contract must describe a commit someone else can check out. So this refuses a CLI tree
# with uncommitted changes to the files the contract is generated from, refuses a detached
# HEAD, and refuses when the generated contract differs from the committed
# docs/cli-contract.json. --allow-dirty syncs anyway and stamps the commit "<sha>-dirty",
# which validate.py rejects: fine for a local experiment, never for a commit.
set -euo pipefail
usage="usage: scripts/sync-cli.sh [--allow-dirty] PATH_TO_CAPCUT_EDITOR_CLI_CLONE"
allow_dirty=0
cli=""
for arg in "$@"; do
  case "$arg" in
    --allow-dirty) allow_dirty=1 ;;
    -h|--help) echo "$usage"; exit 0 ;;
    -*) echo "$usage" >&2; exit 2 ;;
    *) cli="$arg" ;;
  esac
done
[ -n "$cli" ] || { echo "$usage" >&2; exit 2; }
cli="$(cd "$cli" && pwd)"
cd "$(cd "$(dirname "$0")/.." && pwd)"

commit=$(git -C "$cli" rev-parse --short HEAD)
branch=$(git -C "$cli" rev-parse --abbrev-ref HEAD)
if [ "$branch" = "HEAD" ]; then
  echo "sync-cli: $cli is on a detached HEAD; check out a branch so the contract names one" >&2
  exit 1
fi

dirty=$(git -C "$cli" status --porcelain --untracked-files=all -- bin src package.json tools docs)
if [ -n "$dirty" ]; then
  if [ "$allow_dirty" -ne 1 ]; then
    echo "sync-cli: the CLI tree has uncommitted changes the contract would describe:" >&2
    echo "$dirty" >&2
    echo "Sync from a clean checkout (git -C CLI worktree add DIR BRANCH), or pass --allow-dirty." >&2
    exit 1
  fi
  commit="$commit-dirty"
fi

# Record the branch as it is; an unmerged one is allowed, but say so.
if git -C "$cli" rev-parse --verify --quiet origin/main >/dev/null \
   && ! git -C "$cli" merge-base --is-ancestor HEAD origin/main; then
  echo "sync-cli: warning: $branch ($commit) is not merged into origin/main;" \
       "the contract describes an unmerged CLI branch, so land both repos together" >&2
fi

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
node "$cli/bin/capcutctl.mjs" contract > "$tmp/cli-contract.json"
node "$cli/bin/capcutctl.mjs" contract --markdown > "$tmp/reference.md"

# The contract the CLI commits must be the one it generates, or the sha names another surface.
if ! git -C "$cli" show HEAD:docs/cli-contract.json 2>/dev/null | cmp -s - "$tmp/cli-contract.json"; then
  if [ "$allow_dirty" -ne 1 ]; then
    echo "sync-cli: the generated contract differs from $branch's committed docs/cli-contract.json;" \
         "regenerate and commit it in the CLI first, or pass --allow-dirty" >&2
    exit 1
  fi
  case "$commit" in *-dirty) ;; *) commit="$commit-dirty" ;; esac
fi

mv "$tmp/cli-contract.json" .capcut/cli-contract.json
mv "$tmp/reference.md" capcut-cli/reference.md
version=$(node -p "require('$cli/package.json').version")
contract=$(node -p "require('./.capcut/cli-contract.json').contractVersion")
python3 - "$commit" "$branch" "$version" "$contract" <<'PY'
import json, sys
commit, branch, version, contract = sys.argv[1:]
path = ".capcut/cli-compatibility.json"
data = json.load(open(path))
data["requiredContractVersion"] = int(contract)
data["minimumCliVersion"] = version
data["contractSyncedFrom"] = {"commit": commit, "branch": branch, "cliVersion": version}
open(path, "w").write(json.dumps(data, indent=2) + "\n")
PY
python3 scripts/validate.py
