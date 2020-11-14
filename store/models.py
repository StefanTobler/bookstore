from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

import hashlib
import uuid
from enum import Enum

from address.models import AddressField

from users.models import StoreUser

from .validators import *

class Item(models.Model):
    selling_price = models.FloatField(validators=[validate_positive])
    buying_price = models.FloatField(validators=[validate_positive])
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    stock = models.IntegerField(default=0) # If stock is negative there is a backorder
    image = models.ImageField(default='default.jpg', upload_to='item_images')
    archived = models.BooleanField(default=False)
    sold = models.PositiveIntegerField(default=0)
    featured = models.BooleanField(default=False)
    rating = models.FloatField(default=0, validators=[validate_rating])
    threshold = models.IntegerField(default=2)
    reviews = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True


class Publisher(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Author(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=16)
    middle_name = models.CharField(max_length=16, default='', blank=True)
    last_name = models.CharField(max_length=16)

    def __str__(self):
        return f'{self.first_name} {self.middle_name} {self.last_name}'


class Genre(models.Model):
    id = models.AutoField(primary_key=True)
    genre = models.CharField(max_length=64) # Should this be unique?

    def __str__(self):
        return self.genre


class Book(Item):
    title = models.CharField(max_length=128)
    summary = models.TextField(default='This is a book!')
    authors = models.ManyToManyField(Author) # One book could have many authors
    genres = models.ManyToManyField(Genre)
    publication_year = models.PositiveIntegerField()
    isbn = models.CharField(max_length=14, validators=[validate_isbn], unique=True) # this really needs a validator, you could honesty probably use an API
    edition = models.PositiveIntegerField(default=0)
    publisher = models.ForeignKey(Publisher, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title

class OrderStatus(Enum):
    ORDERED = 'Ordered'
    SHIPPED = 'Shipped'
    DELIVERED = 'Delivered'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

class OrderedBook(models.Model):
    status = models.CharField(max_length=10, choices=OrderStatus.choices(), default=OrderStatus.ORDERED)
    shipping_address = AddressField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} ordered {self.book.title} on {self.date}.'


class Promotion(models.Model):
    DISCOUNT_TYPE = (
        ('P', 'Percentage'),
        ('D', 'Dollar'),
    )
    title = models.CharField(max_length=64, default="New Promotion!")
    expiry = models.DateTimeField()
    code = models.CharField(max_length=20, unique=True)
    discount_type = models.CharField(max_length=1, choices=DISCOUNT_TYPE)
    discount_amount = models.FloatField()

    def __str__(self):
        return f'Promotion {self.code} - {self.title}'


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    promotion = models.ForeignKey(Promotion, null=True, default=None, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.user.username}\'s Cart'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, verbose_name=_('cart'), on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name=_('quantity'))
    book = models.ForeignKey(Book, verbose_name=_('item'), on_delete=models.CASCADE)
