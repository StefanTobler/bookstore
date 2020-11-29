from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from bookstore.logger import LoggerFactory
from django.db.models.signals import post_save, pre_save

import hashlib
import uuid
from enum import Enum

from address.models import AddressField

from users.models import StoreUser

from .validators import *

from .utils import *


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

    def sell_item(self, amount):
        self.stock -= amount
        self.sold += amount
        self.save()

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
    isbn = models.CharField(max_length=14, validators=[validate_isbn], unique=True) # this really needs a validator, you could honestly probably use an API
    edition = models.PositiveIntegerField(default=0)
    publisher = models.ForeignKey(Publisher, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title

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

class Order(models.Model):

    ORDERED = 'Ordered'
    SHIPPED = 'Shipped'
    DELIVERED = 'Delivered'

    CHOICES = [
        (ORDERED, ORDERED),
        (SHIPPED, SHIPPED),
        (DELIVERED, DELIVERED)
    ]

    order_id= models.CharField(max_length=120, blank=True)
    status = models.CharField(max_length=10, choices=CHOICES, default=ORDERED)
    shipping_address = AddressField()
    user = models.ForeignKey(StoreUser, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    promotion = models.ForeignKey(Promotion, null=True, default=None, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'Order {self.order_id} - {self.user.user.username}'

    def get_items(self):
        return OrderedBook.objects.filter(order=self)

class OrderedBook(models.Model):
    order = models.ForeignKey(Order, verbose_name=_('order'), on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name=_('quantity'))
    book = models.ForeignKey(Book, verbose_name=_('item'), on_delete=models.CASCADE)
    price = models.FloatField()

    def __str__(self):
        return self.book.title

    def to_cart_item(self, cart):
        cart_item = CartItem(cart=cart, quantity=self.quantity, book=self.book)
        cart_item.save()
        return cart_item

class Cart(models.Model):
    user = models.OneToOneField(StoreUser, on_delete=models.CASCADE)
    promotion = models.ForeignKey(Promotion, null=True, default=None, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.user.user.username}\'s Cart'

    def remove_promotion(self):
        self.promotion = None
        self.save()

    def empty(self):
        items = CartItem.objects.filter(cart=self)
        items.delete()

    def add_order(self, order):
        items = order.get_items()
        for item in items:
            item.to_cart_item(self)
        return

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, verbose_name=_('cart'), on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name=_('quantity'))
    book = models.ForeignKey(Book, verbose_name=_('item'), on_delete=models.CASCADE)

    def set_quantity(self, amount):
        self.quantity = amount

    def increment_quantity(self):
        self.quantity += 1

    def to_ordered_book(self, order):
        ordered_book = OrderedBook(order=order, quantity=self.quantity, book=self.book, price=self.book.selling_price)
        ordered_book.save()
        return ordered_book

    def __str__(self):
        return self.book.title + ' ' + str(self.quantity)

class SortBy(Enum):

    TITLE = "Title"
    GENRE = "Genre"
    ISBN = "ISBN"
    AUTHOR = "Author"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class BookSearch(models.Model):
    search = models.CharField(max_length=120, blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.DO_NOTHING, blank=True)
    sort_by = models.CharField(max_length=10, choices=SortBy.choices(), default=SortBy.TITLE)

def create_user_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)

post_save.connect(create_user_cart, sender=StoreUser)

def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id= unique_order_id_generator(instance)

pre_save.connect(pre_save_create_order_id, sender=Order)

def get_cart_totals(cart, tax_rate=.07):
    cart_items = CartItem.objects.filter(cart=cart)
    subtotal = 0
    for cart_item in cart_items:
        subtotal += cart_item.book.selling_price * cart_item.quantity

    taxes = subtotal * .07
    total = taxes + subtotal
    return ("{:.2f}".format(subtotal), "{:.2f}".format(taxes), "{:.2f}".format(total))

def get_order_totals(order, tax_rate=.07):
    order_items = OrderedBook.objects.filter(order=order)
    subtotal = 0
    for order_item in order_items:
        subtotal += order_item.price * order_item.quantity

    taxes = subtotal * .07
    total = taxes + subtotal
    return ("{:.2f}".format(subtotal), "{:.2f}".format(taxes), "{:.2f}".format(total))
