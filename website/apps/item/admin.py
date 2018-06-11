from django.contrib import admin

from .models import *
#Don't these two ^v do the same thing?
from website.apps.item.models import *

admin.site.register(Inventory)
admin.site.register(Donation)
admin.site.register(Category)
admin.site.register(StoreLocation)
