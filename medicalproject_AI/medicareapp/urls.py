from django.urls import path
from medicareapp import views

urlpatterns = [
    path('', views.index, name='login'),          # This is your home/login page
    path('register/', views.register, name='signup'), # Fixes the signup error
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'), # Essential for logout button
    path('forgot-password/', views.password_reset_request, name='password_reset_request'),
]   