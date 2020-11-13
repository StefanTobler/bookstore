from django import forms
from django.forms import Form
from django.utils.translation import gettext_lazy as _

from .models import Genre

class AdminBookLookupForm(Form):

    title = forms.CharField(max_length=128, required=False)
    isbn = forms.CharField(max_length=14, required=False)
    author = forms.CharField(max_length=64, required=False)
    genre = forms.ChoiceField(choices=[('','')] + [(x, x) for x in Genre.objects.all()], required=False)


class AdminUserLookupForm(Form):

    phone_number = forms.CharField(max_length=128, required=False)
    username = forms.CharField(max_length=128, required=False)
