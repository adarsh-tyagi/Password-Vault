from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import NewUserForm, PasswordForm
from .models import PasswordModel
from django.utils import timezone
from datetime import datetime

def encryption(s, key):
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890@#$*&";
    shiftedAlpha = alpha[key:]+alpha[0:key]
    print(shiftedAlpha)
    newS = ''
    for i in s:
        if i.upper() in alpha:
            idx = alpha.index(i.upper())
            if i.isupper():
                newS += shiftedAlpha[idx]
            else:
                newS += shiftedAlpha[idx].lower()
        else:
            newS += i

    print(newS)
    return newS

def decryption(s):
    tempS = encryption(s, 36);
    print(tempS)
    return tempS

# Create your views here.
def home(request):
    return render(request,template_name='main/home.html', context={"msg": "hello"})

def register_view(request):
    if request.method == 'GET':
        return render(request,'main/register.html', {"form": NewUserForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], request.POST['email'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('main:home')
            except IntegrityError:
                return render(request, 'main/register.html', {'form': NewUserForm(), 'error': 'Username/email already registered.'})
        else:
            return render(request, 'main/register.html', {'form': NewUserForm(), 'error': 'Both passwords did not matched.'})

def login_view(request):
    if request.method == 'GET':
        return render(request, 'main/login.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'main/login.html', {'form': AuthenticationForm(), 'error': 'Username and password did not matched.'})
        else:
            login(request, user)
            return redirect('main:home')

@login_required
def logout_view(request):
    logout(request)
    return redirect('main:home')

@login_required
def passwords_view(request):
    password_list = PasswordModel.objects.filter(user=request.user)
    for p in password_list:
        p.password_value = decryption(p.password_value)
    count = len(password_list)
    return render(request, 'main/password.html', {'password_list': password_list, "count": count})

@login_required
def create_password(request):
    if request.method == 'GET':
        return render(request, 'main/create_password.html', {'form': PasswordForm()})
    else:
        try:
            form = PasswordForm(request.POST)
            new_pass = form.save(commit=False)
            new_pass.password_value = encryption(new_pass.password_value, 5)
            new_pass.user = request.user
            new_pass.save()
            return redirect("main:passwords")
        except Exception as e:
            return render(request, 'main/create_password.html', {'form': PasswordForm()})

@login_required
def delete_password(request, passwords_pk):
    password = get_object_or_404(PasswordModel, pk=passwords_pk, user=request.user)
    password.delete()
    return redirect("main:passwords")

@login_required
def profile_view(request):
    password_list = PasswordModel.objects.filter(user=request.user)
    count = len(password_list)
    return render(request, 'main/profile.html', {"user": request.user, 'password_list': password_list, "count": count})
