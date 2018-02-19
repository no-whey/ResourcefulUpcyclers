from django.contrib import admin

from .models import *
#Don't these two ^v do the same thing?
from website.apps.item.models import Inventory
from website.apps.item.models import Donation

admin.site.register(Inventory)
admin.site.register(Donation)