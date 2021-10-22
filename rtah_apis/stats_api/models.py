from django.db import models
from django.utils import timezone

class Person(models.Model):
    first_name          = models.CharField(max_length=100, blank=False)
    last_name           = models.CharField(max_length=100, blank=False)
    join_date           = models.DateTimeField(default=timezone.now)
    email               = models.EmailField(max_length=100, blank=False)
    profile_img         = models.ImageField(upload_to='static/images/%Y/%m/%d', blank=True, null=True)

    def __str__(self):
        return "{} {} ({})".format(self.first_name, self.last_name, self.id)

    def fullname(self):
        return "{} {}".format(self.first_name, self.last_name)

class Hike(models.Model):
    hiker               = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='hikes')
    hike_date           = models.DateField(max_length=100, blank=False)
    location            = models.CharField(max_length=100, blank=False)
    state               = models.CharField(max_length=30, blank=False)
    distance_mi         = models.FloatField(blank=False)
    elevation_gain_ft   = models.IntegerField(blank=False)
    highest_elev_ft     = models.IntegerField(blank=True, null=True)
    alltrails_url       = models.URLField(max_length=100, blank=True, null=True)
    blogger_url         = models.URLField(max_length=100, blank=True, null=True)

    def __str__(self):
        return "{}: {}, {} ({})".format(self.id, self.hike_date, self.location, self.hiker.fullname())
