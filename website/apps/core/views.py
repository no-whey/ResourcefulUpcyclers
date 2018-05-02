from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import Group, User
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from website.apps.core.models import Business
from website.apps.item.models import Inventory
from website.apps.core.forms import CreateBusinessForm
from decouple import config

import string
import random

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
    offers_list = Inventory.objects.filter(private=False, business=business)
    return render(request, 'profile/businessprofile.html', {'business' : business, 'owner_group' : owner_group, 'offers_list' : offers_list })

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
