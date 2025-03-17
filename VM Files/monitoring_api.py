from flask import Flask, jsonify
import psutil
import os

app = Flask(__name__)

def get_metrics():
    # CPU usage
    cpu_usage = psutil.cpu_percent(interval=1)

    # Memory usage
    memory = psutil.virtual_memory()
    memory_usage = memory.percent

    # Disk usage
    disk = psutil.disk_usage('/')
    disk_usage = disk.percent

    # Network I/O
    network = psutil.net_io_counters()
    network_bytes_sent = network.bytes_sent
    network_bytes_recv = network.bytes_recv

    # Process count
    process_count = len(psutil.pids())

    return {
        "cpu_usage": cpu_usage,
        "memory_usage": memory_usage,
        "disk_usage": disk_usage,
        "network_bytes_sent": network_bytes_sent,
        "network_bytes_recv": network_bytes_recv,
        "process_count": process_count
    }

@app.route('/metrics', methods=['GET'])
def metrics():
    return jsonify(get_metrics())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)