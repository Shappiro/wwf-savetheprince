from __future__ import unicode_literals
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import get_user_model
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView,PasswordResetDoneView, PasswordResetConfirmView
from braces import views as bracesviews
from django.conf import settings
from dal import autocomplete
from . import forms
from wwf_prince.utils import PROVINCIA_CHOICES

User = get_user_model()

app_name = __package__


class LoginView(bracesviews.AnonymousRequiredMixin,
                LoginView):
    template_name = app_name + "/login.html"
    form_class = forms.LoginForm

    def form_valid(self, form):
        redirect = super().form_valid(form)
        remember_me = form.cleaned_data.get('remember_me')
        if remember_me is True:
            ONE_MONTH = 30 * 24 * 60 * 60
            expiry = getattr(settings, "KEEP_LOGGED_DURATION", ONE_MONTH)
            self.request.session.set_expiry(expiry)
        return redirect


class LogoutView(LogoutView):
    url = reverse_lazy('home')


class SignUpView(bracesviews.AnonymousRequiredMixin,
                 bracesviews.FormValidMessageMixin,
                 generic.CreateView):
    form_class = forms.SignupForm
    model = User
    template_name = app_name + '/signup.html'
    success_url = reverse_lazy('home')
    form_valid_message = "Ti sei iscritto!"

    def form_valid(self, form):
        r = super().form_valid(form)
        username = form.cleaned_data["email"]
        password = form.cleaned_data["password1"]
        user = auth.authenticate(email=username, password=password)
        auth.login(self.request, user)
        return r


class PasswordChangeView(PasswordChangeView):
    form_class = forms.PasswordChangeForm
    template_name = app_name + '/password-change.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.save()
        messages.success(self.request,
                         "La tua password è stata cambiata, "
                         "quindi sei stato disconnesso. Per favore rieffettua il login.")
        return super().form_valid(form)


class PasswordResetView(PasswordResetView):
    form_class = forms.PasswordResetForm
    template_name = app_name + '/password-reset.html'
    success_url = reverse_lazy('accounts:password-reset-done')
    subject_template_name = app_name + '/emails/password-reset-subject.txt'
    email_template_name = app_name + '/emails/password-reset-email.html'


class PasswordResetDoneView(PasswordResetDoneView):
    template_name = app_name + '/password-reset-done.html'


class PasswordResetConfirmView(PasswordResetConfirmView):
    template_name = app_name + '/password-reset-confirm.html'
    form_class = forms.SetPasswordForm
    success_url = reverse_lazy('home')


class ProvincesAutoComplete(autocomplete.Select2ListView):
    def get_list(self):
        return [a[0] for a in PROVINCIA_CHOICES]
