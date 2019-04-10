from django.urls import path, reverse
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetView
from django.views.generic import TemplateView

from .forms import (
    UserLoginForm,
    MyPasswordResetForm,

)
from . import views
# from .decorators import check_recaptcha


app_name = 'myauth'


urlpatterns = [

    path('signup/',
        views.LogupView.as_view(),
        name="signup",
        ),  
    path(
        'linkforlogin/',
        views.LinkForLogin.as_view(),
        name='link_for_login' 
        ),
    path(
        'login/',
        views.MyLoginView.as_view(),
        name="login",
    ),
    path('activateconfirm/',
            TemplateView.as_view(
                template_name = 'myauth/acc_confirm.html',
            ),
            name='acc_confirm' 
    ),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
  
    path('logout/', views.MyLogoutView.as_view(), name="logout",),

    # path('logout-then-login/', auth_views.logout_then_login, name='logout_then_login'), 


    path(
        'change-password/',
        # auth_views.PasswordChangeView.as_view(),
        auth_views.PasswordChangeView.as_view(template_name='myauth/password_change_form.html'),
        name = 'change_password'
        ),
    path('password_change/done/',
        auth_views. PasswordChangeDoneView.as_view(template_name='myauth/password_change_done.html'),
        name='password_change_done'
        ),
    path(
        'password_reset/',
        views.MyPasswordResetView.as_view(),
        name='password_reset'
        ),
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='myauth/password_reset_done.html'),
        name='password_reset_done'
        ),
    path(
        'reset/<uidb64>/<token>/',
        views.MyPasswordResetConfirmView.as_view(),
        name='password_reset_confirm',
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(template_name = 'myauth/password_reset_complete.html'),
        name='password_reset_complete'),
]
