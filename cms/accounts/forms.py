from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import SignupCustomer


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Type a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )


class SignupCustomerForm(forms.ModelForm):
    class Meta:
        model = SignupCustomer
        fields = ('approved',)