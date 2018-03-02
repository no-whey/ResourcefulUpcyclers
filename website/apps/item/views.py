from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.contrib.auth import authenticate
from website.apps.item.models import Donation
from website.apps.item.models import Inventory
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse

from .forms import DonationForm, UpdateDonationForm, OfferForm, UpdateOfferForm

# For customers to create a new donation ticket
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
            donation.quantity = form.cleaned_data.get('quantity')
            donation.img_link = form.cleaned_data.get('img_link')
            donation.needs_pickup = form.cleaned_data.get('needs_pickup')

            donation.save()

            # Redirect to all Donations from that user, Maybe a "Thank you" page???
            return redirect('allDonations')
    else:
        form = DonationForm()
    return render(request, 'donations/newDonation.html', {'form': form})

# For Customers to view their submitted Donations, Owners can see all donations
@login_required
def allDonations(request):
    if(request.user.profile.isOwner):
        donation_list = Donation.objects.all()
        return render(request, 'donations/allDonations.html', {'donations' : donation_list})
    else:
        donation_list = Donation.get_my_donations(request.user)
        return render(request, 'donations/allDonations.html', {'donations' : donation_list})

# Owners see only their interested Donations, customers get same access as allDonations view
@login_required
def interestedDonations(request):
    if(request.user.profile.isOwner):
        donation_list = []
        for donation in Donation.objects.all():
            if donation.owner_interest:
                donation_list.append(donation)
        return render(request, 'donations/allDonations.html', {'donations' : donation_list})
    else:
        donation_list = Donation.get_my_donations(request.user)
        return render(request, 'donations/allDonations.html', {'donations' : donation_list})

# For Owners to view and edit one specific donation
@login_required
def oneDonation(request, slug):
    if(request.user.profile.isOwner):
        donation = get_object_or_404(Donation, id=slug)
        if request.method == 'POST':
            form = UpdateDonationForm(request.POST)
            if form.is_valid():
                donation.refresh_from_db()

                donation.name = form.cleaned_data.get('name')
                donation.donor_email = form.cleaned_data.get('donor_email')
                donation.city = form.cleaned_data.get('city')
                donation.text_description = form.cleaned_data.get('text_description')
                donation.quantity = form.cleaned_data.get('quantity')
                donation.img_link = form.cleaned_data.get('img_link')
                donation.needs_pickup = form.cleaned_data.get('needs_pickup')
                donation.status = form.cleaned_data.get('status')
                donation.owner_interest = form.cleaned_data.get('owner_interest')

                donation.save()

                # Redirect to Home, Maybe a "Thank you" page???
                return redirect('allDonations')
        else:
            form = UpdateDonationForm(instance=donation)
        return render(request, 'donations/oneDonation.html', {'form' : form, 'donation' : donation})
    else:
        return render(request, 'donations/allDonations.html')

# Owners can delete a donation
@login_required
def deleteDonation(request, slug):
    if(request.user.profile.isOwner):
        donation = get_object_or_404(Donation, id=slug)
        if request.method == 'POST':
            donation.delete(keep_parents=True)
            return redirect('allDonations')
        else:
            return render(request, 'donations/deleteDonation.html', {'donation' : donation})
    else:
        return redirect('allDonations')

# Owners can view their available inventory
@login_required
def inventory(request):
    if(request.user.profile.isOwner):
        inventory_list = Inventory.objects.all()
        return render(request, 'inventory/index.html', {'inventory' : inventory_list})
    else:
        return render(request, 'index.html')

# Owners can create new offers
@login_required
def newOffer(request):
    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            offer = form.save()
            #offer.save()
            #offer.refresh_from_db()

            #offer.name = form.cleaned_data.get('name')
            #offer.quantity = form.cleaned_data.get('quantity')
            #offer.price = form.cleaned_data.get('price')
            #offer.location = form.cleaned_data.get('location')
            #offer.text_description = form.cleaned_data.get('text_description')
            #offer.img_link = form.cleaned_data.get('img_link')
            #offer.private = form.cleaned_data.get('private')
            #temp_img = form.cleaned_data.get('img_link')
            #(width, height)  = temp_img.size

            #temp_img.resize( (width/(width/200), height/(width/200)), Image.ANTIALIAS )
            #offer.img_link = temp_img

            offer.save()

            form.save_m2m()

            # Redirect to inventory, new offer created
            return redirect('inventory')
    else:
        form = OfferForm()
    return render(request, 'inventory/newOffer.html', {'form': form})

# Only shows customer/anonymous the non-private inventory, owners see all inventory
def viewOffer(request):
    if(request.user.is_authenticated and request.user.profile.isOwner):
        offers_list = Inventory.objects.all()
        return render(request, 'inventory/viewOffer.html', {'offers_list' : offers_list})
    else:
        offers_list = []
        for offer in Inventory.objects.all():
            if not offer.private:
                offers_list.append(offer)
        return render(request, 'inventory/viewOffer.html', {'offers_list' : offers_list})
        
# Owners can edit their offers. 
@login_required
def editOffer(request, slug):
    if(request.user.profile.isOwner):
        offer = get_object_or_404(Inventory, id=slug)
        if request.method == 'POST':
            form = UpdateOfferForm(request.POST)
            if form.is_valid():
                offer.refresh_from_db()

                offer.name = form.cleaned_data.get('name')
                offer.price = form.cleaned_data.get('price')
                offer.location = form.cleaned_data.get('location')
                offer.text_description = form.cleaned_data.get('text_description')
                offer.img_link = form.cleaned_data.get('img_link')

                offer.save()

                return redirect('inventory')
        else:
            form = UpdateOfferForm(instance=offer)
        return render(request, 'inventory/newOffer.html', {'form' : form, 'offer' : offer})
    else:
        return render(request, 'inventory/index.html')
        
# Owners can delete an offer
@login_required
def deleteOffer(request, slug):
    if(request.user.profile.isOwner):
        offer = get_object_or_404(Inventory, id=slug)
        if request.method == 'POST':
            offer.delete(keep_parents=True)
            return redirect('inventory')
        else:
            return render(request, 'inventory/deleteOffer.html', {'offer' : offer})
    else:
        return redirect('inventory')
        
# Owners can show/hide an offer
@login_required
def showHideOffer(request, slug):
    if(request.user.profile.isOwner):
        offer = get_object_or_404(Inventory, id=slug)
        
        offer.refresh_from_db()
        
        #Invert privacy field
        offer.private = not offer.private
        
        offer.save()
        
        return redirect('inventory')
        
    else:
        return redirect('inventory')

@login_required
def receipt(request, slug):
    donation = get_object_or_404(Donation, id=slug)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="%sReceipt.pdf"' %slug

    p = canvas.Canvas(response, pagesize=letter)
    p.setLineWidth(.3)
    p.setFont('Helvetica', 16)

    #Header
    p.drawString(240, 720, 'Donation Receipt')
    p.drawString(50, 675, 'Organization Receiving Donation')
    p.drawString(50, 655, 'Organization\'s Address')
    p.drawString(50, 635, 'Organization\'S Phone Number')

    p.drawString(50, 595, 'Item/Donation ID: %s' %slug)

    #Content
    p.drawString(50, 555, 'Charitable Contribution Receipt')
    p.line(25, 550, 575, 550)
    p.drawString(50, 510, 'Date of Receipt:   ')
    p.drawString(50, 470, 'Donor\'s Name:   %s' %donation.donor)
    p.drawString(50, 430, 'Donation Type:   Item Donation')
    p.drawString(50, 390, 'Description of Donation:   %s' %donation.text_description)
    p.drawString(50, 350, 'Amount of Contribution:   %s' %donation.quantity)
    p.drawString(50, 310, 'Donor\'s Estimated Value of Goods or Services: ')
    p.drawString(50, 270, 'Signed As Recieved By:   ')
    p.drawString(50, 190, '**Notice: No Goods Or Services Were Provieded In Return For This Gift')



    p.showPage()
    p.save()
    return response