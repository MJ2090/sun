from django.urls import path

from . import views

urlpatterns = [
    # ex: /embedding/
    path('', views.index, name='index'),
    path('answer/', views.answer, name='answer'),
]