from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from website.apps.core.models import Business

class Profile(models.Model):
    # Adopting User model
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Extra information, Add extra attributes here
    bio = models.TextField(max_length=500, blank=True, null=True)
    #birth_date = models.DateField(null=True, blank=True)
    isOwner = models.BooleanField(default=False)
    #profile_image = models.ImageField(upload_to=None)
    business = models.ForeignKey(Business, blank=True, null=True, on_delete=models.CASCADE)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    try:
        instance.profile.save()
    except AttributeError:
        profile = Profile.objects.create(user=instance)
        profile.save()
