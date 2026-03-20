#!/usr/bin/env bash
set -euo pipefail

if ! command -v uv >/dev/null 2>&1 && [[ -f "${HOME}/.local/bin/env" ]]; then
    # shellcheck disable=SC1090
    source "${HOME}/.local/bin/env"
fi

APP_NAME="${APP_NAME:-pystonk}"
APP_DIR="${APP_DIR:-/opt/apps/${APP_NAME}}"
PYTHON_VERSION="${PYTHON_VERSION:-3.12}"
SERVICE_NAME="${SERVICE_NAME:-${APP_NAME}}"

cd "${APP_DIR}"

uv python install "${PYTHON_VERSION}"
uv sync --python "${PYTHON_VERSION}" --frozen

sudo systemctl restart "${SERVICE_NAME}"
sudo systemctl status "${SERVICE_NAME}" --no-pager
