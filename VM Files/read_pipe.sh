#!/bin/bash
while true; do
    if read line < /tmp/api_log_pipe; then
        echo "$line" >> /var/log/api_requests.log
    fi
done