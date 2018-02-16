from django import forms
from website.apps.item.models import Donation
from website.apps.item.models import Offer

# Note for future stylizing: if you want to make a text BOX use widget=forms.Textarea, if you just want to make the CharField
# box longer, use widget=forms.TextIput. We can just use Textarea if that's easier, set rows to 1.
class DonationForm(forms.Form):

    name = forms.CharField( label='Name of the Item', max_length=30, required=True, help_text='General Name of Item', \
         widget=forms.TextInput (attrs={ 'size': 60 }) )

    text_description = forms.CharField ( label='Description of the Item', max_length=500, required=True, \
        help_text='Describe the Item\'s features along with any flaws or impairments', widget=forms.Textarea(attrs={'cols': 80, 'rows': 4}) )

    img_link = forms.URLField ( max_length=200, required=True, help_text='Link to Images of Item (use a different site)', \
        widget=forms.TextInput (attrs={ 'size':60 }) )

    city = forms.CharField ( max_length=30, required=True, help_text='Name of the city the item is coming from' )

    donor_email = forms.EmailField ( max_length=255, required=True, help_text='Email or phone number to contact you *Required', \
        widget=forms.TextInput (attrs={ 'size': 60 }) )

    # Be sure to add extra fields here
    class Meta:
        model = Donation
        fields = (  'name',
                    'text_description',
                    'img_link',
                    'city',
                    'donor_email',
                    )

class OfferForm(forms.Form):

    name = forms.CharField (max_length=30, required=True, help_text='General Name of Item')
    price = forms.CharField (max_length=30, required=True, help_text='Asking Price of Item')
    location = forms.CharField (max_length=60, required=True, help_text='In-House Item Location')
    text_description = forms.CharField (max_length=500, required=True, help_text='Describe the Item')
    img_link = forms.URLField (max_length=200, required=True, help_text='Link to Images of Item (use a different site)')
    
    # Be sure to add extra fields here
    class Meta:
        model = Offer
        fields = (  'name',
                    'price',
                    'location',
                    'text_description',
                    'img_link',
                    )
