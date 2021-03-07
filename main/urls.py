"""passwordVault URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

app_name="main"
urlpatterns = [
    path('', views.home, name="home"),
    path('login/',views.login_view, name="login"),
    path('register/', views.register_view, name="register"),
    path('profile/', views.profile_view, name="profile"),
    path('logout/', views.logout_view, name="logout"),
    path('passwords/', views.passwords_view, name="passwords"),
    path('createpassword/', views.create_password, name="create_password"),
    path('<int:passwords_pk>/delete', views.delete_password, name="delete_password")
]
