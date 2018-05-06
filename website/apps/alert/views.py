from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.contrib.auth import authenticate
from website.apps.alert.models import *
from website.apps.core.models import *
from django.http import HttpResponse


# View list of alerts
@login_required
def view_alerts(request, bid):
    #Business id required in base.html
    business = get_object_or_404(Business, id=bid)
    
    return render(request, 'alert/index.html', {'business' : business})

# Delete an alert/index
@login_required
def delete_alert(request, bid, slug):
    #Business id required in base.html
    business = get_object_or_404(Business, id=bid)
    
    alert = get_object_or_404(Alert, id=slug)
    alert.delete(keep_parents=True)
    
    return render(request, 'alert/index.html', {'business' : business})
    
# Mark an alert as read or unread
@login_required
def read_alert(request, bid, slug):
    #Business id required in base.html
    business = get_object_or_404(Business, id=bid)
    
    alert = get_object_or_404(Alert, id=slug)
    alert.read =  not alert.read
    alert.save()
    
    return render(request, 'alert/index.html', {'business' : business})