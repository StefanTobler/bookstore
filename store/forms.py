from django import forms
from django.forms import Form, ModelForm
from django.utils.translation import gettext_lazy as _

from .models import Genre, Book

class EditBookForm(ModelForm):

    class Meta:
        model = Book
        fields = ['title', 'summary', 'stock', 'threshold', 'selling_price', 'featured', 'archived']
        labels = {
            'title': _('Title'),
            'summary': _('Summary'),
        }

class NewBookForm(ModelForm):

    authors = forms.CharField(max_length=1024, help_text='This is a comma seperated list of authors.', widget=forms.TextInput(attrs={'data-role':'tagsinput'}))
    genres = forms.CharField(max_length=1024, help_text='This is a comma seperated list of genres.', widget=forms.TextInput(attrs={'data-role':'tagsinput'}))
    publisher = forms.CharField(max_length=128)
    image = forms.ImageField(required=False)
    class Meta:
        model = Book
        fields = ['image', 'title', 'summary', 'authors', 'genres',
        'publication_year', 'isbn', 'edition', 'publisher', 'stock',
        'threshold', 'selling_price', 'buying_price', 'featured']
        labels = {
            'title': _('Title'),
            'summary': _('Summary'),
            'isbn': _('ISBN'),
        }
