from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='users-register'),
    path('login/', views.LoginView.as_view(), name='users-login'),
    path('confirm/', views.ConfirmationView.as_view(), name='users-confirmation'),
    path('edit/', views.EditProfileView.as_view(), name='users-editprofile'),
    path('admin/', views.AdminView.as_view(), name='users-admin'),
]
