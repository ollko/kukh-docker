from django import forms

from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
)
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML
from crispy_forms.bootstrap import PrependedText
from crispy_forms.layout import Field

User = get_user_model()


class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Password confirm'), widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'is_staff', 'is_active')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

# -----------------------------------------------------------------------------
# ----Site User Forms

class UserCreationForm(UserAdminCreationForm):
    check_me_out = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-signin'
        self.helper.attrs = {'novalidate': '',}
        self.helper.layout = Layout(
            'email',
            'password1',
            'password2',
            CustomCheckbox('check_me_out'),  # <-- Here
            Submit('submit', 'Sign up')
        )


class CustomCheckbox(Field):
    template = 'custom_checkbox.html'


class UserLoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.input_type = "email"  # ugly hac

        self.helper = FormHelper()
        self.helper.form_class = 'form-signin'
        self.helper.attrs = {'novalidate': ''}
        self.helper.layout = Layout(
            Field("username", placeholder="Email"),
            Field("password", placeholder="Password"),
            # PrependedText('username', '@', placeholder="Email"),
            # PrependedText('password', '@', placeholder="Password"),
        HTML('<a href="{}">Forgot Password?</a>'.format(
            reverse("myauth:password_reset"))),
        CustomCheckbox('remember_me'),  # <-- Here
        Submit('submit', 'Sign in', css_class='btn-block')
        )

class MyPasswordResetForm(PasswordResetForm):

    def __init__(self, *args, **kwargs):
        super(MyPasswordResetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-signin'
        self.helper.attrs = {'novalidate': ''}
        self.helper.layout = Layout(
            Field("username", placeholder="Email"),
        Submit('submit', 'Send me instruction', css_class='btn-block')
        )
