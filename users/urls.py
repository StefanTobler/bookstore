from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('confirm/', views.ConfirmationView.as_view(), name='users-confirmation'),
    path('edit/', login_required(views.EditProfileView.as_view()), name='users-editprofile'),
    path('admin/', views.AdminView.as_view(), name='users-admin'),
]
