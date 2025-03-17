#!/bin/bash
if ! systemctl is-active monitoring-api.service > /dev/null; then
    sudo systemctl start monitoring-api.service
    echo "$(date): Restarted monitoring-api.service" >> /var/log/api_restart.log
fi