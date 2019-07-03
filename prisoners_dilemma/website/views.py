from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .forms import PlayerCreationForm

# Create your views here.
class HomeView(generic.TemplateView):
    template_name = 'website/home.html'

class SignUpView(generic.edit.CreateView):
    template_name = 'website/signup.html'
    form_class = PlayerCreationForm
    
    # You will get migrate errors if you use 'reverse' instead of 'reverse_lazy'
    # in your views
    success_url = reverse_lazy('login')
    
class AccountView(generic.DetailView):
    def random(self):
        return

class LeaderboardView(generic.ListView):
    def random(self):
        return