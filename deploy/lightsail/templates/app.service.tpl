[Unit]
Description=__APP_NAME__ service
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=__APP_USER__
Group=__APP_USER__
WorkingDirectory=__APP_DIR__
EnvironmentFile=__ENV_FILE__
ExecStart=__APP_DIR__/.venv/bin/__APP_ENTRYPOINT__
Restart=always
RestartSec=5
TimeoutStopSec=15
PrivateTmp=true
NoNewPrivileges=true
ProtectSystem=full
ProtectHome=true
ReadWritePaths=__DATA_DIR__

[Install]
WantedBy=multi-user.target
