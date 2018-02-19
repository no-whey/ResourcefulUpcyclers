from django import forms
from model_utils.fields import StatusField
from model_utils import Choices

from website.apps.item.models import Donation
from website.apps.item.models import Inventory

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

class UpdateDonationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        #old_donation = kwargs.pop('instance')
        super(UpdateDonationForm, self).__init__(*args, **kwargs)
        # Re-enter the Donation info if we're just updating it
        '''
        if old_donation:
            self.fields['name'].initial = old_donation.name
            self.fields['text_description'].initial = old_donation.text_description
            self.fields['img_link'].initial = old_donation.img_link
            self.fields['city'].initial = old_donation.city
            self.fields['donor_email'].initial = old_donation.donor_email
        '''
        if 'instance' in kwargs and kwargs['instance']:
            self.fields['name'].initial = kwargs['instance'].name
            self.fields['text_description'].initial = kwargs['instance'].text_description
            #self.fields['img_link'].initial = kwargs['instance'].img_link
            self.fields['city'].initial = kwargs['instance'].city
            self.fields['donor_email'].initial = kwargs['instance'].donor_email

    STATUS_OPTIONS = Choices('pending', 'accepted', 'declined')

    name = forms.CharField( label='Name of the Item', max_length=30, required=True, help_text='General Name of Item', \
         widget=forms.TextInput (attrs={ 'size': 60 }) )

    text_description = forms.CharField ( label='Description of the Item', max_length=500, required=True, \
        help_text='Describe the Item\'s features along with any flaws or impairments', widget=forms.Textarea(attrs={'cols': 80, 'rows': 4}) )

    img_link = forms.URLField ( max_length=200, required=True, help_text='Link to Images of Item (use a different site)', \
        widget=forms.TextInput (attrs={ 'size':60 }) )

    city = forms.CharField ( max_length=30, required=True, help_text='Name of the city the item is coming from' )

    donor_email = forms.EmailField ( max_length=255, required=True, help_text='Email or phone number to contact you *Required', \
        widget=forms.TextInput (attrs={ 'size': 60 }) )

    status = StatusField(choices_name='STATUS_OPTIONS')

    owner_interest = forms.BooleanField ( label='Show Interest', help_text='Check this if your interested in acquiring the donation' , required=False)

    # Be sure to add extra fields here
    class Meta:
        model = Donation
        fields = (  'name',
                    'text_description',
                    'img_link',
                    'city',
                    'donor_email',
                    'status',
                    'owner_interest',
                    )


class OfferForm(forms.Form):

    name = forms.CharField (max_length=30, required=True, help_text='General Name of Item')
    price = forms.CharField (max_length=30, required=True, help_text='Asking Price of Item')
    location = forms.CharField (max_length=60, required=True, help_text='In-House Item Location')
    text_description = forms.CharField (max_length=500, required=True, help_text='Describe the Item')
    img_link = forms.URLField (max_length=200, required=True, help_text='Link to Images of Item (use a different site)')
    # Be sure to add extra fields here
    class Meta:
        model = Inventory
        fields = (  'name',
                    'price',
                    'location',
                    'text_description',
                    'img_link',
                    )
