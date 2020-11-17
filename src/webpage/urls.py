from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path('', views.homeView, name='home'),
    path('ieee', views.homeIeee, name='home_ieee'),
    path('acm', views.homeAcm, name='home_acm'),
    path('upload', views.upload, name='upload'),
]

urlpatterns += staticfiles_urlpatterns()
