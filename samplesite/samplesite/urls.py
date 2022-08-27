"""samplesite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from bboard.views import home
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home),

    path('accounts/login/', auth_views.LoginView.as_view(next_page='bboard:inde'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='bboard:inde'), name='logout'),

    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(
        template_name='registration/change_password.html'
    ), name='password_change'),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='registration/password_changed.html'
    ), name='password_change_done'),

    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/reset_password.html',
        subject_template_name='registration/reset_subject.txt',
        email_template_name='registration/reset_email.txt'
    ), name='password_reset'),
    path('accounts/password_reset/done', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/email_sent.html',
    ), name='password_reset_done'),
    path('accounts/password_reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/confirm_password.html',
    ), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_confirmed.html',
    ), name='password_reset_complete'),

    path('bboard/', include('bboard.urls')),
    path('ticket/', include('ticket.urls')),
]
