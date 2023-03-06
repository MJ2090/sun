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
    path('settings/', views.settings, name='settings'),
    path('payments/', views.payments, name='payments'),
    path('contact/', views.contact, name='contact'),
    path('chat/', views.chat, name='chat'),
    path('chat2/', views.chat, name='chat2'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    path('sendchat/', views.sendchat, name='sendchat'),
    path('image/', views.image, name='image'),
    path('collection/', views.collection, name='collection'),
    path('super/', views.add_prompt_model, name='add_prompt_model'),
    path('send_grammar/', views.grammar_async, name='grammar_async'),
    path('send_summary/', views.send_summary, name='send_summary'),
]