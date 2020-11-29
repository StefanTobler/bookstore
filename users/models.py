from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.base_user import AbstractBaseUser
from django.db.models.signals import post_save

from address.models import AddressField
from phonenumber_field.modelfields import PhoneNumberField
from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField

from enum import Enum

class StoreUser(models.Model):

    ACTIVE = 'A'
    INACTIVE = 'I'
    SUSPENDED = 'S'

    CHOICES = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
        (SUSPENDED, 'Suspended')
    ]

    address = AddressField(blank=True, null=True)
    phone_number = PhoneNumberField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None, null=True)
    status = models.CharField(max_length=10, choices=CHOICES, default=INACTIVE)
    subscribed = models.BooleanField(default=False)
    activation_token = models.CharField(max_length=40, blank=True)
    is_employee = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Store User'

    def get_status(self):
        for choice in self.CHOICES:
            if choice[0] == self.status:
                return choice[1]
        return None

    def is_active(self):
        return self.status == self.ACTIVE

    def is_suspended(self):
        return self.status == self.SUSPENDED

    def activate(self):
        self.status = self.ACTIVE
        return True

    def suspend(self):
        self.status = self.SUSPENDED
        return True

    def deactivate(self):
        self.status = self.INACTIVE
        return True

class Payment(models.Model):
    cc_number = CardNumberField(blank=True, null=True)
    cc_expiry = CardExpiryField(blank=True, null=True)
    cc_code = SecurityCodeField(blank=True, null=True)
    billing_address = AddressField(blank=True, null=True)
    user = models.OneToOneField(StoreUser, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'****{self.cc_number[-4:]}'

    def get_ending(self):
        return self.cc_number[-4:]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile.png', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
