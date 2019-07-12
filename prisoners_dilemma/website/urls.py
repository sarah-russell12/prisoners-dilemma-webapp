# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 14:17:57 2019

@author: Sarah
"""

from django.urls import path
from django.contrib.auth import views as auth_views

from .views import HomeView, SignUpView, ProfileView


urlpatterns = [
            path('home/', HomeView.as_view(), name='home'),
            path('signup/', SignUpView.as_view(), name='signup'),
            path('login/', auth_views.LoginView.as_view(template_name='website/auth/login.html'), name='login'),
            path('profile/', ProfileView.as_view(), name='profile'),
            path('profile/change-password/', auth_views.PasswordChangeView.as_view(template_name='website/auth/change-password.html'), name='change-password'),
            path('profile/change-password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='website/auth/change-password-done.html'), name='change-password-done'),
            path('reset-password/', auth_views.PasswordResetView.as_view(template_name='website/auth/reset-password.html'), name='reset-password'),
            path('reset-password/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='website/auth/reset-password-confirm.html')),
            path('reset-password/done/', auth_views.PasswordResetDoneView.as_view(template_name='website/auth/reset-password-done.html'), name='password-reset-done'),
            path('logout/', auth_views.LogoutView.as_view(), name='logout')
        ]