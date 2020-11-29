from django import forms
from django.forms import Form, ModelForm
from django.utils.translation import gettext_lazy as _
from django.contrib.admin.widgets import FilteredSelectMultiple, RelatedFieldWidgetWrapper
from bookstore.logger import LoggerFactory

import datetime
import pytz

from .models import Genre, Book, Author, Promotion, StoreUser, User, Publisher, BookSearch


class BookSearchForm(ModelForm):
    search = forms.CharField(max_length=1024, widget=forms.TextInput(attrs={'placeholder':'Search By Title, Author, Keyword, ISBN...'}), required=False)
    class Meta:
        model = BookSearch
        fields = ['search', 'genre']
        labels = {
            'search': _('Search'),
            'genre': _('Genre'),
            # 'sort_by': _('Sort by'),
        }


class EditBookForm(ModelForm):

    class Meta:
        model = Book
        fields = ['image', 'title', 'summary', 'stock', 'threshold', 'selling_price', 'featured', 'archived']
        labels = {
            'title': _('Title'),
            'summary': _('Summary'),
        }


class EditStoreUserForm(ModelForm):

    class Meta:
        model = StoreUser
        fields = ['status', 'is_employee']
        labels = {
            'status': _('Status'),
            'is_employee': _('Employee'),
        }


class EditUserForm(ModelForm):

    class Meta:
        model = User
        fields = ['is_superuser']
        labels = {
            'is_superuser': _('Admin'),
        }


class NewBookForm(ModelForm):

    authors = forms.CharField(max_length=1024, help_text='This is a comma seperated list of authors.', widget=forms.TextInput(attrs={'data-role':'tagsinput'}))
    genres = forms.CharField(max_length=1024, help_text='This is a comma seperated list of genres.', widget=forms.TextInput(attrs={'data-role':'tagsinput'}))
    image = forms.ImageField(required=False)
    publisher = forms.MultipleChoiceField(required=False)

    def clean_publisher(self):
        return Publisher.objects.all()[0]

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

class NewPromoForm(ModelForm):

    expiry = forms.DateTimeField(
        widget=forms.TextInput(
            attrs={'type': 'datetime-local'}
    ))

    def clean_expiry(self):
        # First make the time string a datetime
        #time = datetime.datetime.strptime(self.cleaned_data['expiry'], '%Y-%m-%dT%H:%M')
        utc=pytz.UTC
        expiry = self.cleaned_data['expiry'].replace(tzinfo=utc)
        now = datetime.datetime.now().replace(tzinfo=utc)
        if expiry < now:
             raise forms.ValidationError('Promotion cannot expire in the past!')
        return expiry

    def clean_discount_amount(self):
        discount_type = self.cleaned_data['discount_type']
        discount_amount = self.cleaned_data['discount_amount']
        if discount_type == 'P' and discount_amount > 100:
            raise forms.ValidationError('Discount amount cannot be more than 100%')
        return discount_amount

    class Meta:
        model = Promotion
        fields = ['title', 'expiry', 'code', 'discount_type', 'discount_amount']
        labels = {
            'title': _('Title'),
            'discount_type': _('Discount Type'),
            'discount_amount': _('Discount Amount'),
        }
