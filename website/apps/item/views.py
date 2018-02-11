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

@login_required    
def inventory(request):
    if(request.user.profile.isOwner):
        return render(request, 'inventory/index.html')
    else:
        return render(request, 'index.html')
    

@login_required    
def newOffer(request):
    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            # Applies Offer fields
            #offer = form.save()
            offer = Offer()
            offer.save()
            offer.refresh_from_db()
            
            offer.name = form.cleaned_data.get('name')
            offer.price = form.cleaned_data.get('price')
            offer.location = form.cleaned_data.get('location')
            offer.text_description = form.cleaned_data.get('text_description')
            offer.img_link = form.cleaned_data.get('img_link')
            
            
            offer.save()
            
            # Redirect to inventory, new offer created
            return redirect('inventory')
    else:
        form = OfferForm()
    return render(request, 'inventory/newOffer.html', {'form': form})
    