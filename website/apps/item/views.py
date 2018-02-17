from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from website.apps.item.models import Donation
from website.apps.item.models import Inventory

from .forms import DonationForm
from .forms import OfferForm

@login_required
def newDonation(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            # Applies Offer fields
            #offer = form.save()
            donation = Donation()
            donation.donor = request.user
            donation.save()
            donation.refresh_from_db()

            donation.name = form.cleaned_data.get('name')
            donation.donor_email = form.cleaned_data.get('donor_email')
            donation.city = form.cleaned_data.get('city')
            donation.text_description = form.cleaned_data.get('text_description')
            donation.img_link = form.cleaned_data.get('img_link')


            donation.save()

            # Redirect to Home, Maybe a "Thank you" page???
            return redirect('allDonations')
    else:
        form = DonationForm()
    return render(request, 'donations/newDonation.html', {'form': form})

@login_required
def allDonations(request):
    if(request.user.profile.isOwner):
        donation_list = Donation.objects.all()
        return render(request, 'donations/allDonations.html', {'donations' : donation_list})
    else:
        donation_list = Donation.get_my_donations(request.user)
        print(donation_list)
        return render(request, 'donations/allDonations.html', {'donations' : donation_list})

@login_required
def inventory(request):
    if(request.user.profile.isOwner):
        inventory_list = Inventory.objects.all()
        return render(request, 'inventory/index.html', {'inventory' : inventory_list})
    else:
        return render(request, 'index.html')


@login_required
def newOffer(request):
    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            # Applies Offer fields
            #offer = form.save()
            offer = Inventory()
            offer.save()
            offer.refresh_from_db()

            offer.name = form.cleaned_data.get('name')
            offer.price = form.cleaned_data.get('price')
            offer.location = form.cleaned_data.get('location')
            offer.text_description = form.cleaned_data.get('text_description')


            offer.img_link = form.cleaned_data.get('img_link')
            #temp_img = form.cleaned_data.get('img_link')
            #(width, height)  = temp_img.size

            #temp_img.resize( (width/(width/200), height/(width/200)), Image.ANTIALIAS )
            #offer.img_link = temp_img


            offer.save()

            # Redirect to inventory, new offer created
            return redirect('inventory')
    else:
        form = OfferForm()
    return render(request, 'inventory/newOffer.html', {'form': form})


def viewOffer(request):
    offers = Inventory.objects.all()
    # offers = Offer.objects.all().filter(private = false)

    return render(request, 'inventory/viewOffer.html', {'offers_list' : offers})
