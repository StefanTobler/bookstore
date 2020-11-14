from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist

from random import shuffle

from .models import *
from .forms import EditBookForm, NewBookForm, EditStoreUserForm, EditUserForm

class MainView(TemplateView):

    template_name = "store/index.html"

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):
        avaliable_books = Book.objects.filter(archived=False)
        paginator = Paginator(avaliable_books, 10)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        context = {
            'top_rated': avaliable_books.order_by('-sold')[:10],
            'featured': avaliable_books.filter(featured=True).all()[:10],
            'genres': Genre.objects.order_by('genre'),
            'page_obj': page_obj,
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
class AdminView(PermissionRequiredMixin):
    permission_required = 'User.can_edit'

class AdminManageBooksView(AdminView, TemplateView):
    template_name = "store/admin_manage_books.html"

    context = {
        'title': 'Manage Books'
    }

    def post(self, request, *args, **kwargs):
        delete = request.POST.get('delete')
        restock = request.POST.get('restock')
        return render(request, self.template_name, self.context)

    def get(self, request, *args, **kwargs):
        self.context.update({
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
        # lookup_form = AdminBookLookupForm(request.POST)
        # matched_users = StoreUser.objects.filter(
        #                                     phone_number__contains=lookup_form.data['phone_number'],
        #                                     username__contains=lookup_form.data['username'],
        # ).distinct()

        # if not len(matched_users):
        #     self.context.update({
        #     'form': lookup_form
        #     })
        #     messages.error(request, 'No users matching the given criteria were found.')
        # else:
        #     # try:
        #     #     # Delete the form if it is present
        #     #     del self.context['form']
        #     # except KeyError:
        #     #     pass
        #     self.context.update({
        #         'users': matched_users
        #     })
        return render(request, self.template_name, self.context)

    def get(self, request, *args, **kwargs):
        # lookup_form = AdminBookLookupForm()
        self.context.update({
            # 'form': lookup_form,
            'users': StoreUser.objects.all()
        })
        return render(request, self.template_name, self.context)

class AdminEditBookView(AdminView, TemplateView):

    template_name = "store/admin_edit_book.html"

    context = {}

    def post(self, request, *args, **kwargs):
        book = get_object_or_404(Book, id=kwargs.get('id'))
        form = EditBookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, f'Book successfully updated!')
        else:
            messages.error(request, 'Looks like something went wrong. Try again later or contact support.')
        self.context.update({
            'book': book,
            'title': 'Edit - ' + book.title,
            'form': form,
        })
        return render(request, self.template_name, self.context)

    def get(self, request, *args, **kwargs):
        book = get_object_or_404(Book, id=kwargs.get('id'))
        form = EditBookForm(initial=book.__dict__)
        self.context.update({
            'book': book,
            'title': 'Edit - ' + book.title,
            'form': form,
        })
        return render(request, self.template_name, self.context)


class AdminEditUserView(AdminView, TemplateView):

    template_name = "store/admin_edit_user.html"

    context = {}

    def post(self, request, *args, **kwargs):
        user = StoreUser.objects.filter(user__id=kwargs.get('id')).get()
        form = EditStoreUserForm(request.POST, instance=user)
        form2 = EditUserForm(request.POST, instance=user.user)
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            messages.success(request, f'User successfully updated!')
        else:
            messages.error(request, 'Looks like something went wrong. Try again later or contact support.')
        self.context.update({
            'user': user,
            'title': 'Edit - ' + user.user.username,
            'form': form,
            'form2': form2,
        })
        return render(request, self.template_name, self.context)

    def get(self, request, *args, **kwargs):
        user = StoreUser.objects.filter(user__id=kwargs.get('id')).get()
        form = EditStoreUserForm(initial=user.__dict__)
        form2 = EditUserForm(initial=user.user.__dict__)
        self.context.update({
            'user': user,
            'title': 'Edit - ' + user.user.username,
            'form': form,
            'form2': form2,
        })
        return render(request, self.template_name, self.context)


class AdminNewBookView(AdminView, TemplateView):

    template_name = "store/admin_new_book.html"

    context = {
        'title': 'New Book'
    }

    def post(self, request, *args, **kwargs):
        form = NewBookForm(request.POST)
        if form.is_valid():
            book = self.book_from_form(form)
        self.context.update({
            'form': form,
        })
        return render(request, self.template_name, self.context)

    def get(self, request, *args, **kwargs):
        form = NewBookForm()
        self.context.update({
            'form': form,
        })
        return render(request, self.template_name, self.context)

    def book_from_form(self, form):
        return Book(
            image=form.data['image'],
            title=form.data['title'],
            summary=form.data['summary'],
            authors=self.get_authors(form.data['authors']),
            genres=self.get_genres(form.data['genres']),
            publication_year=form.data['publication_year'],
            isbn=form.data['isbn'],
            edition=form.data['edition'],
            publisher=self.get_publisher(form.data['publisher']),
            threshold=form.data['threshold'],
            selling_price=form.data['selling_price'],
            buying_price=form.data['buying_price'],
            # featured=form.data['featured']
        )

    def get_publisher(self, publisher):
        publisher = publisher.title()
        try:
            return Publisher.objects.get(name=publisher)
        except ObjectDoesNotExist:
            return Publisher(name=publisher)

    def get_genres(self, genres):
        genres = genres.split(',')
        for i, genre in enumerate(genres):
            genre = genre.capitalize()
            try:
                genres[i] = Genre.objects.get(genre=genre)
            except ObjectDoesNotExist:
                genres[i] = Genre(genre=genre)
        return genres

    def get_authors(self, authors):
        real_authors = []
        authors = authors.split(',')
        for i, author in enumerate(authors):
            author = author.title().split()
            if len(author) > 0:
                first_name = author[0]
                if len(authors) == 3:
                    middle_name = author[1]
                    last_name = author[-1]
                elif len(author) > 3:
                    last_name = author[-1]
                    middle_name = ''
                    for j in range(1, len(author)-1):
                        middle_name += author[j]
                elif len(author) == 1:
                    last_name = ''
                    middle_name = ''
                else:
                    last_name = author[1]
                    middle_name = ''
                try:
                    db_author = Author.objects.get(first_name=first_name,
                                                      middle_name=middle_name,
                                                      last_name=last_name)
                except ObjectDoesNotExist:
                    db_author = Author(first_name=first_name,
                                        middle_name=middle_name,
                                        last_name=last_name)
                real_authors.append(db_author)
        return real_authors
