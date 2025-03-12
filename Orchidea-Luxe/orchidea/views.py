from django.http import HttpResponse
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone


class HomeView(generic.View):
    def get(self, request):
        return render(request, 'orchidea/Components.html')
    
class RegisterView(generic.View):
    def get(self, request):
        return HttpResponse("Hello, world. You're at the orchidea register page.")
    
class LoginView(generic.View):
    def get(self, request):
        return HttpResponse("Hello, world. You're at the orchidea login page.")