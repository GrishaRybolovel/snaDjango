import requests
import json
from django.shortcuts import render
import subprocess
import speedtest
import requests


def calculate_performance(request):
    if request.method == 'POST':
        ip_address = request.POST.get('ip_address')
        packet_loss_threshold = request.POST.get('packet_loss_threshold')
        latency_threshold = request.POST.get('latency_threshold')
        bandwidth_utilization_threshold = request.POST.get('bandwidth_utilization_threshold')

        if ip_address and packet_loss_threshold and latency_threshold and bandwidth_utilization_threshold:
            packet_loss_threshold = float(packet_loss_threshold)
            latency_threshold = float(latency_threshold)
            bandwidth_utilization_threshold = float(bandwidth_utilization_threshold)

            packet_loss = check_packet_loss(ip_address)
            packet_loss_status = "Passed" if packet_loss is not None and packet_loss <= packet_loss_threshold else "Failed"

            latency = check_latency(ip_address)
            latency_status = "Passed" if latency is not None and latency <= latency_threshold else "Failed"
            latency = int(latency) if latency is not None else latency

            bandwidth_utilization = check_bandwidth_utilization(ip_address)
            bandwidth_utilization_status = "Passed" if bandwidth_utilization is not None and bandwidth_utilization <= bandwidth_utilization_threshold else "Failed"
            bandwidth_utilization = int(bandwidth_utilization) if bandwidth_utilization is not None \
                else bandwidth_utilization

            download_speed, upload_speed, network_speed = check_network_speed()
            network_speed_status = "Passed" if network_speed is not None and network_speed == "High" else "Failed"
            download_speed = int(download_speed)
            upload_speed = int(upload_speed)

            network_security = check_network_security(ip_address)
            network_security_status = "Passed" if network_security is not None else "Failed"

            context = {
                'ip_address': ip_address,
                'packet_loss': packet_loss,
                'packet_loss_status': packet_loss_status,
                'latency': latency,
                'latency_status': latency_status,
                'bandwidth_utilization': bandwidth_utilization,
                'bandwidth_utilization_status': bandwidth_utilization_status,
                'download_speed': download_speed,
                'upload_speed': upload_speed,
                'network_speed': network_speed,
                'network_speed_status': network_speed_status,
                'network_security_status': network_security_status
            }
            print(ip_address, packet_loss, latency, bandwidth_utilization, network_speed, network_security_status)
            return render(request, 'calculate_performance.html', context=context)

    return render(request, 'calculate_performance.html')



def check_packet_loss(ip_address):
    # Используем утилиту ping для проверки потери пакетов
    # Опция -c указывает количество пакетов для отправки
    # Опция -W указывает время ожидания ответа в секундах
    command = ['ping', '-c', '5', '-W', '1', ip_address]
    try:
        output = subprocess.check_output(command)
        output = output.decode('utf-8')
        packet_loss = float(output.split('packet loss')[0].split(',')[-1].strip().replace('%', ''))
        return packet_loss
    except subprocess.CalledProcessError:
        return 100.0


def check_latency(ip_address):
    # Используем утилиту ping для измерения задержки (latency)
    # Опция -c указывает количество пакетов для отправки
    # Опция -W указывает время ожидания ответа в секундах
    command = ['ping', '-c', '5', '-W', '1', ip_address]
    try:
        output = subprocess.check_output(command)
        output = output.decode('utf-8')
        latency = float(output.split('/stddev = ')[1].split('/')[1])
        return latency
    except subprocess.CalledProcessError:
        return float('inf')


def check_bandwidth_utilization(ip_address):
    # Реализация проверки использования пропускной способности сети
    # на основе запросов к удаленному серверу или собственным методам измерения
    try:
        # Выполните запрос к удаленному серверу и измерьте время ответа
        response = requests.get('http://' + ip_address)
        response_time = response.elapsed.total_seconds() * 1000  # В миллисекундах

        # Рассчитайте использование пропускной способности на основе времени ответа
        bandwidth_utilization = response_time  # Примерная оценка, адаптируйте к вашим требованиям

        return bandwidth_utilization
    except requests.RequestException:
        return None


def check_network_speed():
    # Реализация проверки скорости сети с использованием библиотеки Speedtest-cli
    try:
        st = speedtest.Speedtest()
        download_speed = st.download() / 10 ** 6  # Скорость загрузки в Мбит/с
        upload_speed = st.upload() / 10 ** 6  # Скорость отдачи в Мбит/с

        # Определите условия для определения высокой скорости сети
        if download_speed >= 20 and upload_speed >= 50:
            network_speed = "High"
        else:
            network_speed = "Low"

        return download_speed, upload_speed, network_speed
    except speedtest.SpeedtestException:
        return None


def check_network_security(ip_address):
    # Реализация проверки безопасности сети на основе системных утилит,
    # анализа журналов или других методов, адаптированных к вашим требованиям
    # ...

    # Пример: Проверка доступности удаленного хоста по IP-адресу
    try:
        response = requests.get('http://' + ip_address)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.RequestException:
        return False
