from __future__ import unicode_literals
from django.db import models
from django.contrib import auth


class UserSettings(models.Model):
    user=models.OneToOneField('auth.User',verbose_name='User')
    google_email=models.EmailField(verbose_name='your google email')
    google_password=models.CharField(verbose_name='your password',max_length=100)
    location_lon=models.DecimalField(verbose_name='your current longitude',
                                    max_digits=8, 
                                    decimal_places=6,
                                    default=59.333409)
    location_lat=models.DecimalField(verbose_name='your current latitude',
                                    max_digits=8, 
                                    decimal_places=6,
                                    default=18.045008)
    gmapkey=models.CharField(verbose_name='google api key',max_length=100)

    def __str__(self):
        return "settings for user {}". format(self.user.id)

    class Meta:
        verbose_name = 'Setting'
        verbose_name_plural = 'Settings'