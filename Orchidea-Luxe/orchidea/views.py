from django.http import HttpResponse
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import User


class HomeView(generic.View):
    def get(self, request):
        return render(request, 'orchidea/Components-Base.html')
    
class AboutView(generic.View):
    def get(self, request):
        return render(request, 'orchidea/Components-About.html')
    
class ContactView(generic.View):
    def get(self, request):
        return render(request, 'orchidea/Components-Contact.html')
    
class RegisterView(generic.FormView):
    model = User
    template_name = 'orchidea/register.html'
    def get(self, request):
        return HttpResponse("Hello, world. You're at the orchidea register page.")
    
class RegisterCustomerView(generic.FormView):
    model = User
    template_name = 'orchidea/Register/registerCustomer.html'
    def get(self, request):
        return HttpResponse("Hello, world. You're at the orchidea register customer page.")

class LogoutView(generic.View):
    template_name = 'orchiea/Login/logout.html'
    def get(self, request):
        return HttpResponse("Hello, world. You're at the orchidea logout page.")
    
class LoginView(generic.View):
    template_name = 'orchidea/Login/Login.html'
    def get(self, request):
        return render(request, 'orchidea/Login/Login.html')
    
class LoginCustomerView(generic.View):
    model = User
    template_name = 'orchidea/loginCustomer.html'
    def get(self, request):
        return HttpResponse("Hello, world. You're at the orchidea login customer page.")
    
class LoginEmployeeView(generic.View):
    model = User
    template_name = 'orchidea/loginEmployee.html'
    def get(self, request):
        return HttpResponse("Hello, world. You're at the orchidea login employee page.")
    
class HomeEmployeeView(generic.View):
    model = User
    template_name = 'orchidea/homeEmployee.html'
    def get(self, request):
        return HttpResponse("Hello, world. You're at the orchidea home employee page.")

class CustomerHomeView(generic.View):
    model = User
    template_name = 'orchidea/customerHome.html'
    def get(self, request):
        return HttpResponse("Hello, world. You're at the orchidea customer home page.")
    
class ManageEmployeesView(generic.View):
    model = User
    template_name = 'orchidea/manageEmployees.html'
    def get(self, request):
        return HttpResponse("Hello, world. You're at the orchidea manage employees page.")
    
class ManageRecruiteesView(generic.View):
    model = User
    template_name = 'orchidea/manageRecruiters.html'
    def get(self, request):
        return HttpResponse("Hello, world. You're at the orchidea manage recruiters page.")

class RecruitmentView(generic.View):
    model = User
    template_name = 'orchidea/recruit.html'
    def get(self, request):
        return HttpResponse("Hello, world. You're at the orchidea recruit page.")
    
class SingleAppointmentView(generic.View):
    model = User
    template_name = 'orchidea/appointments.html'
    def get(self, request):
        return HttpResponse("Hello, world. You're at the orchidea single appointment page.")
    
class AppointmentView(generic.View):
    model = User
    template_name = 'orchidea/appointments.html'
    def get(self, request):
        return HttpResponse("Hello, world. You're at the orchidea appointments page.")