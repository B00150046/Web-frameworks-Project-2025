from django.contrib import admin
from django.urls import include, path
from debug_toolbar.toolbar import debug_toolbar_urls
from . import views

app_name = 'orchidea'
urlpatterns = [
    path("", views.HomeView.as_view(), name='home'),
    path("register/", views.RegisterView.as_view(), name='register'),
    path("login/", views.LoginView.as_view(), name='login'),
    # path("")
]