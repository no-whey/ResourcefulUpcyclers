from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.contrib.auth import authenticate
from website.apps.item.models import *
from django.http import HttpResponse


# Owners can view their available inventory
@login_required
def view_alerts(request, bid):
    #Business id required for base.html
    business = get_object_or_404(Business, id=bid)
    
    return render(request, 'alert/index.html', {'business' : business})
    