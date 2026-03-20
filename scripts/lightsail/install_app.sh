#!/usr/bin/env bash
set -euo pipefail

if ! command -v uv >/dev/null 2>&1 && [[ -f "${HOME}/.local/bin/env" ]]; then
    # shellcheck disable=SC1090
    source "${HOME}/.local/bin/env"
fi

require_var() {
    local name="$1"
    if [[ -z "${!name:-}" ]]; then
        echo "Missing required variable: ${name}" >&2
        exit 1
    fi
}

APP_NAME="${APP_NAME:-}"
APP_DOMAIN="${APP_DOMAIN:-}"
APP_PORT="${APP_PORT:-}"
APP_REPO_URL="${APP_REPO_URL:-}"
PYTHON_VERSION="${PYTHON_VERSION:-3.12}"
APP_ENTRYPOINT="${APP_ENTRYPOINT:-pystonk-web}"
APP_ROOT="${APP_ROOT:-/opt/apps}"
APP_DIR="${APP_DIR:-${APP_ROOT}/${APP_NAME}}"
APP_USER="${APP_USER:-${APP_NAME}}"
ENV_DIR="${ENV_DIR:-/etc/${APP_NAME}}"
ENV_FILE="${ENV_FILE:-${ENV_DIR}/${APP_NAME}.env}"
DATA_DIR="${DATA_DIR:-/var/lib/${APP_NAME}}"
SERVICE_FILE="${SERVICE_FILE:-/etc/systemd/system/${APP_NAME}.service}"
CADDY_SITE_FILE="${CADDY_SITE_FILE:-/etc/caddy/sites-enabled/${APP_NAME}.caddy}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SERVICE_TEMPLATE="${SERVICE_TEMPLATE:-${REPO_ROOT}/deploy/lightsail/templates/app.service.tpl}"
CADDY_TEMPLATE="${CADDY_TEMPLATE:-${REPO_ROOT}/deploy/lightsail/templates/app.caddy.tpl}"
ENV_EXAMPLE_PATH="${ENV_EXAMPLE_PATH:-deploy/lightsail/${APP_NAME}.env.example}"

require_var APP_NAME
require_var APP_DOMAIN
require_var APP_PORT
require_var APP_REPO_URL

render_template() {
    local template="$1"
    sed \
        -e "s|__APP_NAME__|${APP_NAME}|g" \
        -e "s|__APP_DOMAIN__|${APP_DOMAIN}|g" \
        -e "s|__APP_PORT__|${APP_PORT}|g" \
        -e "s|__APP_USER__|${APP_USER}|g" \
        -e "s|__APP_DIR__|${APP_DIR}|g" \
        -e "s|__ENV_FILE__|${ENV_FILE}|g" \
        -e "s|__DATA_DIR__|${DATA_DIR}|g" \
        -e "s|__APP_ENTRYPOINT__|${APP_ENTRYPOINT}|g" \
        "${template}"
}

if ! id -u "${APP_USER}" >/dev/null 2>&1; then
    sudo useradd --system --home "${APP_DIR}" --shell /usr/sbin/nologin "${APP_USER}"
fi

sudo mkdir -p "${APP_ROOT}" "${ENV_DIR}" "${DATA_DIR}" /etc/caddy/sites-enabled
sudo chown -R "${APP_USER}:${APP_USER}" "${DATA_DIR}"

if [[ -d "${APP_DIR}/.git" ]]; then
    echo "Using existing checkout at ${APP_DIR}"
else
    if [[ -e "${APP_DIR}" ]]; then
        echo "Target app directory exists but is not a git checkout: ${APP_DIR}" >&2
        exit 1
    fi
    sudo mkdir -p "$(dirname "${APP_DIR}")"
    sudo chown -R "${USER}:${USER}" "$(dirname "${APP_DIR}")"
    git clone "${APP_REPO_URL}" "${APP_DIR}"
fi

cd "${APP_DIR}"

uv python install "${PYTHON_VERSION}"
uv sync --python "${PYTHON_VERSION}" --frozen

if [[ ! -f "${ENV_FILE}" ]]; then
    if [[ -f "${APP_DIR}/${ENV_EXAMPLE_PATH}" ]]; then
        sudo cp "${APP_DIR}/${ENV_EXAMPLE_PATH}" "${ENV_FILE}"
    else
        sudo touch "${ENV_FILE}"
    fi
fi

render_template "${SERVICE_TEMPLATE}" | sudo tee "${SERVICE_FILE}" >/dev/null
render_template "${CADDY_TEMPLATE}" | sudo tee "${CADDY_SITE_FILE}" >/dev/null

sudo systemctl daemon-reload
sudo systemctl enable "${APP_NAME}"
sudo systemctl restart "${APP_NAME}"
sudo systemctl restart caddy

echo "App install complete for ${APP_NAME}."
echo "Env file: ${ENV_FILE}"
echo "Service file: ${SERVICE_FILE}"
echo "Caddy site: ${CADDY_SITE_FILE}"
