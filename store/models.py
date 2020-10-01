from django.db import models

import hashlib
import uuid

from .validators import *

class Item(models.Model):
    selling_price = models.FloatField(validators=[validate_positive])
    buying_price = models.FloatField(validators=[validate_positive])
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    stock = models.IntegerField(default=0) # If stock is negative there is a backorder
    image = models.ImageField(default='default.jpg', upload_to='item_images')
    archived = models.BooleanField(default=False)
    sold = models.PositiveIntegerField(default=0)
    featured = models.BooleanField(default=True)
    rating = models.FloatField(default=0, validators=[validate_rating])

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
    middle_name = models.CharField(max_length=16, default='')
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
    isbn = models.CharField(max_length=14, validators=[validate_isbn]) # this really needs a validator, you could honesty probably use an API
    edition = models.PositiveIntegerField(default=0)
    publisher = models.ForeignKey(Publisher, on_delete=models.DO_NOTHING, blank=True)

    def __str__(self):
        return self.title
