from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q, F
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.datastructures import MultiValueDictKeyError
from django.db.models.functions import Lower
from bookstore.logger import LoggerFactory

from random import shuffle
from threading import Thread
import sys
import datetime
import pytz
from copy import copy
from time import sleep


from .models import *
from .forms import EditBookForm, NewBookForm, NewPromoForm, EditStoreUserForm, EditUserForm, BookSearchForm

factory = LoggerFactory()
info_logger = factory.get_logger('INFO')


class MainView(TemplateView):

    template_name = "store/index.html"

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        print()
        url_request = request.GET.urlencode()

        if url_request != "":
            return redirect('/search?' + url_request)

        form = BookSearchForm()
        avaliable_books = Book.objects.filter(archived=False)
        paginator = Paginator(avaliable_books, 10)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        context = {
            'top_rated': avaliable_books.order_by('-sold')[:10],
            'featured': avaliable_books.filter(featured=True).all()[:10],
            'genres': Genre.objects.order_by('genre'),
            'page_obj': page_obj,
            'form': form,
        }
        return render(request, self.template_name, context)


class SearchView(TemplateView):

    template_name = "store/search.html"

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        print()
        search = request.GET.get('search', '')
        genre = request.GET.get('genre', '')
        sort_by = request.GET.get('sort_by', '')
        info_logger.log(f"User searched for: {search}")
        form = BookSearchForm()

        true_q = ~Q(pk__in=[])
        genre_q = true_q
        if genre != '':
            genre_q = Q(genres__in=[genre])

        available_authors = Author.objects.filter(Q(first_name__icontains=str(search)) |
            Q(middle_name__icontains=str(search)) | Q(last_name__icontains=str(search)))
        avaliable_books = Book.objects.filter(genre_q & (Q(title__icontains=str(search)) |
            Q(authors__in=available_authors) | Q(isbn__icontains=str(search))), archived=False).distinct()

        if sort_by == 'TITLE':
            avaliable_books = avaliable_books.order_by(Lower('title'))
        elif sort_by == 'GENRE':
            avaliable_books = avaliable_books.order_by(Lower('genre'))
        elif sort_by == 'ISBN':
            avaliable_books = avaliable_books.order_by(Lower('isbn'))
        elif sort_by == 'AUTHOR':
            avaliable_books = avaliable_books.order_by(Lower('authors'))

        paginator = Paginator(avaliable_books, 10)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        context = {
            'genres': Genre.objects.order_by('genre'),
            'page_obj': page_obj,
            'form': form,
            'search': str(search),
        }
        return render(request, self.template_name, context)


class BookView(TemplateView):

    template_name = "store/book.html"

    def post(self, request, id, *args, **kwargs):
        book = get_object_or_404(Book, id=id)
        user = request.user
        cart = user.storeuser.cart
        cart_items = CartItem.objects.filter(cart=cart)
        cart_item = cart_items.filter(book=book)
        try:
            if len(cart_items.filter(book=book)) == 0:
                cart_item = CartItem(cart=cart, quantity=1, book=book)
                cart_item.save()
                messages.success(request, f'{book.title} added to cart!')
            else:
                print('UPDATING quantity')
                cart_item.update(quantity=F('quantity') + 1)
                messages.success(request, f'{book.title} added to cart!')
        except:
            messages.error(request, 'Looks like an error occured, try again later.')
            info_logger.log(sys.exc_info()[0])

        context = {
            'book': book,
        }
        return render(request, self.template_name, context)


    def get(self, request, id, *args, **kwargs):
        book = get_object_or_404(Book, id=id)
        context = {
            'book': book,
        }
        return render(request, self.template_name, context)

class CartView(TemplateView):

    template_name = "store/cart.html"

    def post(self, request, *args, **kwargs):
        try:
            cart_item = CartItem.objects.filter(cart=request.user.storeuser.cart, book=request.POST['book_id'])
            if int(request.POST['qty']) > 0:
                cart_item.update(quantity=request.POST['qty'])
            else:
                messages.success(request, f'{cart_item[0].book.title} removed from cart.')
                cart_item.delete()
        except:
            messages.error(request, 'Looks like an error occured, try again later.')
        return self.get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        cart_items = CartItem.objects.filter(cart=request.user.storeuser.cart)
        totals = get_cart_totals(request.user.storeuser.cart)
        out_of_stock = False
        out_books = []
        for item in cart_items:
            if item.book.stock <= 0 or item.quantity > item.book.stock:
                out_of_stock = True
                out_books.append(item.book)
        context = {
            'title': 'Cart',
            'cart_items': cart_items,
            'subtotal': totals[0],
            'taxes': totals[1],
            'total': totals[2],
            'out_of_stock': out_of_stock,
            'out_books': out_books
        }
        return render(request, self.template_name, context)

class CheckoutView(TemplateView):

    template_name="store/checkout.html"

    def post(self, request, *args, **kwargs):
        code = request.POST['promo']
        promo = Promotion.objects.filter(code=code)
        utc=pytz.UTC
        if len(promo) < 1:
            messages.error(request, 'That promotion does not exist.')
        elif promo[0].expiry < datetime.datetime.now(tz=utc):
            messages.error(request, 'That promotion has already expired.')
        else:
            request.user.storeuser.cart.promotion = promo[0]
            messages.success(request, 'Promotion applied!')
        return self.get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        cart_items = CartItem.objects.filter(cart=request.user.storeuser.cart)
        promotion = request.user.storeuser.cart.promotion
        totals = get_cart_totals(request.user.storeuser.cart)
        out_cart_items = cart_items.filter(book__stock__lt=1).delete()
        context = {
            'title': 'Checkout',
            'cart_items': cart_items,
            'subtotal': totals[0],
            'taxes': totals[1],
            'total': totals[2],
            'promo': promotion
        }
        return render(request, self.template_name, context)

class OrderSummaryView(TemplateView):

    template_name = "store/order_summary.html"

    context = {}

    def post(self, request, order_number, *args, **kwargs):
        if not request.user.storeuser.address or not request.user.storeuser.payment:
           messages.error(request, 'Please enter valid payment or shipping information.')
           return redirect('store-checkout')
        if order_number == 'new':
            cart = request.user.storeuser.cart
            cart_items = CartItem.objects.filter(cart=cart)

            shipping_address = copy(request.user.storeuser.address)
            shipping_address.pk = None
            shipping_address.save()

            order = Order(
                    shipping_address=shipping_address,
                    user=request.user.storeuser,
                    promotion=cart.promotion
            )
            order.save()

            for item in cart_items:
                item.to_ordered_book(order)
                item.book.sell_item(item.quantity)
            order_number = order.order_id
            cart_items.delete()
            cart.remove_promotion()
            Thread(target=self.deliver_order, args=(order, )).start()

        return redirect('store-ordersummary', order_number=order_number)

    def get(self, request, order_number, *args, **kwargs):
        order = get_object_or_404(Order, user=request.user.storeuser, order_id=order_number)
        order_items = OrderedBook.objects.filter(order=order)

        totals = get_order_totals(order)
        promotion = order.promotion

        self.context.update({
        'title': 'Order Summary - ' + order_number,
        'order': order,
        'order_items': order_items,
        'subtotal': totals[0],
        'taxes': totals[1],
        'total': totals[2],
        'promo': promotion
        })
        return render(request, self.template_name, self.context)

    def deliver_order(self, order):
        sleep(20)
        order.status = Order.SHIPPED
        order.save()
        sleep(20)
        order.status = Order.DELIVERED
        order.save()
        return

class ManageOrdersView(TemplateView):

    template_name = "store/manageorders.html"

    def post(self, request, *args, **kwargs):
        order = get_object_or_404(Order, user=request.user.storeuser, order_id=request.POST['order_id'])
        cart = request.user.storeuser.cart
        cart.empty()
        cart.add_order(order)
        return redirect('store-cart')

    def get(self, request, *args, **kwargs):
        user = request.user.storeuser
        orders = Order.objects.filter(user=user)
        current_orders = orders.filter(Q(status=Order.SHIPPED) | Q(status=Order.ORDERED))
        print(current_orders)
        past_orders = orders.filter(status=Order.DELIVERED)
        context = {
            'title': 'Manage Orders',
            'current_orders': current_orders,
            'past_orders': past_orders,
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

class AdminManageUsersView(AdminView, TemplateView):

    template_name = "store/admin_manage_users.html"

    context = {
        'title': 'Manage Users'
    }

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)

    def get(self, request, *args, **kwargs):
        self.context.update({
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
            b = form.save(commit=False)
            try:
                image = request.FILES['image']
            except MultiValueDictKeyError:
                image = book.image
            b.image = image
            b.save()
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
            'userstore': user,
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
            'storeuser': user,
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
            book = self.book_from_form(request, form)
            book.save()
            for author in self.get_authors(form.data['authors']):
                book.authors.add(author, author.pk)
            for genre in self.get_genres(form.data['genres']):
                book.genres.add(genre)
            book.save()
            messages.success(request, f'Successfully added {form.data["title"]}.')
            return redirect('store-adminmanagebooks')
        messages.error(request, f'Looks like something went wrong, check your input and please try again.')
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

    def book_from_form(self, request, form):
        try:
            image = request.FILES['image']
        except MultiValueDictKeyError:
            image = 'default.jpg'
        return Book(
            image=image,
            title=form.data['title'],
            summary=form.data['summary'],
            publication_year=form.data['publication_year'],
            isbn=form.data['isbn'],
            edition=form.data['edition'],
            stock=form.data['stock'],
            publisher=self.get_publisher(request.POST['publisher_placeholder']),
            threshold=form.data['threshold'],
            selling_price=form.data['selling_price'],
            buying_price=form.data['buying_price'],
            # featured=form.data['featured']
        )

    def get_publisher(self, publisher):
        publisher = publisher.title().strip()
        try:
            return Publisher.objects.get(name=publisher)
        except ObjectDoesNotExist:
            publisher = Publisher(name=publisher)
            publisher.save()
            return publisher

    def get_genres(self, genres):
        genres = genres.split(',')
        for i, genre in enumerate(genres):
            print("Before:", genre)
            genre = genre.strip().capitalize()
            print("After:", genre)
            try:
                genres[i] = Genre.objects.get(genre=genre)
            except ObjectDoesNotExist:
                genres[i] = Genre(genre=genre)
                genres[i].save()
        return genres

    def get_authors(self, authors):
        real_authors = []
        authors = authors.split(',')
        for i, author in enumerate(authors):
            author = author.title().split()
            if len(author) > 0:
                first_name = author[0]
                if len(author) == 1:
                    last_name = ''
                    middle_name = ''
                elif len(author) == 2:
                    last_name = author[1]
                    middle_name = ''
                elif len(author) == 3:
                    middle_name = author[1]
                    last_name = author[-1]
                elif len(author) > 3:
                    last_name = author[-1]
                    middle_name = ''
                    for j in range(1, len(author)-1):
                        middle_name += author[j]
                else:
                    last_name = ''
                    middle_name = ''
                try:
                    db_author = Author.objects.get(first_name=first_name,
                                                      middle_name=middle_name,
                                                      last_name=last_name)
                except ObjectDoesNotExist:
                    db_author = Author(first_name=first_name,
                                        middle_name=middle_name,
                                        last_name=last_name)
                    db_author.save()
                real_authors.append(db_author)
        return real_authors

class AdminPromosView(AdminView, TemplateView):

    template_name = "store/admin_promos.html"

    context = {
        'title': 'Promotions'
    }

    def post(self, request, *args, **kwargs):
        return self.get(request, args, kwargs)

    def get(self, request, *args, **kwargs):
        self.context.update({
            'promos': Promotion.objects.all()
        })
        return render(request, self.template_name, self.context)

class AdminNewPromoView(AdminView, TemplateView):

    template_name = "store/admin_new_promo.html"

    context = {
        'title': 'Create Promotion',
        'button': 'Create and Send'
    }

    def post(self, request, *args, **kwargs):
        form = NewPromoForm(request.POST)
        if form.is_valid():
            form.save()
            Thread(target=self.send_promo, args=(form, )).start()
            messages.success(request, f'{form.data["title"]} added!')
            return redirect('store-adminmanagepromos')
        self.context.update({
            'form': form,
        })
        return render(request, self.template_name, self.context)

    def get(self, request, *args, **kwargs):
        form = NewPromoForm()
        self.context.update({
            'form': form,
        })
        return render(request, self.template_name, self.context)

    def send_promo(self, form):
        mail_subject = f'{form.data["title"]} - Bookstore4050'
        expiry = form.data['expiry']
        title = form.data['title']
        code = form.data['code']
        discount_type = form.data['discount_type']
        discount_amount = form.data['discount_amount']
        users = StoreUser.objects.filter(subscribed=True)
        for user in users:
            message = render_to_string('store/promotion.html', {
                    'user': user.user,
                    'expiry': expiry,
                    'title': title,
                    'code': code,
                    'discount_type': discount_type,
                    'discount_amount': discount_amount,
            })
            email = EmailMessage(
                    mail_subject, message, to=[user.user.email]
            )
            email.send()
        return

class AdminEditPromosView(AdminView, TemplateView):

    template_name = "store/admin_new_promo.html"

    context = {
        'title': 'Edit Promotion',
        'button': 'Update'
    }

    def post(self, request, *args, **kwargs):
        promo = get_object_or_404(Promotion, code=kwargs.get('code'))
        form = NewPromoForm(request.POST, instance=promo)
        if form.is_valid():
            form.save()
            messages.success(request, f'{promo.title} updated!')
            return redirect('store-adminmanagepromos')
        self.context.update({
            'form': form,
        })
        return render(request, self.template_name, self.context)

    def get(self, request, *args, **kwargs):
        promo = get_object_or_404(Promotion, code=kwargs.get('code'))
        form = NewPromoForm(instance=promo)
        self.context.update({
            'form': form,
        })
        return render(request, self.template_name, self.context)
