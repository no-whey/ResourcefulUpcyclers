from django.db import models
from django.contrib.auth.models import User, Group

class Business(models.Model):
    name = models.TextField(max_length=50, blank=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    owner_group = models.ForeignKey(Group, related_name="owners")
    address = models.TextField(max_length=100, blank=True)
    #donations =
    #inventory =
    icon = models.ImageField()
