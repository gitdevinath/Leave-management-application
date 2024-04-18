from django import forms
from .models import addLeave
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='username', max_length=150)
    email = forms.EmailField(label='email')
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='password2', widget=forms.PasswordInput)


class employeeLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class AddLeaveForm(forms.ModelForm):
    class Meta:
        model = addLeave
        fields = ['fromDate', 'toDate', 'reason', 'comment']

class CustomUserCreationForm(UserCreationForm):
    model = User
    fields = ['username', 'email', 'password1', 'password2']