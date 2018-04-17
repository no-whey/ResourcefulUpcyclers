from django.db import models
from django.contrib.auth.models import User
from model_utils import Choices
from model_utils.fields import StatusField


# Generic alert model
class Alert(models.Model):
    STATUS_OPTIONS = Choices('unread', 'read')
    
    status = StatusField(choices_name='STATUS_OPTIONS', default='unread')
    message = models.TextField(max_length = 200, blank = True, default='', null=True)
    user = models.ForeignKey(User, related_name='alert_user', on_delete=models.CASCADE)
    
