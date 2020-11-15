from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


from address.models import AddressField
from phonenumber_field.modelfields import PhoneNumberField
from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField

from .models import Payment, StoreUser

class UniqueEmailForm:
    def clean_email(self):
        qs = User.objects.filter(email=self.cleaned_data['email'])
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.count():
            raise forms.ValidationError(
                'That email address is already in use')
        else:
            return self.cleaned_data['email']

class UserRegisterForm(UniqueEmailForm, UserCreationForm):

    first_name = forms.CharField(max_length=32)
    last_name = forms.CharField(max_length=32)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        labels = {
            'first_name': _('First Name'),
            'last_name': _('Last Name'),
        }

class StoreUserRegistrationForm(ModelForm):
    phone_number = PhoneNumberField(unique=True)
    address = AddressField(blank=True)

    class Meta:
        model = StoreUser
        fields = ['phone_number', 'address', 'subscribed']
        labels = {
            'phone_number': _('Phone Number'),
            'address': _('Shipping Address'),
            'subscribed': _('Stay up to date with our promotions!')
        }

class PaymentForm(ModelForm):
    cc_number = CardNumberField(blank=True)
    cc_expiry = CardExpiryField(blank=True)
    cc_code = SecurityCodeField(blank=True)
    billing_address = AddressField(blank=True)

    class Meta:
        model = Payment
        fields = ['cc_number', 'cc_expiry', 'cc_code', 'billing_address']
        labels = {
            'cc_number': _('Card Number'),
            'cc_expiry': _('Expiration Date'),
            'cc_code': _('CVV/CVC'),
            'billing_address': _('Billing Address')
        }

class UserEditForm(ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        labels = {
            'first_name': _('First Name'),
            'last_name': _('Last Name'),
        }
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user_permissions = self.fields.get('user_permissions')
        if user_permissions:
            user_permissions.queryset = user_permissions.queryset.select_related('content_type')

class ContactEditForm(forms.ModelForm):

    class Meta:
        model = StoreUser
        fields = ['phone_number', 'address', 'subscribed']
        labels = {
            'phone_number': _('Phone Number'),
            'address': _('Shipping Address'),
            'subscribed': _('Subscribe to Promotions')
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user_permissions = self.fields.get('user_permissions')
        if user_permissions:
            user_permissions.queryset = user_permissions.queryset.select_related('content_type')

class BillingEditForm(forms.ModelForm):

    class Meta:
        model = Payment
        fields = ['cc_number', 'cc_expiry', 'cc_code', 'billing_address']
        labels = {
            'cc_number': _('Card Number'),
            'cc_expiry': _('Expiration Date'),
            'cc_code': _('CVV/CVC'),
            'billing_address': _('Billing Address')
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user_permissions = self.fields.get('user_permissions')
        if user_permissions:
            user_permissions.queryset = user_permissions.queryset.select_related('content_type')
