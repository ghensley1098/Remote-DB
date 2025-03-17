import dash
from dash import dcc, html
import plotly.graph_objs as go
import requests
from dash.dependencies import Input, Output
import time

app = dash.Dash(__name__)

# Thresholds for notifications (user-adjustable)
thresholds = {
    "cpu_usage": 80.0,
    "memory_usage": 80.0,
    "disk_usage": 80.0
}

# Store historical data
history = {
    "times": [],
    "cpu_usage": [],
    "memory_usage": [],
    "disk_usage": [],
    "network_bytes_sent": [],
    "network_bytes_recv": [],
    "process_count": []
}

# Store last valid graph figures to handle intermittent failures
last_figures = {
    "cpu_fig": go.Figure(),
    "memory_fig": go.Figure(),
    "disk_fig": go.Figure(),
    "network_fig": go.Figure(),
    "process_fig": go.Figure()
}

def fetch_metrics():
    try:
        response = requests.get("http://34.130.140.20:5000/metrics", timeout=10)
        metrics = response.json()
        print(f"Fetched metrics: {metrics}")  # Debug output
        return metrics
    except Exception as e:
        print(f"Error fetching metrics: {e}")
        return {}

app.layout = html.Div([
    html.H1("Server Performance Dashboard"),
    html.Div(id="notification", style={"color": "red"}),
    dcc.Graph(id="cpu-graph"),
    dcc.Graph(id="memory-graph"),
    dcc.Graph(id="disk-graph"),
    dcc.Graph(id="network-graph"),
    dcc.Graph(id="process-graph"),
    dcc.Interval(id="interval-component", interval=5*1000, n_intervals=0)
])

@app.callback(
    [Output("cpu-graph", "figure"),
     Output("memory-graph", "figure"),
     Output("disk-graph", "figure"),
     Output("network-graph", "figure"),
     Output("process-graph", "figure"),
     Output("notification", "children")],
    [Input("interval-component", "n_intervals")]
)
def update_graphs(n):
    global last_figures  # Use global to persist last valid figures
    metrics = fetch_metrics()
    if not metrics:
        print("No metrics fetched, returning last valid graphs")  # Debug output
        return [last_figures["cpu_fig"], last_figures["memory_fig"], last_figures["disk_fig"],
                last_figures["network_fig"], last_figures["process_fig"], "Error: Unable to fetch metrics"]

    # Append to historical data
    current_time = time.ctime()
    history["times"].append(current_time)
    history["cpu_usage"].append(metrics["cpu_usage"])
    history["memory_usage"].append(metrics["memory_usage"])
    history["disk_usage"].append(metrics["disk_usage"])
    history["network_bytes_sent"].append(metrics["network_bytes_sent"])
    history["network_bytes_recv"].append(metrics["network_bytes_recv"])
    history["process_count"].append(metrics["process_count"])

    # Limit history to last 100 data points (optional, to prevent memory issues)
    if len(history["times"]) > 100:
        for key in history:
            history[key] = history[key][-100:]

    print(f"History data: {history}")  # Debug output

    # CPU Usage
    cpu_fig = go.Figure()
    cpu_fig.add_trace(go.Scatter(x=history["times"], y=history["cpu_usage"], mode="lines+markers", name="CPU Usage"))
    cpu_fig.update_layout(title="CPU Usage (%)", yaxis_range=[0, 100])

    # Memory Usage
    memory_fig = go.Figure()
    memory_fig.add_trace(go.Scatter(x=history["times"], y=history["memory_usage"], mode="lines+markers", name="Memory Usage"))
    memory_fig.update_layout(title="Memory Usage (%)", yaxis_range=[0, 100])

    # Disk Usage
    disk_fig = go.Figure()
    disk_fig.add_trace(go.Scatter(x=history["times"], y=history["disk_usage"], mode="lines+markers", name="Disk Usage"))
    disk_fig.update_layout(title="Disk Usage (%)", yaxis_range=[0, 100])

    # Network I/O
    network_fig = go.Figure()
    network_fig.add_trace(go.Scatter(x=history["times"], y=history["network_bytes_sent"], mode="lines+markers", name="Bytes Sent"))
    network_fig.add_trace(go.Scatter(x=history["times"], y=history["network_bytes_recv"], mode="lines+markers", name="Bytes Received"))
    network_fig.update_layout(title="Network I/O (Bytes)")

    # Process Count
    process_fig = go.Figure()
    process_fig.add_trace(go.Scatter(x=history["times"], y=history["process_count"], mode="lines+markers", name="Process Count"))
    process_fig.update_layout(title="Process Count")

    # Store last valid figures
    last_figures["cpu_fig"] = cpu_fig
    last_figures["memory_fig"] = memory_fig
    last_figures["disk_fig"] = disk_fig
    last_figures["network_fig"] = network_fig
    last_figures["process_fig"] = process_fig

    # Notification system
    notification = ""
    if metrics["cpu_usage"] > thresholds["cpu_usage"]:
        notification += f"Warning: CPU usage ({metrics['cpu_usage']}%) exceeds threshold ({thresholds['cpu_usage']}%)!\n"
    if metrics["memory_usage"] > thresholds["memory_usage"]:
        notification += f"Warning: Memory usage ({metrics['memory_usage']}%) exceeds threshold ({thresholds['memory_usage']}%)!\n"
    if metrics["disk_usage"] > thresholds["disk_usage"]:
        notification += f"Warning: Disk usage ({metrics['disk_usage']}%) exceeds threshold ({thresholds['disk_usage']}%)!\n"

    return cpu_fig, memory_fig, disk_fig, network_fig, process_fig, notification

if __name__ == "__main__":
    app.run_server(debug=True)