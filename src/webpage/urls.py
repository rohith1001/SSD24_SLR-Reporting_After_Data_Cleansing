from django.urls import path

from . import views

urlpatterns = [
    path('', views.homeView, name='home'),
    path('upload', views.upload, name='upload'),
]
