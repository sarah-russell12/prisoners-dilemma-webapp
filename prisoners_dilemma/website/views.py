from django.shortcuts import render
from django.views import generic

# Create your views here.
class HomeView(generic.TemplateView):
    template_name = 'website/home.html'
    def random(self):
        return
    
class AccountView(generic.DetailView):
    def random(self):
        return

class LeaderboardView(generic.ListView):
    def random(self):
        return