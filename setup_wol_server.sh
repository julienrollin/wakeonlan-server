#!/bin/bash

echo "==== Wake-on-LAN Flask Server Setup ===="

USERNAME=$(whoami)
USER_HOME="/home/$USERNAME"
INSTALL_DIR="$USER_HOME/wakeonlan-server"

echo "[1/5] Creating application directory..."
mkdir -p "$INSTALL_DIR"

echo "[2/5] Copying files to $INSTALL_DIR..."
cp wake_server.py requirements.txt "$INSTALL_DIR"

echo "[3/5] Creating virtual environment..."
python3 -m venv "$INSTALL_DIR/venv"

echo "[4/5] Installing dependencies..."
source "$INSTALL_DIR/venv/bin/activate"
pip install --upgrade pip
pip install -r "$INSTALL_DIR/requirements.txt"

echo "[5/5] Creating systemd service..."

SERVICE_FILE="/etc/systemd/system/wakeonlan.service"
sudo bash -c "cat > $SERVICE_FILE" <<EOL
[Unit]
Description=Flask Wake-on-LAN Server
After=network.target

[Service]
User=$USERNAME
WorkingDirectory=$INSTALL_DIR
ExecStart=$INSTALL_DIR/venv/bin/python3 wake_server.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOL

echo "Enabling and starting service..."
sudo systemctl daemon-reload
sudo systemctl enable wakeonlan.service
sudo systemctl start wakeonlan.service

echo "✅ Setup complete. The server should be running at http://<your-ip>:8080"
