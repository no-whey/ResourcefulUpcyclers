from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.shortcuts import render, redirect
from decouple import config
from website.apps.core.models import Business
from website.apps.core.forms import CreateBusinessForm
from website.apps.profiles.forms import SignUpOwnerForm, SignUpCustomerForm, UpdateUserForm

@login_required
def index(request):
    if(request.user.profile.isOwner):
        return render(request, 'profile/businessprofile.html')
    else:
        return render(request, 'profile/profile.html')

def signup_owner(request):
    if request.method == 'POST':
        form = SignUpOwnerForm(request.POST)
        if form.is_valid():
            # Applies Profile fields
            user = form.save()
            user.refresh_from_db()

            #Checks if they put in an owner key
            if form.cleaned_data.get('owner_key'):
                #Here we check if a user is signing up to an
                #Existing business
                business_list = Business.objects.all()
                attempted_key = form.cleaned_data.get('owner_key')
                for business in business_list:
                    if attempted_key == business.owner_key:
                        user.profile.isOwner = True
                        user.profile.business = Business.objects.get(id=business.id)
                        user.groups.add(business.owner_group)
            # Either Create and add, or just add that owner to the owners group
            """
            if user.profile.isOwner:
                try:
                    owners_group = Group.objects.get(name='owners')
                    user.groups.add(owners_group)
                except Group.DoesNotExist:
                    owners_group = Group(name='owners')
                    owners_group.save()
                    user.groups.add(owners_group)
            """
            #user.profile.profile_image = form.cleaned_data.get('profile_image')
            user.save()
            # User requirements
            username = form.cleaned_data.get('username')
            #raw_password = form.cleaned_data.get('password')
            #user = authenticate(username=username, password=raw_password)
            login(request, user)
            if not user.profile.isOwner:
                return redirect('create_business')
            # Redirect home, new User is logged in

            return redirect('home')
    else:
        form = SignUpOwnerForm()
    return render(request, 'registration/signup_owner.html', {'form': form})


def signup_customer(request):
    if request.method == 'POST':
        form = SignUpCustomerForm(request.POST)
        if form.is_valid():
            # Applies Profile fields
            user = form.save()
            user.refresh_from_db()
            user.save()
            #user.profile.birth_date = form.cleaned_data.get('birth_date')
            #user.profile.bio = form.cleaned_data.get('bio')

            # User requirements
            username = form.cleaned_data.get('username')
            #raw_password = form.cleaned_data.get('password')
            #user = authenticate(username=username, password=raw_password)

            # Redirect home, new User is logged in
            login(request, user)
            return redirect('home')
    else:
        form = SignUpCustomerForm()
    return render(request, 'registration/signup_customer.html', {'form': form})

def logout_user(request):
    logout(request)
    return render(request, 'profile/logout.html')

@login_required
def update_user(request):
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            user.refresh_from_db()

            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.profile.bio = form.cleaned_data.get('bio')
            user.save()

            return redirect('profile')
    else:
        form = UpdateUserForm(instance=request.user.profile)
    return render(request, 'profile/updateprofile.html', {'form':form})
