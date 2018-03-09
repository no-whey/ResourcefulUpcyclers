from django import forms
from model_utils.fields import StatusField
from model_utils import Choices

from website.apps.item.models import *
import tagulous.forms
from mptt.forms import *

# Note for future stylizing: if you want to make a text BOX use widget=forms.Textarea, if you just want to make the CharField
# box longer, use widget=forms.TextIput. We can just use Textarea if that's easier, set rows to 1.
class DonationForm(forms.Form):

    name = forms.CharField( label='Name of the Item', max_length=30, required=True, help_text='General Name of Item', \
         widget=forms.TextInput (attrs={ 'size': 60 }) )
    text_description = forms.CharField ( label='Description of the Item', max_length=500, required=True, \
        help_text='Describe the Item\'s features along with any flaws or impairments', widget=forms.Textarea(attrs={'cols': 80, 'rows': 4}) )
    quantity = forms.IntegerField ( label='Quantity', required=True, help_text='Number of items' )
    img_link = forms.URLField ( max_length=200, required=True, help_text='Link to Images of Item (use a different site)', \
        widget=forms.TextInput (attrs={ 'size':60 }) )
    city = forms.CharField ( max_length=30, required=True, help_text='Name of the city the item is coming from' )
    donor_email = forms.EmailField ( max_length=255, required=True, help_text='Email or phone number to contact you *Required', \
        widget=forms.TextInput (attrs={ 'size': 60 }) )
    needs_pickup = forms.BooleanField ( label='Needs Pickup', help_text='Does this item need to be retrieved from your location?', required=False)

    # Be sure to add extra fields here
    class Meta:
        model = Donation
        fields = (  'name',
                    'text_description',
                    'quantity',
                    'img_link',
                    'city',
                    'donor_email',
                    'needs_pickup'
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
            self.fields['quantity'].initial = kwargs['instance'].quantity
            self.fields['img_link'].initial = kwargs['instance'].img_link
            self.fields['city'].initial = kwargs['instance'].city
            self.fields['donor_email'].initial = kwargs['instance'].donor_email
            self.fields['needs_pickup'].initial = kwargs['instance'].needs_pickup

    STATUS_OPTIONS = Choices('pending', 'accepted', 'declined')

    name = forms.CharField ( label='Name of the Item', max_length=30, required=True, help_text='General Name of Item', \
        widget=forms.TextInput (attrs={ 'size': 60 }) )
    text_description = forms.CharField ( label='Description of the Item', max_length=500, required=True, \
        help_text='Describe the Item\'s features along with any flaws or impairments', widget=forms.Textarea(attrs={'cols': 80, 'rows': 4}) )
    quantity = forms.IntegerField ( label='Quantity', required=True, help_text='Number of items' )
    img_link = forms.URLField ( max_length=200, required=True, help_text='Link to Images of Item (use a different site)', \
        widget=forms.TextInput (attrs={ 'size':60 }) )
    city = forms.CharField ( max_length=30, required=True, help_text='Name of the city the item is coming from' )
    donor_email = forms.EmailField ( max_length=255, required=True, help_text='Email or phone number to contact you *Required', \
        widget=forms.TextInput (attrs={ 'size': 60 }) )
    needs_pickup = forms.BooleanField ( label='Needs Pickup', help_text='Does this item need to be retrieved from your location *Required', required=False )
    status = StatusField( choices_name='STATUS_OPTIONS' )
    declined_reason = forms.CharField( label='Reason for declining:', max_length=200, widget=forms.TextInput (attrs={ 'size': 60 }), required=False, \
        help_text='**Fill this out only if delcining a donation for donor to see.**' )
    owner_interest = forms.BooleanField ( label='Show Interest', help_text='Check this if your interested in acquiring the donation' , required=False )

    # Be sure to add extra fields here
    class Meta:
        model = Donation
        fields = (  'name',
                    'text_description',
                    'quantity',
                    'img_link',
                    'city',
                    'donor_email',
                    'needs_pickup',
                    'status',
                    'declined_reason',
                    'owner_interest',
                    )


class OfferForm(forms.ModelForm):

    name = forms.CharField ( label='Item Name', max_length=30, required=True, help_text='General Name of Item', \
        widget=forms.TextInput (attrs={ 'size': 60 }) )
    quantity = forms.IntegerField ( label='Quantity', required=True, help_text='Number of items' )
    price = forms.DecimalField ( label='Price', required=True, help_text='Asking Price per Item')
    location = forms.CharField ( label='Location', max_length=60, required=True, help_text='In-House Item Location')
    text_description = forms.CharField (label='Description', max_length=500, required=True, help_text='Describe the Item', \
         widget=forms.Textarea(attrs={'cols': 80, 'rows': 4}) )
    img_link = forms.URLField ( label='Image Link', max_length=200, required=True, help_text='Link to Images of Item (use a different site)', \
        widget=forms.TextInput (attrs={ 'size':60 }) )
    private = forms.BooleanField ( label='Hide Item', required=False, help_text='Hide object from public view?')
    tag_pile = tagulous.forms.TagField( label='Item Tags', required=False, help_text='Add tags to help find your object',
        tag_options=tagulous.models.TagOptions(force_lowercase=True))
    category = TreeNodeChoiceField( label='Category', queryset=Category.objects.all(), required=False, help_text='Optional. What Category is this a part of?' )

    # Be sure to add extra fields here
    class Meta:
        model = Inventory
        fields = (  'name',
                    'quantity',
                    'price',
                    'location',
                    'text_description',
                    'img_link',
                    'private',
                    'tag_pile',
                    'category',
                    )

class UpdateOfferForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UpdateOfferForm, self).__init__(*args, **kwargs)

        #Prefill form with old info
        if 'instance' in kwargs and kwargs['instance']:
            self.fields['name'].initial = kwargs['instance'].name
            self.fields['quantity'].initial = kwargs['instance'].quantity
            self.fields['price'].initial = kwargs['instance'].price
            self.fields['location'].initial = kwargs['instance'].location
            self.fields['text_description'].initial = kwargs['instance'].text_description
            self.fields['img_link'].initial = kwargs['instance'].img_link
            self.fields['private'].initial = kwargs['instance'].private
            self.fields['tag_pile'].initial = kwargs['instance'].tag_pile


    name = forms.CharField( label='Name of the Item', max_length=30, required=True, help_text='General Name of Item', \
         widget=forms.TextInput (attrs={ 'size': 60 }) )

    quantity = forms.IntegerField ( label='Quantity', required=True, help_text='Number of items' )

    price = forms.CharField( label='Asking Price of Item', max_length=30, required=True, help_text='Asking Price of Item', \
         widget=forms.TextInput (attrs={ 'size': 60 }) )

    location = forms.CharField( label='In-House Item Location', max_length=60, required=True, help_text='In-House Item Location', \
         widget=forms.TextInput (attrs={ 'size': 60 }) )

    text_description = forms.CharField ( label='Describe the Item', max_length=500, required=True, \
        help_text='Describe the Item', widget=forms.Textarea(attrs={'cols': 80, 'rows': 4}) )

    img_link = forms.URLField ( max_length=200, required=True, help_text='Link to Images of Item (use a different site)', \
        widget=forms.TextInput (attrs={ 'size':60 }))

    private = forms.BooleanField (label='Hide Item', required=False, help_text='Hide object from public view?')

    tag_pile = tagulous.forms.TagField(label='Item Tags', required=False, help_text='Add tags to help find your object', \
        tag_options=tagulous.models.TagOptions(force_lowercase=True))
    category = TreeNodeChoiceField(label='Category', queryset=Category.objects.all(), required=False, help_text='Optional. What Category is this a part of?' )

    # Be sure to add extra fields here
    class Meta:
        model = Inventory
        fields = (  'name',
                    'quantity',
                    'price',
                    'location',
                    'text_description',
                    'img_link',
                    'private',
                    'tag_pile',
                    'category',
                    )

class NewCategoryForm(forms.ModelForm):

    #PARENT_OPTIONS = list(Category.objects.all())

    name = forms.CharField (label='Category Name', max_length=30, required=True, help_text='What type of items will be kept in this category?')
    parent = TreeNodeChoiceField(label='Parent Category', queryset=Category.objects.all(), required=False, help_text='Optional. What is the parent of this category?' )

    class Meta:
        model = Category
        fields = ( 'name',
                   'parent',
                 )
