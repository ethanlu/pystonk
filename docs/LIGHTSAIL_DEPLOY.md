# Lightsail Deployment

## Goal

Run `pystonk` on a reusable Ubuntu 24.04 Lightsail host using:

- `uv` + Python `3.12`
- `systemd` as the required process manager
- `Caddy` for domain routing and TLS
- `git pull` on the VM for updates
- SQLite on local disk for watchlists and presets

This deployment pattern is designed to host more than one small app later.

## Standard Host Layout

One app = one user, one localhost port, one `systemd` unit, one env file, one Caddy site.

Shared paths:

- app code: `/opt/apps/<app>`
- env file: `/etc/<app>/<app>.env`
- mutable data: `/var/lib/<app>`
- systemd unit: `/etc/systemd/system/<app>.service`
- Caddy site: `/etc/caddy/sites-enabled/<app>.caddy`

`pystonk` defaults:

- app name: `pystonk`
- user: `pystonk`
- port: `8000`
- code path: `/opt/apps/pystonk`
- env path: `/etc/pystonk/pystonk.env`
- db path: `/var/lib/pystonk/pystonk.sqlite3`

## Manual Cloud Steps

1. Create a Lightsail Ubuntu 24.04 instance.
2. Attach a static IP.
3. Point your DNS record at the static IP.
4. Open ports `22`, `80`, and `443` in Lightsail networking.
5. SSH into the instance.

## First-Time Server Bootstrap

You need one temporary checkout of the repo to access the bootstrap scripts. Start with the smallest manual setup possible:

```bash
sudo apt update
sudo apt install -y git curl
git clone <YOUR_REPO_URL> ~/pystonk-bootstrap
cd ~/pystonk-bootstrap
./scripts/lightsail/bootstrap_host.sh
```

That script:

- installs `curl`, `git`, `sqlite3`, and `caddy`
- installs `uv`
- creates `/opt/apps` and `/etc/caddy/sites-enabled`
- ensures the main Caddy config imports `sites-enabled/*.caddy`

## Install `pystonk`

Run the app installer from the bootstrap checkout:

```bash
cd ~/pystonk-bootstrap
APP_NAME=pystonk \
APP_DOMAIN=pystonk.example.com \
APP_PORT=8000 \
APP_REPO_URL=<YOUR_REPO_URL> \
APP_ENTRYPOINT=pystonk-web \
./scripts/lightsail/install_app.sh
```

The installer will:

- create the `pystonk` Linux user
- clone the repo into `/opt/apps/pystonk` if missing
- install Python `3.12`
- run `uv sync --python 3.12 --frozen`
- create `/etc/pystonk` and `/var/lib/pystonk`
- create `/etc/pystonk/pystonk.env` from the example file if missing
- generate the `systemd` unit and Caddy site file from templates
- reload `systemd`
- enable and restart the `pystonk` service
- reload `caddy`

## Fill In Secrets

Edit the generated env file:

```bash
sudo nano /etc/pystonk/pystonk.env
```

Set at least:

```bash
PYSTONK_SCHWAB_KEY=your-key
PYSTONK_SCHWAB_SECRET=your-secret
PYSTONK_LOG_LEVEL=INFO
PYSTONK_WEB_HOST=127.0.0.1
PYSTONK_WEB_PORT=8000
PYSTONK_WEB_DB_PATH=/var/lib/pystonk/pystonk.sqlite3
```

Then restart the service:

```bash
sudo systemctl restart pystonk
```

## Verification

Local verification:

```bash
systemctl status pystonk --no-pager
systemctl is-enabled pystonk
curl http://127.0.0.1:8000/health
```

Public verification after DNS propagation:

```bash
systemctl status caddy --no-pager
curl -I https://pystonk.example.com/health
```

## Ongoing Deploys

Deploys happen from the app checkout on the VM:

```bash
cd /opt/apps/pystonk
git pull
./scripts/deploy_lightsail.sh
```

The wrapper script calls the reusable deploy script, which:

- runs `uv sync --python 3.12 --frozen`
- restarts the `pystonk` service
- prints `systemctl status`

## Backups

SQLite remains local in v1, so keep backups simple:

- enable Lightsail snapshots
- run the backup script from cron if you want file-level restores

Example:

```cron
0 3 * * * APP_NAME=pystonk /opt/apps/pystonk/scripts/backup_sqlite.sh
```

## Multi-App Pattern

When you add future apps, reuse the same host conventions:

- `tool1.example.com` -> `127.0.0.1:8000`
- `tool2.example.com` -> `127.0.0.1:8001`
- `tool3.example.com` -> `127.0.0.1:8002`

For each app:

- one Linux user
- one repo checkout under `/opt/apps/<app>`
- one env file under `/etc/<app>`
- one data directory under `/var/lib/<app>`
- one `systemd` unit
- one Caddy site file

## Notes

- `systemd` is required in this deployment pattern.
- `nohup` is only for smoke tests, not real runtime management.
- `uv.lock` should be committed so deploys can use `--frozen`.
