from django.db import models
from django.contrib.auth.models import User, Group

class Business(models.Model):
    name = models.TextField(max_length=50, blank=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    address = models.TextField(max_length=200, blank=True)
    icon = models.ImageField(blank=True)
    owner_group = models.ForeignKey(Group, related_name="owners", on_delete=models.CASCADE)
    owner_key = models.TextField(max_length=50, default="change_this_key")
