#!/usr/bin/env bash
set -euo pipefail

if ! command -v sudo >/dev/null 2>&1; then
    echo "This script requires sudo access." >&2
    exit 1
fi

if ! command -v uv >/dev/null 2>&1 && [[ -f "${HOME}/.local/bin/env" ]]; then
    # shellcheck disable=SC1090
    source "${HOME}/.local/bin/env"
fi

APP_ROOT="${APP_ROOT:-/opt/apps}"
CADDY_SITES_DIR="${CADDY_SITES_DIR:-/etc/caddy/sites-enabled}"
CADDYFILE_PATH="${CADDYFILE_PATH:-/etc/caddy/Caddyfile}"
CADDY_IMPORT_LINE="import ${CADDY_SITES_DIR}/*.caddy"

sudo apt update
sudo apt install -y curl git sqlite3 debian-keyring debian-archive-keyring apt-transport-https gpg

if ! command -v uv >/dev/null 2>&1; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # shellcheck disable=SC1090
    source "${HOME}/.local/bin/env"
fi

if [[ ! -f /usr/share/keyrings/caddy-stable-archive-keyring.gpg ]]; then
    curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
fi

if [[ ! -f /etc/apt/sources.list.d/caddy-stable.list ]]; then
    curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list >/dev/null
fi

sudo apt update
sudo apt install -y caddy

sudo mkdir -p "${APP_ROOT}" "${CADDY_SITES_DIR}"

if [[ ! -f "${CADDYFILE_PATH}" ]]; then
    echo "${CADDY_IMPORT_LINE}" | sudo tee "${CADDYFILE_PATH}" >/dev/null
elif ! sudo grep -Fq "${CADDY_IMPORT_LINE}" "${CADDYFILE_PATH}"; then
    printf "\n%s\n" "${CADDY_IMPORT_LINE}" | sudo tee -a "${CADDYFILE_PATH}" >/dev/null
fi

sudo systemctl enable caddy >/dev/null 2>&1 || true
sudo systemctl restart caddy

echo "Host bootstrap complete."
