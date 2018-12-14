from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('success/', views.success),
    path('login', views.login),
    path('logout/', views.logout),
    path('new/', views.new),
    path('add', views.add),
    path('show/<id>', views.show),
    path('join/<id>', views.join)
]