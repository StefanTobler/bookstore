from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.db.models import Q

from .models import *

from .forms import AdminBookLookupForm

class MainView(TemplateView):

    template_name = "store/index.html"

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):
        context = {
            'top_rated': Book.objects.order_by('-rating')[:10],
            'featured': Book.objects.filter(featured=True).all()[:10],
            'genres': Genre.objects.order_by('genre')
        }
        return render(request, self.template_name, context)

class BookView(TemplateView):

    template_name = "store/book.html"

    def post(self, request, id, *args, **kwargs):
        return self.get(request, id, *args, **kwargs)


    def get(self, request, id, *args, **kwargs):
        book = get_object_or_404(Book, id=id)
        context = {
            'book': book,
        }
        return render(request, self.template_name, context)

class CartView(TemplateView):

    template_name = "store/cart.html"

    def post(self, request, *args, **kwargs):
        return self.get(request, id_url, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {
            'books': Book.objects.filter(publication_year__lte=2014)
        }
        return render(request, self.template_name, context)

class ManageOrdersView(TemplateView):

    template_name = "store/manageorders.html"

    def post(self, request, *args, **kwargs):
        return self.get(request, id_url, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        user = request.user
        orders = OrderedBook.objects.filter(user=user)
        test = orders.filter(status=OrderStatus.SHIPPED)
        print(orders)
        print(test)
        current_orders = orders.filter(Q(status=OrderStatus.SHIPPED) | Q(status=OrderStatus.ORDERED))
        print(current_orders)
        past_orders = orders.filter(status=OrderStatus.DELIVERED)
        context = {
            'current_orders': orders,
            'past_orders': orders,
        }
        return render(request, self.template_name, context)

class AdminManageBooksView(PermissionRequiredMixin, TemplateView):
    permission_required = 'User.can_edit'
    template_name = "store/admin_manage_books.html"

    context = {
        'title': 'Manage Books'
    }

    def post(self, request, *args, **kwargs):
        lookup_form = AdminBookLookupForm(request.POST)
        # TODO: Filter by Author
        matched_books = Book.objects.filter(
                                            title__contains=lookup_form.data['title'],
                                            isbn__contains=lookup_form.data['isbn'],
                                            genres__genre__contains=lookup_form.data['genre'],

        ).distinct()
        # print('TITLE', lookup_form['title'], 'TYPE=', type(lookup_form['title']))
        # print('ISBN', lookup_form['isbn'], 'TYPE=', type(lookup_form['isbn']))
        # print('GENRE', lookup_form['genre'], 'TYPE=', type(lookup_form['genre']))
        #print('QUERY SET', matched_books)
        if not len(matched_books):
            self.context.update({
            'form': lookup_form
            })
            messages.error(request, 'No books matching the given criteria were found.')
        else:
            # try:
            #     # Delete the form if it is present
            #     del self.context['form']
            # except KeyError:
            #     pass
            self.context.update({
                'books': matched_books
            })
        return render(request, self.template_name, self.context)

    def get(self, request, *args, **kwargs):
        lookup_form = AdminBookLookupForm()
        self.context.update({
        'form': lookup_form,
        'books': Book.objects.all()
        })
        return render(request, self.template_name, self.context)


class AdminManageUsersView(PermissionRequiredMixin, TemplateView):
    permission_required = 'User.can_edit'
    template_name = "store/admin_manage_users.html"

    context = {
        'title': 'Manage Users'
    }

    def post(self, request, *args, **kwargs):
        lookup_form = AdminBookLookupForm(request.POST)
        matched_users = StoreUser.objects.filter(
                                            phone_number__contains=lookup_form.data['phone_number'],
                                            username__contains=lookup_form.data['username'],
        ).distinct()

        if not len(matched_users):
            self.context.update({
            'form': lookup_form
            })
            messages.error(request, 'No users matching the given criteria were found.')
        else:
            # try:
            #     # Delete the form if it is present
            #     del self.context['form']
            # except KeyError:
            #     pass
            self.context.update({
                'users': matched_users
            })
        return render(request, self.template_name, self.context)

    def get(self, request, *args, **kwargs):
        lookup_form = AdminBookLookupForm()
        self.context.update({
            'form': lookup_form,
            'users': StoreUser.objects.all()
        })
        return render(request, self.template_name, self.context)
