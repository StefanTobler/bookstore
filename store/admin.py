from django.contrib import admin
from .models import *
from .forms import *

# Register your models here.
# class BookAdmin(admin.ModelAdmin):
#     form = NewBookForm

admin.site.register(Book)
admin.site.register(Publisher)
admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(Order)
admin.site.register(Promotion)
admin.site.register(Cart)
admin.site.register(CartItem)
