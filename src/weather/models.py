from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Sensor(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

class Temperature(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=5, decimal_places=1)
    timestamp = models.DateTimeField(auto_now_add=True)

class Humidity(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=5, decimal_places=1)
    timestamp = models.DateTimeField(auto_now_add=True)
