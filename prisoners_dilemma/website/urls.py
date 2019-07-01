# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 14:17:57 2019

@author: Sarah
"""

from django.urls import path

from . import views

urlpatterns = [
            path('', views.HomeView.as_view(), name='home'),
        ]