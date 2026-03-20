#!/usr/bin/env bash
set -euo pipefail

APP_NAME="${APP_NAME:-pystonk}"
DB_PATH="${DB_PATH:-/var/lib/${APP_NAME}/${APP_NAME}.sqlite3}"
BACKUP_DIR="${BACKUP_DIR:-/var/backups/${APP_NAME}}"
RETENTION_DAYS="${RETENTION_DAYS:-14}"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"

mkdir -p "${BACKUP_DIR}"
sqlite3 "${DB_PATH}" ".backup '${BACKUP_DIR}/${APP_NAME}-${TIMESTAMP}.sqlite3'"
find "${BACKUP_DIR}" -type f -name "${APP_NAME}-*.sqlite3" -mtime "+${RETENTION_DAYS}" -delete
