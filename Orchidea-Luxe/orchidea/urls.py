from django.contrib import admin
from django.urls import include, path
from debug_toolbar.toolbar import debug_toolbar_urls
from . import views

app_name = 'orchidea'
urlpatterns = [
    # ╔══════════════════════════════════════════════════════════════════════════════╗
    # ║                                BASIC VIEWS                                   ║
    # ╚══════════════════════════════════════════════════════════════════════════════╝
    path("", views.HomeView.as_view(), name='home'),

    # ╔══════════════════════════════════════════════════════════════════════════════╗
    # ║                              REGISTER VIEWS                                  ║
    # ╚══════════════════════════════════════════════════════════════════════════════╝
    path("register/", views.RegisterView.as_view(), name='register'),
    path("register/customer/", views.CustRegisterView.as_view(), name='registerCustomer'),
    path("register/employee/", views.EmpRegisterView.as_view(), name='registerEmployee'),
    path("register/candidate/", views.CandRegisterView.as_view(), name='registerCandidate'),

    # ╔══════════════════════════════════════════════════════════════════════════════╗
    # ║                               LOGIN VIEWS                                    ║
    # ╚══════════════════════════════════════════════════════════════════════════════╝
    path("login/", views.LoginView.as_view(), name='login'),
    path("login/customer/", views.LoginCustomerView.as_view(), name='loginCustomer'),
    path("login/employee/", views.LoginEmployeeView.as_view(), name='loginEmployee'),
    path("login/candidate/", views.LoginCandidateView.as_view(), name='loginCandidate'),
    path("logout/", views.LogoutView.as_view(), name='logout'),

    # ╔══════════════════════════════════════════════════════════════════════════════╗
    # ║                        PROTECTED VIEWS - EMPLOYEES                           ║
    # ╚══════════════════════════════════════════════════════════════════════════════╝
    path("employee/<int:User_Id>/", views.HomeEmployeeView.as_view(), name='homeEmployee'),
    #View Bookings with other Customers
    path("employee/<int:User_Id>/viewBookings", views.EmployeeBookingView.as_view(), name='employee-bookings'),
    path("employee/<int:User_Id>/viewBookings/<int:pk>/", views.EmployeeBookingView.as_view(), name='employee-single-booking'),
    path("employee/<int:User_Id>/viewBookings/<int:pk>/cancel/", views.CancelEmployeeBookingView.as_view(), name='cancel-booking'),
    path("employee/<int:User_Id>/viewBookings/<int:pk>/details/", views.EmployeeBookingDetailView.as_view(), name='employee-appointment-detail'),
    #View Recruitment Forms
    path("employee/<int:User_Id>/viewRecruitmentForms/", views.RecruitmentView.as_view(), name='employee-recruitment'),
    path("employee/<int:User_Id>/viewRecruitmentForms/<int:pk>/", views.SingleRecruitmentView.as_view(), name='employee-single-recruitment'),
    path("employee/<int:User_Id>/viewRecruitmentForms/<int:pk>/accept/", views.AcceptRecruitmentView.as_view(), name='acceptRecruitment'),
    path("employee/<int:User_Id>/viewRecruitmentForms/<int:pk>/reject/", views.RejectRecruitmentView.as_view(), name='rejectRecruitment'),
    #Profile stuff
    path("employee/<int:User_Id>/profile/", views.EmployeeProfileView.as_view(), name='profile'),
    path("employee/<int:User_Id>/profile/addSkill/", views.AddEmployeeSkillView.as_view(), name='addSkill'),
    path("employee/<int:User_Id>/profile/deleteSkill/<int:pk>/", views.DeleteEmployeeSkillView.as_view(), name='deleteSkill'),

    # ╔══════════════════════════════════════════════════════════════════════════════╗
    # ║                        PROTECTED VIEWS - CUSTOMERS                           ║
    # ╚══════════════════════════════════════════════════════════════════════════════╝
    path("customer/<int:User_Id>/", views.CustomerHomeView.as_view(), name='homeCustomer'),
    path("customer/<int:User_Id>/appointments", views.AppointmentView.as_view(), name='appointments'),
    path("customer/<int:User_Id>/appointments/<int:pk>/", views.SingleAppointmentView.as_view(), name='appointment-detail'),
    path("customer/<int:User_Id>/appointments/<int:pk>/makeBooking/", views.makeBookingView.as_view(), name='makeBooking'),
    path("customer/<int:User_Id>/bookings", views.BookingView.as_view(), name='bookings'),
    path("customer/<int:User_Id>/bookings/<int:pk>/", views.SingleBookingViewDetail.as_view(), name='customer-single-booking'),
    path("customer/<int:User_Id>/bookings/<int:pk>/cancel/", views.CancelBookingView.as_view(), name='cancelBooking'),

    # ╔══════════════════════════════════════════════════════════════════════════════╗
    # ║                        PROTECTED VIEWS - CANDIDATES                          ║
    # ╚══════════════════════════════════════════════════════════════════════════════╝
    path("candidate/<int:User_Id>/", views.HomeCandidateView.as_view(), name='homeCandidate'),
    path("candidate/<int:User_Id>/apply-form/", views.ApplyFormView.as_view(), name='apply-form'),
    path("candidate/<int:User_Id>/viewRecruitmentForms", views.CandidateRecruitmentView.as_view(), name='candidate-recruitment'),
    path("candidate/<int:User_Id>/viewRecruitmentForms/<int:pk>/", views.SingleCandidateRecruitmentView.as_view(), name='candidate-single-recruitment'),
    path("candidate/<int:User_Id>/viewRecruitmentForms/<int:pk>/withdraw/", views.WithdrawRecruitmentView.as_view(), name='withdrawRecruitment'),
]