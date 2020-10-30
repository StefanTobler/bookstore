from django.contrib import admin
from .models import Profile, StoreUser, Payment

admin.site.register(Profile)
admin.site.register(StoreUser)
admin.site.register(Payment)
