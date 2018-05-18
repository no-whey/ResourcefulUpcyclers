from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import Group, User
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from website.apps.core.models import Business
from website.apps.item.models import Inventory
from website.apps.core.forms import CreateBusinessForm
from decouple import config

import string
import random
import datetime

#==============================
# Helper Fcns
#==============================
def unique_owner_key(key):
    all_businesses = Business.objects.all()
    for business in all_businesses:
        if key == business.owner_key:
            return False
    return True
#==============================



# Create your views here.
def index(request):
    business_list = Business.objects.all()
    return render(request, 'core/index.html', {'businesses' : business_list})

def viewBusiness(request, bid):
    business = get_object_or_404(Business, id=bid)
    owner_group = User.objects.filter(groups__name=business.name)
    offers_list = Inventory.objects.filter(private=False, business=business)[::-1][:3]
    route = render(request, 'profile/businessprofile.html', {'business' : business, 'owner_group' : owner_group, 'offers_list' : offers_list[0:4], 'user' : request.user })

    if request.POST and request.FILES:
        try:
            csv_file = request.FILES["csv_file"]
            if not csv_file.name.endswith('.csv'):
                messages.error(request,'File is not CSV type')
                return HttpResponseRedirect(route)
            #if file is too large, return
            if csv_file.multiple_chunks():
                messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
                return HttpResponseRedirect(route);
     
            file_data = csv_file.read().decode("utf-8")        
     
            lines = file_data.split("\r\n")

            Inventory.objects.filter(private=False, business=business).delete()
            #loop over the lines and save them in db. If error , store as string and then display
            first_line = True
            for line in lines:
            	if first_line:
            		first_line = False
            	else:                        
	                fields = line.split(",")
	                if len(fields) == 6:
		                item = Inventory()
		                item.name = fields[0]
		                item.quantity = fields[1]
		                item.price = fields[2]
		                item.location = fields[3]
		                item.text_description = fields[4]
		                item.img_link = fields[5]
		                item.date = datetime.date.today	
		                item.private = False
		                item.business = business
		                item.save()
 
        except Exception as e:
            logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
            messages.error(request,"Unable to upload file. "+repr(e))

    offers_list = Inventory.objects.filter(private=False, business=business)[::-1][:3]
    return render(request, 'profile/businessprofile.html', {'business' : business, 'owner_group' : owner_group, 'offers_list' : offers_list[0:4], 'user' : request.user })

def create_business(request):
    if request.method == 'POST':
        form = CreateBusinessForm(request.POST)
        if form.is_valid():
            business = Business()
            business.name = form.cleaned_data.get('name')
            business.description = form.cleaned_data.get('description')
            business.address = form.cleaned_data.get('address')
            if form.cleaned_data.get('icon'):
                business.icon = form.cleaned_data.get('icon')
            o_group = Group(name=business.name)
            o_group.save()
            business.owner_group = Group.objects.get(id=o_group.id)
            #business.owner_group.save()

            # I STILL NEED TO RANDOM GENERATE AN OWNER KEY BELOW
            alph_nums = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
            key = ''.join(random.choice(alph_nums) for _ in range(32))
            while(not unique_owner_key(key)):
                key = ''.join(random.choice(alph_nums) for _ in range(32))
            business.owner_key = key
            business.save()
            request.user.groups.add(business.owner_group)
            request.user.profile.isOwner = True
            request.user.profile.business = Business.objects.get(id=business.id)
            request.user.profile.save()

            return render(request, 'profile/businessprofile.html', {'business' : business})

    else:
        form = CreateBusinessForm()
    return render(request, 'registration/create_business.html', {'form': form})
"""
def logout_user(request):
    logout(request)
    return render(request, 'profile/logout.html')
"""
