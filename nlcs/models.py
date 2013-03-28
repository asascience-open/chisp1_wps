from django.db import models

# Create your models here.

class Lake(models.Model):
    name = models.CharField("name of the great lake", max_length=30, unique=True)
    def __unicode__(self):
        return self.name
    def get_stations(self, parameter, date):
        if parameter.lower() == "nitrogen":
            filt_tribs = self.tributary_set.filter(has_nitrogen=True)
        elif parameter.lower() == "phosphorus":
            filt_tribs = self.tributary_set.filter(has_phosphorus=True)
        filt_tribs = filt_tribs.filter(has_stream=True)
        return filt_tribs

class Tributary(models.Model):
    lake = models.ForeignKey(Lake, verbose_name="the lake that this tributary drains into")
    country = models.CharField(max_length=3)
    name = models.CharField(max_length=100, unique=True)
    has_phosphorus = models.BooleanField()
    has_nitrogen = models.BooleanField()
    has_stream = models.BooleanField()
    def __unicode__(self):
        return self.name
    
class WaterQuality(models.Model):
    tributary = models.ForeignKey(Tributary, verbose_name="the river that this water quality station is on")
    sos_endpoint = models.CharField(max_length=300)
    name = models.CharField(max_length=100)
    startdate = models.DateField()
    enddate = models.DateField()
    station = models.CharField(max_length=100)
    has_phosphorus = models.BooleanField()
    has_nitrogen = models.BooleanField()
    def __unicode__(self):
        return self.station
    
class StreamGauge(models.Model):
    tributary = models.ForeignKey(Tributary, verbose_name="the river that this stream gauge is on")
    sos_endpoint = models.CharField(max_length=300)
    name = models.CharField(max_length=100)
    startdate = models.DateField()
    enddate = models.DateField()
    latitude = models.DecimalField(help_text="Latitude or Y coordinate", blank=True, max_digits=20, decimal_places=8)
    longitude = models.DecimalField(help_text="Longitude or X coordinate", blank=True, max_digits=20, decimal_places=8)
    station = models.CharField(max_length=100)
    def __unicode__(self):
        return self.station
