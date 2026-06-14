#!/bin/bash
set -e
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'
info()    { echo -e "${BLUE}[INFO]${NC} $1"; }
success() { echo -e "${GREEN}[OK]${NC} $1"; }
error()   { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

clear
echo -e "${GREEN}"
echo "╔══════════════════════════════════════════════════════╗"
echo "║         Football Bot (foti) - Auto Installer         ║"
echo "║              Ubuntu 22.04 | Python 3.11              ║"
echo "╚══════════════════════════════════════════════════════╝"
echo -e "${NC}"

[[ $EUID -ne 0 ]] && error "Run as root: sudo bash install.sh"

echo ""
read -p "$(echo -e ${YELLOW})Telegram Bot Token: $(echo -e ${NC})" BOT_TOKEN
[[ -z "$BOT_TOKEN" ]] && error "Bot token is required"

read -p "$(echo -e ${YELLOW})Admin Telegram ID (numeric): $(echo -e ${NC})" ADMIN_ID
[[ ! "$ADMIN_ID" =~ ^[0-9]+$ ]] && error "Admin ID must be numeric"

read -p "$(echo -e ${YELLOW})Install directory [/opt/foti]: $(echo -e ${NC})" INSTALL_DIR
INSTALL_DIR=${INSTALL_DIR:-/opt/foti}

DB_PASS=$(openssl rand -hex 16)
API_KEY=$(openssl rand -hex 32)

info "Installing to: $INSTALL_DIR"

info "Installing system packages..."
apt-get update -qq
apt-get install -y -qq python3.11 python3.11-venv python3-pip \
    postgresql postgresql-contrib redis-server git curl openssl \
    build-essential libpq-dev > /dev/null 2>&1
success "System packages installed"

info "Configuring PostgreSQL..."
systemctl start postgresql && systemctl enable postgresql
sudo -u postgres psql -c "CREATE USER foti WITH PASSWORD '$DB_PASS';" 2>/dev/null || true
sudo -u postgres psql -c "CREATE DATABASE foti_db OWNER foti;" 2>/dev/null || true
success "PostgreSQL ready"

info "Starting Redis..."
systemctl start redis-server && systemctl enable redis-server
success "Redis ready"

info "Setting up $INSTALL_DIR ..."
mkdir -p "$INSTALL_DIR" && cd "$INSTALL_DIR"
if [[ -d ".git" ]]; then
    git pull origin main
else
    git clone https://github.com/moha100h/foti.git .
fi
mkdir -p logs

info "Creating Python virtual environment..."
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q
success "Python environment ready"

info "Writing .env ..."
cat > .env << ENVEOF
BOT_TOKEN=$BOT_TOKEN
ADMIN_IDS=$ADMIN_ID
DATABASE_URL=postgresql+asyncpg://foti:$DB_PASS@localhost:5432/foti_db
REDIS_URL=redis://localhost:6379/0
ADMIN_API_KEY=$API_KEY
ADMIN_HOST=0.0.0.0
ADMIN_PORT=8000
LOG_LEVEL=INFO
LOG_FILE=logs/foti.log
ELO_INITIAL=1500
CONFIDENCE_THRESHOLD=0.6
CACHE_TTL=3600
LIVE_CACHE_TTL=60
RATE_LIMIT=60
RATE_LIMIT_WINDOW=60
ENVEOF
success ".env created"

info "Running database migrations..."
python -m alembic upgrade head
success "Migrations done"

info "Installing systemd service..."
cat > /etc/systemd/system/foti.service << SVCEOF
[Unit]
Description=Foti Football Telegram Bot
After=network.target postgresql.service redis.service

[Service]
Type=simple
User=root
WorkingDirectory=$INSTALL_DIR
ExecStart=$INSTALL_DIR/venv/bin/python -m football_bot.main
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
EnvironmentFile=$INSTALL_DIR/.env

[Install]
WantedBy=multi-user.target
SVCEOF

systemctl daemon-reload
systemctl enable foti
systemctl start foti
success "Service foti started"

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║              Installation Complete!                  ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "  ${BLUE}Directory:${NC}   $INSTALL_DIR"
echo -e "  ${BLUE}Status:${NC}      systemctl status foti"
echo -e "  ${BLUE}Logs:${NC}        journalctl -u foti -f"
echo -e "  ${BLUE}Admin API:${NC}   http://$(hostname -I | awk '{print $1}'):8000"
echo ""
