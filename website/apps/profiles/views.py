from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from .forms import SignUpForm

def index(request):
    return render(request, 'profiles/index.html')

def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			# Applies Profile fields
			user = form.save()
			user.refresh_from_db()
			user.profile.birth_date = form.cleaned_data.get('birth_date')
			user.profile.bio = form.cleaned_data.get('bio')
			user.profile.business_key = form.cleaned_data.get('business_key')
			#user.profile.profile_image = form.cleaned_data.get('profile_image')
			user.save()

			# User requirements
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=raw_password)

			# Redirect home, new User is logged in
			login(request, user)
			return redirect('home')
	else:
		form = SignUpForm()
	return render(request, 'profiles/signup.html', {'form': form})