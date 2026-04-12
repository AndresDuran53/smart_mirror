#!/bin/bash
# Start the Smart Mirror application
# This script is designed to be called from an autostart .desktop file
# so that the DISPLAY environment variable is already set by the desktop session.

SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$SCRIPT_DIR"

# Activate virtual environment
source "$SCRIPT_DIR/.venv/bin/activate"

# Run the smart mirror
exec python3 "$SCRIPT_DIR/smartmirror.py"
