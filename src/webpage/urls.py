from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path('', views.homeView, name='home'),
    path('upload', views.upload, name='upload'),
]

urlpatterns += staticfiles_urlpatterns()
