from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import ObjectDoesNotExist



from .forms import UserRegisterForm, StoreUserRegistrationForm, PaymentForm, UserEditForm, ContactEditForm, BillingEditForm
from .models import StoreUser

try:
    from store.models import Book
except ImportError:
    pass

class EditProfileView(TemplateView):

    template_name = "users/profile.html"

    context = {
        'title': 'Your Account'
    }

    def post(self, request, *args, **kwargs):
        user_form = UserEditForm(request.POST, instance=request.user)
        contact_form = ContactEditForm(request.POST, instance=request.user.storeuser)
        billing_form = BillingEditForm(request.POST, instance=request.user.storeuser.payment)
        password_form = PasswordChangeForm(request.user, request.POST)
        if 'first_name' in request.POST:
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Successfully updated profile information.')
                self.notify_user_change(request, request.user)
            else:
                message.error(request, 'Something went wrong when trying to update your information. Try again later.')
        elif 'phone_number' in request.POST:
            store_user = request.user.storeuser
            if contact_form.is_valid():
                contact_form.save()
                messages.success(request, 'Successfully updated contact information.')
                self.notify_user_change(request, request.user)
            else:
                message.error(request, 'Something went wrong when trying to update your information. Try again later.')
        elif 'cc_number' in request.POST:
            if billing_form.is_valid():
                billing_form.save()
                messages.success(request, 'Successfully updated billing information.')
                self.notify_user_change(request, request.user)
            else:
                messages.error(request, 'Something went wrong when trying to update your information. Try again later.')
        elif 'old_password' in request.POST:
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                self.notify_user_change(request, request.user, password=True)
            else:
                messages.error(request, 'Something went wrong when trying to update your information. Try again later.')
        self.context.update({
            'user_form': user_form,
            'contact_form': contact_form,
            'billing_form': billing_form,
            'password_form': password_form,
        })
        return self.get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        user_form = UserEditForm(instance=request.user)
        contact_form = ContactEditForm(instance=request.user.storeuser)
        billing_form = BillingEditForm(instance=request.user.storeuser.payment)
        password_form = PasswordChangeForm(request.user)
        self.context.update({
            'user_form': user_form,
            'contact_form': contact_form,
            'billing_form': billing_form,
            'password_form': password_form,
        })
        return render(request, self.template_name, self.context)

    def notify_user_change(self, request, user, password=False):
        current_site = get_current_site(request)
        mail_subject = 'Password Changed' if password else 'Account Info Change - Bookstore4050'
        template = 'users/password_change.html' if password else 'users/account_change.html'
        message = render_to_string(template, {
                    'user': user
        })
        email = EmailMessage(
                mail_subject, message, to=[user.email]
        )
        email.send()

class LoginView(TemplateView):

    template_name = "users/login.html"

    context = {
        'form': AuthenticationForm,
        'title': 'Login'
    }

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user == None:
            try:
                username = User.objects.get(email=username).username
                user = authenticate(request, username=username, password=password)
            except ObjectDoesNotExist:
                messages.error(request, 'That username and password combination does not exist.')
                return self.get(request, *args, **kwargs)
        try:
            store_user = StoreUser.objects.filter(user=user)[0]
        except IndexError:
            messages.error(request, 'That username and password combination does not exist.')
            return self.get(request, *args, **kwargs)
        if user is not None and store_user.is_active():
            login(request, user)
            return redirect('store-index')
        elif user is not None and storeuser.is_suspended:
            messages.error(request, 'You have been suspended, for questions please email an admin.')
        messages.error(request, 'Please activate your account.')
        return self.get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)

class RegisterView(TemplateView):

    template_name = "users/register.html"

    context = {
        'title': 'Register',
        'static_scripts': ['store/js/register.js']
    }

    def post(self, request, *args, **kwargs):
        user_form = UserRegisterForm(request.POST)
        store_form = StoreUserRegistrationForm(request.POST)
        payment_form = PaymentForm(request.POST)
        if user_form.is_valid() and store_form.is_valid() and payment_form.is_valid():
            user = user_form.save()
            store_user = store_form.save()
            store_user.user = user
            store_user.save()
            payment = payment_form.save()
            payment.user = store_user
            payment.save()
            self.send_confirmation_email(request, store_user)
            messages.success(request, f'An activation email has been sent to {user.email}.')
            return redirect('login')

        self.context.update({
            'user_form': user_form,
            'store_form': store_form,
            'payment_form': payment_form,
        })
        return render(request, self.template_name, self.context)

    def get(self, request, *args, **kwargs):
        user_form = UserRegisterForm()
        store_form = StoreUserRegistrationForm()
        payment_form = PaymentForm()

        self.context.update({
            'user_form': user_form,
            'store_form': store_form,
            'payment_form': payment_form,
        })
        return render(request, self.template_name, self.context)

    def send_confirmation_email(self, request, user):
        token = default_token_generator.make_token(user.user)
        user.activation_token = token
        user.save()
        current_site = get_current_site(request)
        mail_subject = 'Activate Account - Bookstore4050'
        message = render_to_string('users/activate_account.html', {
                'user': user.user,
                'domain': current_site.domain,
                'token': token,
        })
        email = EmailMessage(
                mail_subject, message, to=[user.user.email]
        )
        email.send()
        return

class ConfirmationView(TemplateView):

    template_name = "users/confirmation.html"

    context = {
        'title': 'Confirmation'
    }

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        token = request.GET.get('token', 'none')
        user = get_object_or_404(StoreUser, activation_token=token)
        self.activate(user)
        return render(request, self.template_name, self.context)

    def activate(self, user):
        user.activate()
        user.save()

class AdminView(PermissionRequiredMixin, TemplateView):
    permission_required = 'User.can_edit'
    template_name = "users/admin.html"

    context_object_name = 'books'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['books'] = Book.objects.all()
        kwargs['title'] = 'Admin Panel'
        return kwargs

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())
