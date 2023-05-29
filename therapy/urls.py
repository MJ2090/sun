from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('therapy/', views.therapy, name='therapy'),
]

urlpatterns += staticfiles_urlpatterns()