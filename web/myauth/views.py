from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, FormView, UpdateView, CreateView

from django.contrib.auth.views import (
        LoginView,
        LogoutView,
        PasswordResetView,
        PasswordResetConfirmView
    ) 

from django.contrib.auth import get_user_model, authenticate, login
User = get_user_model()


from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse


# from letters.models import Letter
from myauth.forms import  UserCreationForm, UserLoginForm, MyPasswordResetForm
from .tokens import account_activation_token    


class LogupView(FormView):

    template_name   = 'myauth/signup.html'
    form_class      = UserCreationForm
    success_url     = '/'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.clean_password2()
        request = self.request

        user = User.objects.create_user(email, password, is_active = False)

        current_site = get_current_site(request)
        mail_subject = _('Activate your {} account.'.format(current_site))
        
        # try:
        #     letter = Letter.objects.get(featured = True)
        # except Letter.DoesNotExist:
        #     letter = None
        # if letter:
        #     text_content, html_content = letter.text_content, letter.html_content
        # else:
        #     text_content, html_content = (None, None)
            
        activation_link = 'http://{}{}'.format( current_site, user.get_activate_url )

        # html_content = letter.html_content.split('[activation-link]')
        # text_content = letter.text_content.split('[activation-link]')
                                                                          
        # html_message = html_content[0] + activation_link + html_content[1]
        # text_message = text_content[0] + activation_link + text_content[1]

        text_message = activation_link
        to_email = email
        email = EmailMultiAlternatives(
                    mail_subject, text_message, to=[to_email]
        )

        # email.attach_alternative(html_message, "text/html")
        email.send()
        return redirect ('myauth:acc_confirm')
        

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('myauth:link_for_login')
    else:
        return HttpResponse(_('Activation link is invalid!') + 'Активационная ссылка не действительна!')


class MyLoginView(LoginView):
    template_name   = 'myauth/login.html'
    authentication_form = UserLoginForm

    def form_valid(self, form):
        self.form = form
        return super(MyLoginView, self).form_valid( form )

    def get_success_url(self):
        return reverse('home')


class MyLogoutView(LogoutView):
    def get_next_page(self):
        return reverse('home')

class LinkForLogin(TemplateView):
    template_name = 'myauth/link_for_login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_url'] = get_current_site(self.request)
        return context

    def get_success_url(self):
        return reverse('myauth:login')

class MyPasswordResetView(PasswordResetView):
    template_name='myauth/password_reset_form.html'
    form_class = MyPasswordResetForm
    email_template_name = 'myauth/password_reset_email.html'

    def get_success_url(self):
        return reverse('myauth:password_reset_done')

class MyPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'myauth/password_reset_confirm.html'

    def get_success_url(self):
        return reverse('myauth:password_reset_complete')
