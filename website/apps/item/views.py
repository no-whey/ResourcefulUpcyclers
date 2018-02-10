from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from website.apps.item.models import Donation
from website.apps.item.models import Offer

from .forms import DonationForm
from .forms import OfferForm

@login_required
def index(request):
    if(request.user.profile.isOwner):
        return render(request, 'donations/owner_index.html')
    else:
        return render(request, 'donations/customer_index.html')

def inventory(request):
    return render(request, 'inventory/index.html')
    
def newOffer(request):
    if request.method == 'POST':
        form = newOffer(request.POST)
        if form.is_valid():
            # Applies Offer fields
            offer = form.save()
            offer.refresh_from_db()
            
            #Set Field values
            offer.name = form.cleaned_data.get('name')
            offer.price = form.cleaned_data.get('price')
            offer.location = form.cleaned_data.get('location')
            offer.text_description = form.cleaned_data.get('text_description')
            offer.img_link = form.cleaned_data.get('img_link')
            
            # Redirect to inventory, new offer created
            login(request, user)
            return redirect('inventory')
    else:
        form = OfferForm()
    return render(request, 'inventory/index.html', {'form': form})
    