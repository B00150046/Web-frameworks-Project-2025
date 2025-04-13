from django.http import HttpResponse
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.shortcuts import redirect

from .models import User, Customer, Employee, Appointment, Skill, Candidate, RecruitmentForm
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from django.contrib import messages

#   ╔══════════════════════════════{  ORCHIDEA VIEWS }═══════════════════════════════╗
#       ╔═══════════════ BASIC VIEW ════════════════╗
#       ║                                           ║
#       ║   Initial views before Login / Register   ║
#       ║                                           ║
#       ╚═══════════════════════════════════════════╝
class HomeView(generic.View):
    def get(self, request):
        return render(request, 'orchidea/Components-Base.html')
    

class RegisterView(generic.View):
    template_name = 'orchidea/Register/Register.html'

    def get(self, request):
        return render(request, self.template_name)

class CustRegisterView(generic.View):
    template_name = 'orchidea/Register/Cust-Register.html'
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check if the user already exists
        if User.objects.filter(email=email).exists():
            return render(request, self.template_name, {"error": "Email already registered"})

        # Create a new user
        user = User.objects.create(username=username, email=email, password=password)

        # Create a new customer linked to the user
        customer = Customer.objects.create(user=user)

        # Store user info in session
        request.session["customer_id"] = customer.id
        request.session["user_name"] = user.username

        # Redirect to the customer home page
        return redirect("orchidea:homeCustomer", User_Id=user.id)
    


class LoginView(generic.View):
    template_name = 'orchidea/Login/Login.html'
    def get(self, request):
        return render(request, 'orchidea/Login/Login.html')
    
class LoginCustomerView(generic.View):
    template_name = 'orchidea/Login/Login-Cust.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email, password=password)
            customer = Customer.objects.get(user=user)

            # Store user info in session
            request.session["customer_id"] = customer.id
            request.session["user_name"] = user.username

            # Redirect to the customer home page
            return redirect("orchidea:homeCustomer", User_Id=user.id)
        except User.DoesNotExist:
            return render(request, self.template_name, {"error": "Invalid email or password"})
        except Customer.DoesNotExist:
            return render(request, self.template_name, {"error": "No customer account linked to this user"})  
    
class LogoutView(generic.View):
    template_name = 'orchiea/Login/logout.html'
    def get(self, request):
        return HttpResponse("Hello, world. You're at the orchidea logout page.")
    
    def post(self, request):
        # Clear the session data
        request.session.flush()
        # Redirect to the login page or any other page
        return redirect('orchidea:login')

#       ╔══════════════ CUSTOMER VIEW ══════════════╗
#       ║                                           ║
#       ║     Views when logged in as Customer      ║
#       ║                                           ║
#       ╚═══════════════════════════════════════════╝
class CustomerHomeView(generic.View):
    model = User
    template_name = 'orchidea/Customer/Customer-Home.html'
    def get(self, request, User_Id):
        user = User.objects.get(id=User_Id)
        customer = Customer.objects.get(user=user)
        return render(request, self.template_name, {'customer': customer})

#   ╚═══════════════════════════════{  ORCHIDEA VIEWS }═══════════════════════════════╝