#!/usr/bin/env bash
# One-time helper to install the daily cron entry.
# Usage: ./setup_cron.sh [HH:MM in 24h, default 07:00]

set -e
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TIME="${1:-07:00}"
HOUR="${TIME%%:*}"
MINUTE="${TIME##*:}"

if [ ! -d "$PROJECT_DIR/venv" ]; then
    echo "Creating virtualenv..."
    python3 -m venv "$PROJECT_DIR/venv"
    "$PROJECT_DIR/venv/bin/pip" install --upgrade pip
    "$PROJECT_DIR/venv/bin/pip" install -r "$PROJECT_DIR/requirements.txt"
fi

mkdir -p "$PROJECT_DIR/logs"

CRON_LINE="$MINUTE $HOUR * * * cd $PROJECT_DIR && $PROJECT_DIR/venv/bin/python main.py >> $PROJECT_DIR/logs/run.log 2>&1"

( crontab -l 2>/dev/null | grep -v "ai-digest-cron/main.py" ; echo "$CRON_LINE" ) | crontab -

echo "Installed cron job:"
echo "  $CRON_LINE"
echo ""
echo "View it anytime with: crontab -l"
echo "Logs will appear in: $PROJECT_DIR/logs/run.log"
