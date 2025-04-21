# Wake-on-LAN Server (Flask + Tailwind UI)

A lightweight web interface running on a Raspberry Pi to remotely wake and check the status of your Windows PC using Wake-on-LAN.

---

## Features

- Wake-on-LAN (Magic Packet)
- Real-time status check: "PC is Online/Offline"
- Auto-start on Raspberry Pi boot (via `systemd`)
- One-command setup script

---

## Installation

On your **Raspberry Pi**:

```bash
git clone https://github.com/julienrollin/wakeonlan-server
cd wakeonlan-server
chmod +x setup_wol_server.sh
./setup_wol_server.sh
