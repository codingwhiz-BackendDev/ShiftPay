from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('shift/log/', views.log_shift, name='log_shift'),
    path('advance/request/', views.advance_request, name='advance_request'),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("reset-password/<uidb64>/<token>/", views.reset_password, name="reset_password"),
]
