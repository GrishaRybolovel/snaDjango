import requests
import json
from django.shortcuts import render
import subprocess
import speedtest
import requests
from .models import PerformanceData


def calculate_performance(request):
    if request.method == 'POST':
        ip_address = request.POST.get('ip_address')

        if ip_address:

            packet_loss = check_packet_loss(ip_address)

            latency = check_latency(ip_address)
            latency = int(latency) if latency != float('inf') else latency

            bandwidth_utilization = check_bandwidth_utilization(ip_address)
            bandwidth_utilization = int(bandwidth_utilization) if bandwidth_utilization is not None \
                else bandwidth_utilization

            download_speed, upload_speed, network_speed = check_network_speed()
            download_speed = int(download_speed)
            upload_speed = int(upload_speed)

            network_security = check_network_security(ip_address)

            cnt = 0
            average_Loss = 0
            average_Latency = 0
            average_Bandwidth = 0
            average_DSpeed = 0
            average_USpeed = 0

            if bandwidth_utilization is not None:
                PerformanceData.objects.create(
                    packet_loss=packet_loss,
                    latency=latency,
                    bandwidth_utilization=bandwidth_utilization,
                    download_speed=download_speed,
                    upload_speed=upload_speed
                )

            upload_speeds = []
            download_speeds = []

            for objects in PerformanceData.objects.all():
                upload_speeds.append(objects.upload_speed)
                download_speeds.append(objects.download_speed)
                average_Loss += objects.packet_loss
                average_Latency += objects.latency if objects.latency != float('inf') else 1000
                average_Bandwidth += objects.bandwidth_utilization \
                    if objects.bandwidth_utilization is not None else 1000
                average_DSpeed += objects.download_speed
                average_USpeed += objects.upload_speed
                cnt += 1
            upload_speeds.append(upload_speed)
            download_speeds.append(download_speed)
            upload_speeds = list(sorted(upload_speeds))
            download_speeds = list(sorted(download_speeds))

            place = str(int(int((upload_speeds.index(upload_speed) + download_speeds.index(download_speed)) / 2) / cnt * 100))

            print(f"Average loss: {average_Loss / cnt}",
                  f"Average latency: {average_Latency / cnt}",
                  f"Average bandwidth: {average_Bandwidth}",
                  f"Average download speed: {average_DSpeed}",
                  f"Average upload speed: {average_USpeed}",
                  sep="\n")

            context = {
                'ip_address': ip_address,
                'packet_loss': packet_loss,
                'latency': latency,
                'bandwidth_utilization': bandwidth_utilization,
                'download_speed': download_speed,
                'upload_speed': upload_speed,
                'network_speed': network_speed,
                'average_Loss': str(int(average_Loss / cnt)),
                'average_Latency': str(int(average_Latency / cnt)),
                'average_Bandwidth': str(int(average_Bandwidth / cnt)),
                'average_DSpeed': str(int(average_DSpeed / cnt)),
                'average_USpeed': str(int(average_USpeed / cnt)),
                'place' : place,
            }
            return render(request, 'results.html', context=context)

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
