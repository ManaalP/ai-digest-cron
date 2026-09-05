#!/usr/bin/env bash
# ==============================================================================
# antigravity_daily_sync.sh
# Local terminal daemon & manual runner for AI Pulse Daily Digest.
#
# Usage:
#   ./antigravity_daily_sync.sh --now         # Run immediate sync for yesterday
#   ./antigravity_daily_sync.sh --daemon 06:30 # Run persistent loop waking up at 06:30 AM
# ==============================================================================

set -eo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

mkdir -p "$SCRIPT_DIR/logs"
LOG_FILE="$SCRIPT_DIR/logs/local_sync.log"

run_sync() {
    echo "======================================================================" | tee -a "$LOG_FILE"
    echo "⚡ [$(date '+%Y-%m-%d %H:%M:%S')] Antigravity Local Sync Initiated" | tee -a "$LOG_FILE"
    echo "======================================================================" | tee -a "$LOG_FILE"
    
    # Check virtual environment
    if [ ! -f "$SCRIPT_DIR/venv/bin/python" ]; then
        echo "❌ Virtualenv not found at $SCRIPT_DIR/venv. Please run: python3 -m venv venv && pip install -r requirements.txt" | tee -a "$LOG_FILE"
        return 1
    fi

    # Load environment variables if .env exists
    if [ -f "$SCRIPT_DIR/.env" ]; then
        set -a
        # shellcheck disable=SC1091
        source "$SCRIPT_DIR/.env"
        set +a
    fi

    # Run main.py targeting the completed previous day and enforcing strict 1-day retention
    "$SCRIPT_DIR/venv/bin/python" "$SCRIPT_DIR/main.py" --yesterday --retention-days=1 2>&1 | tee -a "$LOG_FILE"
    
    echo "✅ [$(date '+%Y-%m-%d %H:%M:%S')] Antigravity Sync Completed Successfully." | tee -a "$LOG_FILE"
}

if [ "$1" == "--now" ] || [ -z "$1" ]; then
    run_sync
    exit 0
fi

if [ "$1" == "--daemon" ]; then
    TARGET_TIME="${2:-06:30}"
    echo "🟢 Antigravity Local Sync Daemon Running in Terminal."
    echo "⏰ Scheduled to execute daily at $TARGET_TIME (Local Time)."
    echo "💡 Keep this terminal window open. If your PC is on, it will automatically update your feed."
    echo "Press [Ctrl+C] to stop."
    echo ""

    while true; do
        CURRENT_TIME=$(date '+%H:%M')
        if [ "$CURRENT_TIME" == "$TARGET_TIME" ]; then
            echo "🚀 Target time $TARGET_TIME reached! Starting synchronization..."
            run_sync || true
            # Sleep 70 seconds so we don't trigger twice in the same minute
            sleep 70
        fi
        sleep 25
    done
fi

echo "Unknown option: $1"
echo "Usage: ./antigravity_daily_sync.sh [--now | --daemon HH:MM]"
exit 1
