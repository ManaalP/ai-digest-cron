#!/usr/bin/env bash
# ==============================================================================
# setup_pc_cron.sh
# 1-Click Installer to automate AI Pulse Daily Sync on your local Linux PC.
#
# Usage:
#   ./setup_pc_cron.sh [HH:MM, default 06:30]
#
# Examples:
#   ./setup_pc_cron.sh           # Runs every morning at 06:30 AM local time
#   ./setup_pc_cron.sh 23:00     # Runs every night at 11:00 PM local time
# ==============================================================================

set -eo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_TIME="${1:-06:30}"
HOUR="${TARGET_TIME%%:*}"
MINUTE="${TARGET_TIME##*:}"

# Validate numbers
if ! [[ "$HOUR" =~ ^[0-9]+$ ]] || ! [[ "$MINUTE" =~ ^[0-9]+$ ]] || [ "$HOUR" -gt 23 ] || [ "$MINUTE" -gt 59 ]; then
    echo "❌ Invalid time format: $TARGET_TIME. Please use HH:MM (e.g. 06:30 or 23:00)."
    exit 1
fi

echo "======================================================================"
echo "⚡ Setting up AI Pulse Local Cron Sync on your PC"
echo "======================================================================"
echo "📁 Project Directory: $PROJECT_DIR"
echo "⏰ Scheduled Run Time: Every day at $TARGET_TIME ($HOUR:$MINUTE Local Time)"
echo ""

# Ensure virtual environment exists
if [ ! -f "$PROJECT_DIR/venv/bin/python" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv "$PROJECT_DIR/venv"
    "$PROJECT_DIR/venv/bin/pip" install --upgrade pip
    "$PROJECT_DIR/venv/bin/pip" install -r "$PROJECT_DIR/requirements.txt"
fi

mkdir -p "$PROJECT_DIR/logs"

# Ensure antigravity_daily_sync.sh is executable
chmod +x "$PROJECT_DIR/antigravity_daily_sync.sh"

# Define crontab line:
# Runs antigravity_daily_sync.sh --now at the specified time every day
CRON_JOB="$MINUTE $HOUR * * * cd $PROJECT_DIR && ./antigravity_daily_sync.sh --now >> $PROJECT_DIR/logs/local_sync.log 2>&1"

# Safely install or replace existing crontab job for this project
( crontab -l 2>/dev/null | grep -v "antigravity_daily_sync.sh" | grep -v "ai-digest-cron" ; echo "$CRON_JOB" ) | crontab -

echo "✅ Crontab job installed successfully!"
echo "----------------------------------------------------------------------"
echo "Active crontab entry:"
crontab -l | grep -E "antigravity|ai-digest"
echo "----------------------------------------------------------------------"
echo ""
echo "💡 How it works:"
echo " 1. Every day at $TARGET_TIME, while your PC is on, your terminal cron wakes up."
echo " 2. It fetches only 1 day old articles for the completed previous day."
echo " 3. It syncs the articles to your Supabase database."
echo " 4. Your Vercel web app immediately displays the fresh daily feed."
echo " 5. All output is logged to: $PROJECT_DIR/logs/local_sync.log"
echo ""
echo "Test it anytime on demand by running:"
echo "  ./antigravity_daily_sync.sh --now"
echo ""
