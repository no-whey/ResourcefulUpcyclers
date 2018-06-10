from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.contrib.auth import authenticate
from website.apps.item.models import *
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from website.apps.alert.models import Alert

import tagulous
import operator
import csv
import datetime
from django.db.models import Q

from .forms import * #RequestForm, DonationForm, UpdateDonationForm, OfferForm, UpdateOfferForm, NewCategoryForm

# For customers to create a new donation ticket
@login_required
def newDonation(request, bid):
    business = get_object_or_404(Business, id=bid)
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            # Applies Offer fields
            #offer = form.save()
            donation = Donation()
            donation.donor = request.user
            donation.business = business
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

            #Notify owners
            for owner in business.profile_set.all():
                Alert.create("New Donation!",
                             "A user has offered to donate \'" + donation.name + "\'",
                             owner.user)

            # Redirect to all Donations from that user, Maybe a "Thank you" page???
            return redirect('allDonations', bid=bid)
    else:
        form = DonationForm()
    return render(request, 'donations/newDonation.html', {'form': form, 'business' : business})

# For Customers to view their submitted Donations, Owners can see all donations
@login_required
def allDonations(request, bid):
    business = get_object_or_404(Business, id=bid)
    owner_group = User.objects.filter(groups__name=business.name)
    if(request.user.profile.isOwner and request.user.profile.business==business):
        donation_list = Donation.get_all_business_donations(request.user, business)
        return render(request, 'donations/allDonations.html', {'donations' : donation_list, 'business' : business, 'owner_group' : owner_group, 'user' : request.user, 'intflag' : False})
    else:
        donation_list = Donation.get_my_donations(request.user)
        return render(request, 'donations/allDonations.html', {'donations' : donation_list, 'business' : business, 'owner_group' : owner_group, 'user' : request.user, 'intflag' : False})

# Owners see only their interested Donations, customers get same access as allDonations view
@login_required
def interestedDonations(request, bid):
    business = get_object_or_404(Business, id=bid)
    owner_group = User.objects.filter(groups__name=business.name)
    if(request.user.profile.isOwner and request.user.profile.business==business):
        donation_list = []
        business_donations = Donation.get_all_business_donations(request.user, business)
        for donation in business_donations:
            if donation.owner_interest:
                donation_list.append(donation)
        return render(request, 'donations/allDonations.html', {'donations' : donation_list, 'business' : business, 'owner_group' : owner_group, 'user' : request.user, 'intflag' : True})
    else:
        donation_list = Donation.get_my_donations(request.user)
        return render(request, 'donations/allDonations.html', {'donations' : donation_list, 'business' : business, 'owner_group' : owner_group, 'user' : request.user, 'intflag': True})

# For Owners to view and edit one specific donation
@login_required
def oneDonation(request, bid, slug):
    business = get_object_or_404(Business, id=bid)
    if(request.user.profile.isOwner and request.user.profile.business==business):
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
                donation.declined_reason = form.cleaned_data.get('declined_reason')
                donation.owner_interest = form.cleaned_data.get('owner_interest')

                donation.save()

                #Notify Donor
                Alert.create("Donation updated!",
                             "Your donation of \'" + donation.name + "\' has been updated.",
                             donation.donor)

                # Redirect to Home, Maybe a "Thank you" page???
                return redirect('allDonations', bid=bid)
        else:
            form = UpdateDonationForm(instance=donation)
        return render(request, 'donations/oneDonation.html', {'form' : form, 'donation' : donation, 'business' : business})
    else:
        return render(request, 'donations/allDonations.html', {'business' : business})

# Owners can delete a donation
@login_required
def deleteDonation(request, bid, slug):
    business = get_object_or_404(Business, id=bid)
    if(request.user.profile.isOwner and request.user.profile.business==business):
        donation = get_object_or_404(Donation, id=slug)
        if request.method == 'POST':
            donation.delete(keep_parents=True)
            return redirect('allDonations', bid=bid)
        else:
            return render(request, 'donations/deleteDonation.html', {'donation' : donation, 'business' : business})
    else:
        return redirect('allDonations', bid=bid)

# For customers to create a new donation ticket
@login_required
def newRequest(request, bid):
    business = get_object_or_404(Business, id=bid)
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            req = Request()
            req.inquirer = request.user
            req.business = business
            req.save()
            req.refresh_from_db()

            req.name = form.cleaned_data.get('name')
            req.text_description = form.cleaned_data.get('text_description')
            req.user_email = form.cleaned_data.get('user_email')

            req.save()

            #Notify owners
            for owner in business.profile_set.all():
                Alert.create("New Request!",
                             "A user has made a request for \'" + req.name + "\'",
                             owner.user)
            # Redirect to all Donations from that user, Maybe a "Thank you" page???
            return redirect('allRequests', bid=bid)
    else:
        form = RequestForm()
    return render(request, 'requests/newRequest.html', {'form': form, 'business' : business})

# For Customers to view their submitted Donations, Owners can see all donations
@login_required
def allRequests(request, bid):
    business = get_object_or_404(Business, id=bid)
    owner_group = User.objects.filter(groups__name=business.name)
    if(request.user.profile.isOwner and request.user.profile.business==business):
        request_list = Request.get_all_business_requests(request.user, business)
        return render(request, 'requests/allRequests.html', {'requests' : request_list, 'business' : business, 'owner_group' : owner_group, 'user' : request.user})
    else:
        request_list = Request.get_my_requests(request.user)
        return render(request, 'requests/allRequests.html', {'requests' : request_list, 'business' : business, 'owner_group' : owner_group, 'user' : request.user})


# Owners can view their available inventory
@login_required
def inventory(request, bid):
    business = get_object_or_404(Business, id=bid)
    owner_group = User.objects.filter(groups__name=business.name)   
    if(request.user.profile.isOwner and request.user.profile.business==business):
        #Loading page
        if request.method == 'GET':
            inventory_list = Inventory.get_all_business_inventory(request.user, business)
            return render(request, 'inventory/index.html', {'inventory' : inventory_list, 'business' : business, 'owner_group' : owner_group, 'user' : request.user})
        #Loading page after searching
        elif request.method == 'POST':
            search = str(request.POST.get('q', None))
            #Empty search bar
            if search == "":
                inventory_list = Inventory.get_all_business_inventory(request.user, business)
            #Non-Empty search bar
            else:
                inventory_list = Inventory.objects.filter(tag_pile=search, business=business)
            return render(request, 'inventory/index.html', {'inventory' : inventory_list, 'business' : business, 'owner_group' : owner_group, 'user' : request.user})
        #Other methods
        else:
            inventory_list = Inventory.get_all_business_inventory(request.user, business)
            return render(request, 'inventory/index.html', {'inventory' : inventory_list, 'business' : business, 'owner_group' : owner_group, 'user' : request.user})
    else:
        return render(request, 'index.html')

# Owners can create new offers
@login_required
def newOffer(request, bid):
    business = get_object_or_404(Business, id=bid)
    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():

            #get offer obj
            offer = Inventory()
            offer.business = business
            offer.name = form.cleaned_data.get('name')
            offer.price = form.cleaned_data.get('price')
            #offer.location = form.cleaned_data.get('location')
            offer.text_description = form.cleaned_data.get('text_description')
            offer.img_link = form.cleaned_data.get('img_link')
            offer.quantity = form.cleaned_data.get('quantity')
            offer.private = form.cleaned_data.get('private')
            offer.tag_pile = form.cleaned_data.get('tag_pile')
            offer.save()

            if form.cleaned_data.get('location'):
                location = form.cleaned_data.get('location')
                offer.location = location

            if form.cleaned_data.get('category'):
                category = form.cleaned_data.get('category')
                category.offers.add(offer)
                category.save()

            #Save all fields except m2m
            offer.save()
            #save m2m fields
            #form.save_m2m()

            # Redirect to inventory, new offer created
            return redirect('inventory', bid=bid)
    else:
        form = OfferForm()
    return render(request, 'inventory/newOffer.html', {'form': form, 'business' : business})

# Only shows customer/anonymous the non-private inventory, owners see all inventory
def viewOffer(request, bid):
    #Loading page
    business = get_object_or_404(Business, id=bid)
    owner_group = User.objects.filter(groups__name=business.name)
    
    if request.method == 'GET':
        offers_list = Inventory.objects.filter(private=False, business=business)
        return render(request, 'inventory/viewOffer.html', {'offers_list' : offers_list, 'business' : business, 'owner_group' : owner_group, 'user' : request.user})
    #Loading page after searching
    elif request.method == 'POST':
        search = str(request.POST.get('q', None))
        #Empty search bar
        if search == "":
            offers_list = Inventory.objects.filter(private=False, business=business)
        #Non-Empty search bar
        else:
            offers_list = Inventory.objects.filter(private=False, tag_pile=search, business=business)
        return render(request, 'inventory/viewOffer.html', {'offers_list' : offers_list, 'business' : business, 'owner_group' : owner_group, 'user' : request.user})
    #Other methods
    else:
        offers_list = Inventory.objects.filter(private=False, business=business)
        return render(request, 'inventory/viewOffer.html', {'offers_list' : offers_list, 'business' : business, 'owner_group' : owner_group, 'user' : request.user})

# Owners can edit their offers.
@login_required
def editOffer(request, bid, slug):
    business = get_object_or_404(Business, id=bid)
    if(request.user.profile.isOwner and request.user.profile.business==business):
        offer = get_object_or_404(Inventory, id=slug)
        if request.method == 'POST':
            form = UpdateOfferForm(request.POST)
            if form.is_valid():
                offer.refresh_from_db()
                #get offer obj
                #offer = form.save(commit=False)

                offer.name = form.cleaned_data.get('name')
                offer.price = form.cleaned_data.get('price')
                #offer.location = form.cleaned_data.get('location')
                offer.text_description = form.cleaned_data.get('text_description')
                offer.img_link = form.cleaned_data.get('img_link')
                offer.quantity = form.cleaned_data.get('quantity')
                offer.private = form.cleaned_data.get('private')
                offer.tag_pile = form.cleaned_data.get('tag_pile')
                offer.save()

                if form.cleaned_data.get('location'):
                    location = form.cleaned_data.get('location')
                    offer.location = location

                if form.cleaned_data.get('category'):
                    category = form.cleaned_data.get('category')
                    category.offers.add(offer)
                    category.save()

                #Save all fields except m2m
                offer.save()

                #Notify owners
                for owner in business.profile_set.all():
                    Alert.create("Offer updated!",
                                 "Your offer \'" + offer.name + "\' has been updated.",
                                 owner.user)

                #Redirect to inventory, offer edited
                return redirect('inventory', bid=bid)
        else:
            form = UpdateOfferForm(instance=offer)
        return render(request, 'inventory/newOffer.html', {'form' : form, 'offer' : offer, 'business' : business})
    else:
        return render(request, 'inventory/index.html', {'business' : business,})

# Owners can delete an offer
@login_required
def deleteOffer(request, bid, slug):
    business = get_object_or_404(Business, id=bid)
    if(request.user.profile.isOwner and request.user.profile.business==business):
        offer = get_object_or_404(Inventory, id=slug)
        if request.method == 'POST':
            offer.delete(keep_parents=True)
            return redirect('inventory', bid=bid)
        else:
            return render(request, 'inventory/deleteOffer.html', {'offer' : offer, 'business' : business})
    else:
        return redirect('inventory', bid=bid)

# Owners can show/hide an offer
@login_required
def showHideOffer(request, bid, slug):
    business = get_object_or_404(Business, id=bid)
    if(request.user.profile.isOwner and request.user.profile.business==business):
        offer = get_object_or_404(Inventory, id=slug)

        offer.refresh_from_db()

        #Invert privacy field
        offer.private = not offer.private

        offer.save()

        return redirect('inventory', bid=bid)

    else:
        return redirect('inventory', bid=bid)

# Customers can show interest in an item and contact info is exchanged
@login_required
def interestedOffer(request, bid, slug):
    business = get_object_or_404(Business, id=bid)
    offer = get_object_or_404(Inventory, id=slug)
    user = request.user

    #Notify owners
    for owner in business.profile_set.all():
        Alert.create("Interest in offer!",
                     user.username + " (" + user.email + \
                        ") has shown interest in your offer of \'" + offer.name + "\'",
                     owner.user)

    return redirect('viewOffer', bid=bid)

@login_required
def receipt(request, bid, slug):
    business = get_object_or_404(Business, id=bid)
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

# For Owners to create and view their categories
@login_required
def manageCategories(request, bid):
    business = get_object_or_404(Business, id=bid)
    if (request.user.profile.isOwner and request.user.profile.business==business):
        category_tree = Category.objects.filter(business=business)
        if request.method == 'POST':
            form = NewCategoryForm(request.POST)
            if form.is_valid():

                cat = Category()
                cat.name = form.cleaned_data.get('name')
                cat.business = business
                if(form.cleaned_data.get('parent')):
                    cat.parent = form.cleaned_data.get('parent')
                cat.save()

                # Redirect to all Donations from that user, Maybe a "Thank you" page???
                return redirect('manageCategories', bid=bid)
        else:
            form = NewCategoryForm()
        return render(request, 'categories/manageCategories.html', {'categories' : category_tree, 'form' : form, 'business' : business})
    return redirect('home')


def allCategories(request, bid):
    business = get_object_or_404(Business, id=bid)
    category_tree = Category.objects.filter(business = business)
    return render(request, 'categories/allCategories.html', {'categories' : category_tree, 'business' : business})

# View the NON-PRIVATE offers in a category
def oneCategory(request, bid, slug):
    business = get_object_or_404(Business, id=bid)
    category = get_object_or_404(Category, id=slug)
    offers_list = []
    for offer in category.offers.all():
        if offer is not offer.private:
            offers_list.append(offer)
    return render(request, 'inventory/viewOffer.html', {'offers_list' : offers_list, 'business' : business})

@login_required
def manageLocations(request, bid):
    business = get_object_or_404(Business, id=bid)
    if (request.user.profile.isOwner and request.user.profile.business==business):
        location_tree = StoreLocation.objects.filter(business=business)
        if request.method == 'POST':
            form = NewStoreLocationForm(request.POST)
            if form.is_valid():

                loc = StoreLocation()
                loc.name = form.cleaned_data.get('name')
                loc.business = business
                if(form.cleaned_data.get('parent')):
                    loc.parent = form.cleaned_data.get('parent')
                loc.save()

                # Redirect to all Donations from that user, Maybe a "Thank you" page???
                return redirect('manageLocations', bid=bid)
        else:
            form = NewStoreLocationForm()
        return render(request, 'storeLocation/manageLocations.html', {'location_tree' : location_tree, 'form' : form, 'business' : business})
    return redirect('home')

"""
def allLocations(request, bid):
    business = get_object_or_404(Business, id=bid)
    location_tree = StoreLocation.objects.filter(business = business)
    return render(request, 'storeLocation/allLocations.html', {'location_tree' : location_tree, 'business' : business})
"""

# View the NON-PRIVATE offers in a category
def oneLocation(request, bid, slug):
    business = get_object_or_404(Business, id=bid)
    store_location = get_object_or_404(StoreLocation, id=slug)
    offers_list = []
    for offer in Inventory.objects.filter(business=business):
        if offer is not offer.private and offer.location == store_location:
            offers_list.append(offer)
    return render(request, 'inventory/viewOffer.html', {'offers_list' : offers_list, 'business' : business})


@login_required
def oneRequest(request):
    return render(request, 'requests/request.html')

@login_required
def exportCSV(request, bid):
    business = get_object_or_404(Business, id=bid)
    if request.method == 'GET':
        offers_list = Inventory.objects.filter(private=False, business=business)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Business%s_Inventory.csv'%bid

    writer = csv.writer(response)
    writer.writerow(['Item Name', 'Quantity', 'Price', 'Private', 'Description', 'Image Link',])
    for item in offers_list:
        writer.writerow([item.name, item.quantity, item.price, item.private, item.text_description, item.img_link,])

    return response
