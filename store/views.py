from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView

from .models import Book, Genre, Item

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
        return render(request, self.template_name, {})
