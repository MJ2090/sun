from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path('therapy/', views.therapy, name='therapy'),
]

urlpatterns += staticfiles_urlpatterns()