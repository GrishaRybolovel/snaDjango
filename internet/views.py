import re

from django.shortcuts import render
# from .models import PerformanceData
import subprocess
import speedtest


# Create your views here.
def calculate_performance(request):
    # Perform network performance calculations
    packet_loss, latency, bandwidth_utilization, network_speed = perform_calculations()

    return render(request, 'calculate_performance.html', {
        'packet_loss': packet_loss,
        'latency': latency,
        'bandwidth_utilization': bandwidth_utilization,
        'network_speed': network_speed
    })

def perform_calculations():
    # Calculate packet loss
    packet_loss_result = subprocess.run(['ping', '-c', '10', 'example.com'], stdout=subprocess.PIPE)
    packet_loss_output = packet_loss_result.stdout.decode()
    packet_loss = parse_packet_loss(packet_loss_output)

    # Calculate latency
    latency_result = subprocess.run(['ping', '-c', '10', '-i', '0.2', 'example.com'], stdout=subprocess.PIPE)
    latency_output = latency_result.stdout.decode()
    latency = parse_latency(latency_output)

    # Calculate bandwidth utilization
    bandwidth_utilization = calculate_bandwidth_utilization()

    # Calculate network speed
    network_speed = calculate_network_speed()

    return packet_loss, latency, bandwidth_utilization, network_speed

def parse_packet_loss(output):
    match = re.search(r'(\d+)% packet loss', output)
    if match:
        return float(match.group(1))
    return 0.0

def parse_latency(output):
    match = re.search(r'rtt min/avg/max/mdev = (\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+) ms', output)
    if match:
        return float(match.group(2))
    return 0.0

def calculate_bandwidth_utilization():
    # Implement your logic to calculate bandwidth utilization
    return 0.0

def calculate_network_speed():
    st = speedtest.Speedtest()
    download_speed = st.download() / 1024 / 1024  # Convert to Mbps
    upload_speed = st.upload() / 1024 / 1024  # Convert to Mbps
    return f"{download_speed:.2f} Mbps (Download), {upload_speed:.2f} Mbps (Upload)"
