#!/bin/bash

# Script to read metrics from named pipe and log them
LOG_FILE="/tmp/metrics_log.txt"

echo "Starting metrics logging..." | tee -a $LOG_FILE
while true; do
    if read line < /tmp/metrics_pipe; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') - $line" | tee -a $LOG_FILE
    fi
done
