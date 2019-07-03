from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import PlayerCreationForm, PlayerChangeForm
from .models import PlayerUser

# Register your models here.
class PlayerAdmin(UserAdmin):
    add_form = PlayerCreationForm
    form = PlayerChangeForm
    model = PlayerUser
    
    list_display = ['username', 'email', 'cooperative_score']
    search_fields = ['username']
    
admin.site.register(PlayerUser, PlayerAdmin)