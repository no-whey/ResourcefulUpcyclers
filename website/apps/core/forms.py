from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from website.apps.core.models import Business

class CreateBusinessForm(forms.Form):

    name = forms.CharField(max_length=30, required=True,
        help_text='Name of your Organization')
    bio = forms.CharField(max_length=500, required=True,
        help_text='Write a short bio about your Organization')
    address = forms.CharField(max_length=200, required=True,
        help_text="Format: 123 Qwerty Ave #456, City, ST 99999")
    icon = forms.ImageField(max_length=100, required=False,
        help_text="Upload a JPEG or PNG logo")

    class Meta:
        model = Business
        fields = (  'name',
                    'bio',
                    'address',
                    'icon',
                    )
