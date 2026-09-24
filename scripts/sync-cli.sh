#!/usr/bin/env bash
# Refresh everything this repository vendors from the CLI, together:
#   .capcut/cli-contract.json      the machine-readable command surface
#   capcut-cli/reference.md        its rendered command reference
#   .capcut/cli-compatibility.json contractSyncedFrom (commit, branch, CLI version)
# Then validate. Usage: scripts/sync-cli.sh PATH_TO_CAPCUT_EDITOR_CLI_CLONE
set -euo pipefail
cli="${1:?usage: scripts/sync-cli.sh PATH_TO_CAPCUT_EDITOR_CLI_CLONE}"
cd "$(cd "$(dirname "$0")/.." && pwd)"
node "$cli/bin/capcutctl.mjs" contract > .capcut/cli-contract.json
node "$cli/bin/capcutctl.mjs" contract --markdown > capcut-cli/reference.md
commit=$(git -C "$cli" rev-parse --short HEAD)
branch=$(git -C "$cli" rev-parse --abbrev-ref HEAD)
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
