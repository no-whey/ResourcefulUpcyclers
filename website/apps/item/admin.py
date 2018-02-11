from django.contrib import admin

from .models import *

from website.apps.item.models import Offer
    
admin.site.register(Offer)