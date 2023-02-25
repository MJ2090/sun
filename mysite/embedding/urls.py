from django.urls import path

from . import views

urlpatterns = [
    # ex: /embedding/
    path('', views.home, name='index'),
    path('summary/', views.summary, name='summary'),
    path('grammar/', views.grammar, name='grammar'),
    path('translation/', views.translation, name='translation'),
    path('embedding/', views.embedding, name='embedding'),
    path('answer/', views.answer, name='answer'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]