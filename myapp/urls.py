from django.urls import path
from . import views
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns=[
    path('',views.home,name='home'),
    path('appointment/new/', views.create_appointment, name='create_appointment'),
    # path('appointments/', views.appointment_list, name='appointment_list'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('about/',views.about,name='about'),
    path('contact/', views.contact, name='contact'),
    path('blog/', views.blog, name='blog'),
    path('register/', views.register, name='register'),
    path('success/', views.appointment_success, name='appointment_success'),
    path('appointments/', views.display, name='appointment_list'),
]