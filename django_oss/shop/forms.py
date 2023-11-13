from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

## SOURCE: https://medium.com/@devsumitg/django-auth-user-signup-and-login-7b424dae7fab ##
class SignupForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['username', 'password1', 'password2']

## SOURCE: https://medium.com/@devsumitg/django-auth-user-signup-and-login-7b424dae7fab ##
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)