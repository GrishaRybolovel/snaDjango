from django.db import models

# Create your models here.


class PerformanceData(models.Model):
    packet_loss = models.FloatField()
    latency = models.FloatField()
    bandwidth_utilization = models.FloatField()
    download_speed = models.FloatField()
    upload_speed = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Performance Data ({self.created_at})'

    class Meta:
        verbose_name = 'Производительность'
        verbose_name_plural = 'Производительность'