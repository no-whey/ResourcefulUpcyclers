from django.shortcuts import render, redirect, render_to_response, get_object_or_404
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
        if request.method == 'POST':
            form = DonationForm(request.POST)
            if form.is_valid():
                # Applies Offer fields
                #offer = form.save()
                donation = Donation()
                donation.save()
                donation.refresh_from_db()
            
                donation.name = form.cleaned_data.get('name')
                donation.donor_email = form.cleaned_data.get('donor_email')
                donation.city = form.cleaned_data.get('city')
                donation.text_description = form.cleaned_data.get('text_description')
                donation.img_link = form.cleaned_data.get('img_link')
            
            
                donation.save()
            
                # Redirect to Home, Maybe a "Thank you" page???
                return redirect('home')
        else:
            form = DonationForm()
        return render(request, 'donations/customer_index.html', {'form': form})

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
    

def viewOffer(request):
    offers = Offer.objects.all()
    # offers = Offer.objects.all().filter(private = false)  

    return render(request, 'inventory/viewOffer.html', {'offers_list' : offers})
    