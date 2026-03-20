#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

export APP_NAME="${APP_NAME:-pystonk}"
export DB_PATH="${DB_PATH:-/var/lib/${APP_NAME}/${APP_NAME}.sqlite3}"
export BACKUP_DIR="${BACKUP_DIR:-/var/backups/${APP_NAME}}"
export RETENTION_DAYS="${RETENTION_DAYS:-14}"

exec "${SCRIPT_DIR}/lightsail/backup_sqlite.sh"
