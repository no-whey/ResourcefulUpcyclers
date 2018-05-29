from django.contrib import admin

from .models import *
from website.apps.core.models import Business
# Register your models here.

admin.site.register(Business)
