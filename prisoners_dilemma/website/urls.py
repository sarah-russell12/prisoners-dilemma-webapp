# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 14:17:57 2019

@author: Sarah
"""

from django.urls import path

from .views import HomeView, SignUpView

urlpatterns = [
            path('home/', HomeView.as_view(), name='home'),
            path('signup/', SignUpView.as_view(), name='signup')
        ]