from django.shortcuts import render, redirect
from .forms import SignUpForm, SignupCustomerForm
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


# Create your views here.

def signup(request):
    if request.method=='POST':
        a_form = SignupCustomerForm(request.POST)
        b_form = SignUpForm(request.POST)
        if a_form.is_valid() and b_form.is_valid():
            user = b_form.save()
            a_form = a_form.save(commit=False)
            a_form.user = user
            a_form.save()
            return redirect(reverse('login'))
    else:
        a_form = SignupCustomerForm()
        b_form = SignUpForm()
    return render(request, 'accounts/signup.html', {'a_form': a_form, 'b_form': b_form})

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/password_change.html', {'form': form})


def pending_approval(request):
    return render(request, 'accounts/pending_approval.html')