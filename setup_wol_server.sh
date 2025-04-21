#!/bin/bash

echo "==== Wake-on-LAN Flask Server Setup ===="

read -p "Enter your username (used for home directory): " USERNAME

APP_DIR="/home/$USERNAME/wakeonlan-server"

echo "[1/5] Creating application directory..."
mkdir -p "$APP_DIR"

cd "$APP_DIR" || exit 1

echo "[2/5] Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "[3/5] Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "[4/5] Creating systemd service..."

SERVICE_FILE="/etc/systemd/system/wakeonlan.service"
sudo bash -c "cat > $SERVICE_FILE" <<EOL
[Unit]
Description=Flask Wake-on-LAN Server
After=network.target

[Service]
User=$USERNAME
WorkingDirectory=$APP_DIR
ExecStart=$APP_DIR/venv/bin/python3 wake_server.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOL

echo "[5/5] Enabling and starting service..."
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable wakeonlan.service
sudo systemctl start wakeonlan.service

echo "Setup complete. The server should now be running on port 8080."
