# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 13:40:51 2019

@author: Sarah
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import PlayerUser

class PlayerCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = PlayerUser
        fields = ('username', 'email')
        
class PlayerChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = PlayerUser
        fields = ('username', 'email')