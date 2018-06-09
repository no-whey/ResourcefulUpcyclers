from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from website.apps.core.models import Business

class CreateBusinessForm(forms.Form):

    name = forms.CharField(max_length=30, required=True,
        help_text='Name of your Organization')
    description = forms.CharField(max_length=500, required=True,
        help_text='Write a short description about your Organization')
    address = forms.CharField(max_length=200, required=True,
        help_text="Format: 123 Qwerty Ave #456, City, ST 99999")
    phone_number = forms.CharField(max_length=13, required=True, help_text="e.g. 1-888-123-4567")
    icon = forms.URLField ( max_length=200, required=True, help_text='Link to Images (use a different site)')

    class Meta:
        model = Business
        fields = (  'name',
                    'description',
                    'address',
                    'phone_number',
                    'icon',
                    )
