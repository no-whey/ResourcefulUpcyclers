from django.db import models
from model_utils import Choices
from model_utils.fields import StatusField
from django.contrib.auth.models import User

from website.apps.profiles.models import Profile


# Generic alert model
class Alert(models.Model):
    STATUS_OPTIONS = Choices('unread', 'read')
    
    status = StatusField(choices_name='STATUS_OPTIONS', default='unread')
    title = models.TextField(max_length = 200, blank = True, default='', null=True)
    message = models.TextField(max_length = 200, blank = True, default='', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
