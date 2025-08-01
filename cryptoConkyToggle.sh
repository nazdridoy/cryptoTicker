#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONKY_CONFIG="$SCRIPT_DIR/cryptoConky.conf"

# Check if Conky is running
if pgrep -f "cryptoConky.conf" > /dev/null; then
    echo "Stopping Conky..."
    pkill -f "cryptoConky.conf"
    echo "Conky stopped successfully."
else
    echo "Starting Conky..."
    
    # Check if conky config file exists
    if [ ! -f "$CONKY_CONFIG" ]; then
        echo "ERROR: Conky configuration file not found: $CONKY_CONFIG"
        echo "Please make sure cryptoConky.conf exists in the same directory as this script."
        exit 1
    fi
    
    # Check if conky is installed
    if ! command -v conky &> /dev/null; then
        echo "ERROR: Conky is not installed or not in PATH."
        echo "Please install Conky first:"
        echo "  Arch Linux: sudo pacman -S conky"
        echo "  Ubuntu/Debian: sudo apt install conky"
        exit 1
    fi
    
    # Start conky
    if conky -d -c "$CONKY_CONFIG"; then
        echo "Conky started successfully."
    else
        echo "ERROR: Failed to start Conky. Check the configuration file for syntax errors."
        exit 1
    fi
fi

