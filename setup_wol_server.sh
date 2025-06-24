#!/bin/bash

echo "==== Wake-on-LAN Flask Server Setup ===="

# Auto-detect user
USER_NAME=$(whoami)
BASE_DIR="/home/${USER_NAME}/wakeonlan-server"

echo "[1/5] Creating application directory at ${BASE_DIR}..."
mkdir -p "$BASE_DIR"
cd "$BASE_DIR" || exit 1

echo "[2/5] Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "[3/5] Checking pip version..."
CURRENT_PIP_VERSION=$(pip --version | awk '{print $2}')
REQUIRED_PIP_VERSION="25.1.1"

if [ "$(printf '%s\n' "$REQUIRED_PIP_VERSION" "$CURRENT_PIP_VERSION" | sort -V | head -n1)" != "$REQUIRED_PIP_VERSION" ]; then
    echo "🔁 Upgrading pip to $REQUIRED_PIP_VERSION..."
    pip install --upgrade pip
else
    echo "✅ pip is already up-to-date (version $CURRENT_PIP_VERSION)"
fi

echo "[3b] Installing Python requirements..."
pip install -r requirements.txt

echo "[4/5] Creating systemd service file..."
SERVICE_FILE="/etc/systemd/system/wakeonlan.service"
sudo bash -c "cat > $SERVICE_FILE" <<EOF
[Unit]
Description=Flask Wake-on-LAN Server
After=network.target

[Service]
User=${USER_NAME}
WorkingDirectory=${BASE_DIR}
ExecStart=${BASE_DIR}/venv/bin/python3 wake_server.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

echo "[5/5] Enabling and starting the service..."
sudo systemctl daemon-reload
sudo systemctl enable wakeonlan.service
sudo systemctl restart wakeonlan.service

LOCAL_IP=$(hostname -I | awk '{print $1}')

echo ""
echo "✅ Setup complete. The server should be running at: http://${LOCAL_IP}:41264"
echo ""
echo "⚠️  Now edit wake_server.py to add your MAC and IP:"
echo "MAC_ADDRESS = 'your_mac_here'"
echo "IP_PC = 'your_ip_here'"

deactivate
exit 0
