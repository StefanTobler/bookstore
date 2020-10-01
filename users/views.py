from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import TemplateView

try:
    from store.models import Book
except ImportError:
    pass


class EditProfileView(TemplateView):

    template_name = "users/profile.html"

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

class LoginView(TemplateView):

    template_name = "users/login.html"

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

class RegisterView(TemplateView):

    template_name = "users/register.html"

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

class ConfirmationView(TemplateView):

    template_name = "users/confirmation.html"

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

class AdminView(TemplateView):

    template_name = "users/admin.html"

    context_object_name = 'books'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['books'] = Book.objects.all()
        return kwargs

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())
