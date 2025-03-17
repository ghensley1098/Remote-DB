#!/bin/bash
echo "Starting stress test..."

# CPU stress for 2 minutes
echo "Stressing CPU..."
stress-ng --cpu 2 --timeout 120s

# Memory stress for 1 minute
echo "Stressing Memory..."
stress-ng --vm 2 --vm-bytes 512M --timeout 60s

# I/O stress for 1.5 minutes
echo "Stressing I/O..."
stress-ng --iomix 2 --timeout 90s

# Filesystem stress for 1 minute
echo "Stressing Filesystem..."
stress-ng --hdd 2 --hdd-bytes 1G --timeout 60s

# Network stress for 1 minute (optional, requires network stressor setup)
echo "Stressing Network..."
stress-ng --udp 2 --timeout 60s

echo "Stress test complete"