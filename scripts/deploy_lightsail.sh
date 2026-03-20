#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

export APP_NAME="${APP_NAME:-pystonk}"
export APP_DIR="${APP_DIR:-/opt/apps/${APP_NAME}}"
export PYTHON_VERSION="${PYTHON_VERSION:-3.12}"
export SERVICE_NAME="${SERVICE_NAME:-${APP_NAME}}"

exec "${SCRIPT_DIR}/lightsail/deploy_app.sh"
