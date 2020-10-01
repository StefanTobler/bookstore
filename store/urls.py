from django.urls import path

from . import views

urlpatterns = [
    path('', views.MainView.as_view(), name='store-index'),
    path('book/<slug:id>', views.BookView.as_view(), name='store-book'),
    path('cart/', views.CartView.as_view(), name='store-cart'),
    path('user/orders/', views.ManageOrdersView.as_view(), name='store-manageorders'),
]
