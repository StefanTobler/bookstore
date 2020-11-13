from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required

from . import views

urlpatterns = [
    path('', views.MainView.as_view(), name='store-index'),
    path('book/<slug:id>', views.BookView.as_view(), name='store-book'),
    path('cart/', login_required(views.CartView.as_view()), name='store-cart'),
    path('orders/', login_required(views.ManageOrdersView.as_view()), name='store-manageorders'),
    path('managebooks/', login_required(views.AdminManageBooksView.as_view()), name='store-adminmanagebooks'),
    path('editbook/<slug:id>', login_required(views.AdminEditBookView.as_view()), name='store-admineditbook'),
    path('newbook/', login_required(views.AdminNewBookView.as_view()), name='store-adminnewbook'),
]
