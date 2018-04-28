"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from website.apps.core import views as core_views
from website.apps.profiles import views as profiles_views
from website.apps.item import views as item_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.index, name='home'),

    #Login, Signup, Profiles, etc.
    path('profile/', profiles_views.index, name='profile'),
    path('updateuser/', profiles_views.update_user, name='updateuser'),
    path('signup-customer/', profiles_views.signup_customer, name='signup_customer'),
    path('signup-owner/', profiles_views.signup_owner, name='signup_owner'),
    path('create-business/', core_views.create_business, name='create_business'),
    path('logout/', auth_views.logout, name='logout'),
    path('login/', auth_views.login, name='login'),

    #Viewing and editing Offers
    path('business/<int:bid>/inventory/', item_views.inventory, name='inventory'),
    path('business/<int:bid>/item/', item_views.newOffer, name='newOffer'),
    path('business/<int:bid>/item/edit/<slug:slug>/', item_views.editOffer, name='editOffer'),
    path('business/<int:bid>/item/delete/<slug:slug>/', item_views.deleteOffer, name='deleteOffer'),
    path('business/<int:bid>/item/showhide/<slug:slug>/', item_views.showHideOffer, name='showHideOffer'),
    path('business/<int:bid>/offers/', item_views.viewOffer, name='viewOffer'),

    #Viewing and editing Donations
    path('business/<int:bid>/newdonation/', item_views.newDonation, name='newDonation'),
    path('business/<int:bid>/donations/', item_views.allDonations, name='allDonations'),
    path('business/<int:bid>/donations/interested', item_views.interestedDonations, name='interestedDonations'),
    path('business/<int:bid>/donations/<slug:slug>/', item_views.oneDonation, name='oneDonation'),
    path('business/<int:bid>/donations/delete/<slug:slug>/', item_views.deleteDonation, name='deleteDonation'),
    path('business/<int:bid>/donations/<slug:slug>/receipt', item_views.receipt, name='donationReceipt'),

    #Categories
    path('business/<int:bid>/category-management/', item_views.manageCategories, name='manageCategories'),
    path('business/<int:bid>/categories/', item_views.allCategories, name='allCategories'),
    path('business/<int:bid>/category/<slug:slug>/', item_views.oneCategory, name='oneCategory'),

    #Requests (coming soon)
    path('request/', item_views.oneRequest, name="request" ),

    #View one specific business
    path('business/<int:bid>/', core_views.viewBusiness, name='viewBusiness'),
]
