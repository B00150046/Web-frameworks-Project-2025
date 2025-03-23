from django.contrib import admin
from django.urls import include, path
from debug_toolbar.toolbar import debug_toolbar_urls
from . import views

app_name = 'orchidea'
urlpatterns = [
    #Basic views
    path("", views.HomeView.as_view(), name='home'),
    
    path("register/", views.RegisterView.as_view(), name='register'), #For employees only
    path("register/Customer", views.RegisterCustomerView.as_view(), name='registerCustomer'), #For recruiters only
    path("about/", views.AboutView.as_view(), name='about'),
    path("contact/", views.ContactView.as_view(), name='contact'),
    
    path("login/", views.LoginView.as_view(), name='login'), # Same thing but applies for all User classes, Recuritees, Employees, Recruiters and Boss
    path("loginCustomer/", views.LoginCustomerView.as_view(), name='loginCustomer'), #For Customers only
    path("loginEmployee/", views.LoginEmployeeView.as_view(), name='loginEmployee'), #For employees only
    
    path("logout/", views.LogoutView.as_view(), name='logout'), # Same thing but applies for all User classes, Recuritees, Employees, Recruiters and Boss
    
    #Protected views - Employees
    path("employee/<int:pk>/", views.HomeEmployeeView.as_view(), name='homeEmployee'), #For employees only
    path("customer/<int:pk>/", views.CustomerHomeView.as_view(), name='customerHome'), #For customers only
    path("manageEmployees/", views.ManageEmployeesView.as_view(), name='manageEmployees'), #For Boss only
    # path("") path for recruitment
    path("recruit/", views.ManageRecruiteesView.as_view(), name='recruit'),
     path("appointments", views.AppointmentView.as_view(), name='appointments'), #All appointments view
    path("appointments/<int:pk>/", views.SingleAppointmentView.as_view(), name='single-appointment'), #single appointment view
    path ("makeRecruitment/<int:pk>/", views.RecruitmentView.as_view(), name='makeRecruitment'),
]