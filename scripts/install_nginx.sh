#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$SCRIPT_DIR/../logs"
LOG_FILE="$LOG_DIR/provisioning.log"

mkdir -p "$LOG_DIR"

echo "---- Nginx Installation Started ----" >> $LOG_FILE

if command -v ngnix &> /dev/null; then
    echo "Nginx already installed" >> $LOG_FILE
else
    echo "Installing Nginx" >> $LOG_FILE
    sudo apt update >> $LOG_FILE 2>&1
    sudo apt install -y nginx >> $LOG_FILE 2>&1

    if [ $? -eq 0]; then
        echo "Nginx installed successfully" >> $LOG_FILE
    else
        echo "ERROR: Installation failed" >> $LOG_FILE
        exit 1
    fi
fi
