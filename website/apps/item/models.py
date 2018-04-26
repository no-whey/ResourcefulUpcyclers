from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from website.apps.core.models import Business
from model_utils.fields import StatusField
from model_utils import Choices
from mptt.models import MPTTModel, TreeForeignKey

import tagulous.models

class Donation(models.Model):

    STATUS_OPTIONS = Choices('pending', 'accepted', 'declined')

    name = models.TextField(max_length=30, blank=True)
    text_description = models.TextField(max_length=500, blank=True)
    quantity = models.IntegerField(default=0, null=True)
    img_link = models.URLField(max_length=200, blank=True)
    city = models.TextField(max_length=30, blank=True)
    donor = models.ForeignKey(User, related_name='donation_creator', on_delete=models.CASCADE)
    donor_email = models.EmailField(max_length=255)
    status = StatusField(choices_name='STATUS_OPTIONS', default='pending')
    owner_interest = models.BooleanField(default=False)
    needs_pickup = models.BooleanField(default=False)
    declined_reason = models.TextField(max_length=200, blank=True, default='', null=True)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)

    @staticmethod
    def get_my_donations(user):
        donation_list = list(user.donation_creator.all())
        return donation_list

    @staticmethod
    def get_all_business_donations(user, business_in):
        donation_list = list(Donation.objects.filter(business = business_in))
        return donation_list

#Custom tag model
#Used to bypass tagulous default model name generation
class Inventory_Tags(tagulous.models.TagModel):
    class TagMeta:
        #Tag options
        force_lowercase = True
        #autocomplete_view =

#Class used to create offers
class Inventory(models.Model):

    name = models.TextField(max_length=30, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    location = models.TextField(max_length=60, blank=True)
    text_description = models.TextField(max_length=500, blank=True)
    img_link = models.URLField(max_length=200, blank=True)
    quantity = models.PositiveIntegerField(default=0)
    date = models.DateField(auto_now=True)
    private = models.BooleanField(default=False)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)

    #Using tagulous tags
    tag_pile = tagulous.models.TagField(to=Inventory_Tags)

    @staticmethod
    def get_all_business_inventory(user, business_in):
        inventory_list = list(Inventory.objects.filter(business = business_in))
        return inventory_list

class Category(MPTTModel):

    name = models.CharField(max_length=100)
    #slug = models.SlugField()
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children',
                            db_index=True, on_delete=models.SET_NULL)
    offers = models.ManyToManyField(Inventory, default=None, blank=True)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)

    class MPTTMeta:
        order_insertion_by = ['name']
