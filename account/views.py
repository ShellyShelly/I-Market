from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import EmailMessage
from django.urls import reverse, reverse_lazy
from django.views import View
from django.contrib import auth
from django.template.context_processors import csrf
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import DetailView, UpdateView

from account.forms import UserSignUpForm, LoginForm, UserForm
from account.tokens import account_activation_token
from account.backends import UserAuth
from account.models import User


# helper method to generate a context csrf_token
# and adding a login form in this context
def create_context_username_csrf(request):
    context = {}
    context.update(csrf(request))
    context['login_form'] = UserAuth
    return context


def activate_account(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.active = True
        user.save()
        auth.login(request, user)
        return render(request, 'account/email_confirmation_is_successful.html')
    else:
        return render(request, 'account/activation_link_is_invalid.html')


class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        return redirect('shop:ProductList')


class LoginView(View):
    def get(self, request):
        # if the user is logged in, then do a redirect to the home page
        if auth.get_user(request).is_authenticated:
            return redirect('shop:ProductList')
        else:
            # Otherwise, form a context with the authorization form
            # and we return to this page context.
            # It works, for url - /admin/login/ and for /accounts/login/
            context = create_context_username_csrf(request)
            form = LoginForm(request.POST or None)
            context['login_form'] = form
            return render(request=request, template_name='account/login.html', context=context)

    def post(self, request):
        # having received the authorization request
        form = LoginForm(request.POST or None)
        # check the correct form, that there is a user and he entered the correct password
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = auth.authenticate(request=request, username=username, password=password)
            if not user:
                return render(request, 'account/invalid_login.html')
            else:
                # if successful authorizing user
                auth.login(request, user)
                #  and if the user of the number of staff and went through url /admin/login/
                # then redirect the user to the admin panel
                if request.user.is_staff or request.user.is_admin:
                    return redirect('/admin/')
                return redirect('shop:ProductList')
        # If not true(form is invalid), then the user will appear on the login page
        # and see an error message
        context = create_context_username_csrf(request)
        context['login_form'] = form
        return render(request=request, template_name='account/login.html', context=context)


class SignupView(View):

    def post(self, request):
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('account/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Activate your BuyBook shop account.'
            to_email = form.cleaned_data.get('email')
            from_email = settings.EMAIL_HOST_USER
            email = EmailMessage(from_email=from_email, subject=mail_subject, body=message, to=[to_email])
            email.send()
            return render(request, 'account/email_is_sent.html')

        return render(request, 'account/sign_up.html', {'signup_form': form})

    def get(self, request):
        form = UserSignUpForm()
        return render(request, 'account/sign_up.html', {'signup_form': form})


class AccountDetailView(DetailView):
    model = User
    template_name = 'account/account_detail.html'

    def get_object(self, queryset=None):
        try:
            user = User.objects.get(pk=queryset)
        except User.DoesNotExist:
            return redirect('shop:ProductList')


class AccountUpdateView(UpdateView):
    model = User
    template_name= 'account/account_update.html'
    form_class = UserForm

    def get_object(self, queryset=None):
        return self.request.user

    def get(self, request, **kwargs):
        self.object = User.objects.get(email=self.request.user)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return redirect(self.get_success_url())

    def get_success_url(self, **kwargs):
        # obj = form.instance or self.object
        return reverse("account:AccountUpdate", kwargs={'pk': self.object.pk})
