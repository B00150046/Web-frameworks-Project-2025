from django.contrib import admin
from django.urls import include, path
from debug_toolbar.toolbar import debug_toolbar_urls
from . import views

app_name = 'orchidea'
urlpatterns = [
    #Basic views
    path("", views.HomeView.as_view(), name='home'),
    
    path("register/", views.RegisterView.as_view(), name='register'), #For employees only
    path("register/customer/", views.CustRegisterView.as_view(), name='registerCustomer'), #For customers only
   # path("about/", views.AboutView.as_view(), name='about'),
   # path("contact/", views.ContactView.as_view(), name='contact'),
    
    path("login/", views.LoginView.as_view(), name='login'), # Same thing but applies for all User classes, Recuritees, Employees, Recruiters and Boss
    path("login/customer/", views.LoginCustomerView.as_view(), name='loginCustomer'), #For Customers only
    path("logout/", views.LogoutView.as_view(), name='logout'), # Same thing but applies for all User classes, Recuritees, Employees, Recruiters and Boss
    # path("login/employee/", views.LoginEmployeeView.as_view(), name='loginEmployee'), #For employees only
    
    # bpath("logout/", views.LogoutView.as_view(), name='logout'), # Same thing but applies for all User classes, Recuritees, Employees, Recruiters and Boss
    
    #Protected views - Employees
    # path("employee/<int:User_Id>/", views.HomeEmployeeView.as_view(), name='homeEmployee'), #For employees only
    path("customer/<int:User_Id>/", views.CustomerHomeView.as_view(), name='homeCustomer'), #For customers only
    # path("employee/<int:User_Id>/manageEmployees/", views.ManageEmployeesView.as_view(), name='manageEmployees'), #For Boss only
    # path("") path for recruitment
    # path("employee/<int:User_Id>/recruit/", views.ManageRecruiteesView.as_view(), name='recruit'),
    # path("customer/<int:User_Id>/appointments", views.AppointmentView.as_view(), name='appointments'), #All appointments view
    # path("customer/<int:User_Id>/appointments/<int:pk>/", views.SingleAppointmentView.as_view(), name='single-appointment'), #single appointment view
    # path ("customer/<int:User_Id>/makeRecruitment/<int:pk>/", views.RecruitmentView.as_view(), name='makeRecruitment'),
]