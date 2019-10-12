from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .forms import PlayerCreationForm
from .models import PlayerUser
from .sio import SERVER, server_update_thread

THREAD = None

# Create your views here.
class HomeView(generic.TemplateView):
    template_name = 'website/home.html'

class SignUpView(generic.edit.CreateView):
    template_name = 'website/auth/signup.html'
    form_class = PlayerCreationForm
    
    # You will get migrate errors if you use 'reverse' instead of 'reverse_lazy'
    # in your views
    success_url = reverse_lazy('login')
    
class ProfileView(generic.TemplateView):
    template_name = 'website/profile.html'

class LeaderboardView(generic.ListView):
    template_name = 'website/leaderboard.html'
    queryset = PlayerUser.objects.order_by('-points').filter(points__gt=0)[:100]
    
    context_object_name = 'leaderboard'
    list_display = ['username', 'points', 'cooperative_score']
    
    def random(self):
        return

def play(request):
    global THREAD
    if THREAD is None:
        THREAD = SERVER.start_background_task(server_update_thread)
    return render(request, 'website/play.html')