from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.contrib.auth import authenticate
from website.apps.alert.models import *
from django.http import HttpResponse

@login_required
def getAlerts():
    alert_list = Alert.objects.all()
    return {'alerts' : alert_list}