from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Donation(models.Model):

    name = models.TextField(max_length=30, blank=True)
    text_description = models.TextField(max_length=500, blank=True)
    img_link = models.URLField(max_length=200, blank=True)
    city = models.TextField(max_length=30, blank=True)
    donor_email = models.EmailField(max_length=255)
    archived = models.BooleanField(default=False)

class Offer(models.Model):
        
    name = models.TextField(max_length=30, blank=True)
    price = models.TextField(max_length=30, blank=True)
    location = models.TextField(max_length=60, blank=True)
    text_description = models.TextField(max_length=500, blank=True)
    img_link = models.URLField(max_length=200, blank=True)
    #private = models.BooleanField(blank=True)
    