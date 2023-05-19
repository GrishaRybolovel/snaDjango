document.getElementById('performanceForm').addEventListener('submit', function(event) {
    event.preventDefault();

    var packetLossThreshold = parseFloat(document.getElementById('packetLossThreshold').value);
    var latencyThreshold = parseFloat(document.getElementById('latencyThreshold').value);
    var bandwidthUtilizationThreshold = parseFloat(document.getElementById('bandwidthUtilizationThreshold').value);
    var ipAddress = document.getElementById('ipAddress').value;

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/performance/calculate/', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    var data = {
        'packet_loss_threshold': packetLossThreshold,
        'latency_threshold': latencyThreshold,
        'bandwidth_utilization_threshold': bandwidthUtilizationThreshold,
        'ip_address': ipAddress
    };

    xhr.send(JSON.stringify(data));
});
