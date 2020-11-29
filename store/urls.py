from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required

from . import views

urlpatterns = [
    path('', views.MainView.as_view(), name='store-index'),
    path('search/', views.SearchView.as_view(), name='store-search'),
    path('book/<slug:id>', views.BookView.as_view(), name='store-book'),
    path('cart/', login_required(views.CartView.as_view()), name='store-cart'),
    path('orders/', login_required(views.ManageOrdersView.as_view()), name='store-manageorders'),
    path('books/', login_required(views.AdminManageBooksView.as_view()), name='store-adminmanagebooks'),
    path('users/', login_required(views.AdminManageUsersView.as_view()), name='store-adminmanageusers'),
    path('books/edit-<slug:id>', login_required(views.AdminEditBookView.as_view()), name='store-admineditbook'),
    path('books/new', login_required(views.AdminNewBookView.as_view()), name='store-adminnewbook'),
    path('promotions/', login_required(views.AdminPromosView.as_view()), name='store-adminmanagepromos'),
    path('promotions/new', login_required(views.AdminNewPromoView.as_view()), name='store-adminnewpromo'),
    path('promotions/promo-<slug:code>', login_required(views.AdminEditPromosView.as_view()), name='store-admineditpromos'),
    path('users/edit-<slug:id>', login_required(views.AdminEditUserView.as_view()), name='store-adminedituser'),
    path('checkout/', login_required(views.CheckoutView.as_view()), name='store-checkout'),
    path('order/<slug:order_number>', login_required(views.OrderSummaryView.as_view()), name='store-ordersummary'),      
]
