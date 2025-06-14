from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    location = models.CharField(max_length=100, null=True, blank=True)
    is_chef = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class ChefProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    specialization = models.CharField(max_length=100, blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    profile_picture = models.ImageField(upload_to='chef_profiles/', blank=True, null=True)
    kitchen_license_image = models.ImageField(upload_to='chef_licenses/')
    bank_details = models.JSONField()  # Store bank account details securely
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_chef_profile(sender, instance, created, **kwargs):
    if created and instance.is_chef:
        ChefProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_chef_profile(sender, instance, **kwargs):
    if instance.is_chef:
        instance.chefprofile.save()
