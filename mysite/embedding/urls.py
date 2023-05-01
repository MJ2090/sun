from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    # ex: /summary/
    path('', views.home, name='index'),
    path('summary/', views.summary, name='summary'),
    path('grammar/', views.grammar, name='grammar'),
    path('translation/', views.translation, name='translation'),
    path('embedding_question/', views.embedding_question,
         name='embedding_question'),
    path('embedding_question_async/', views.embedding_question_async,
         name='embedding_question_async'),
    path('embedding_training/', views.embedding_training,
         name='embedding_training'),
    path('embedding_training_async/', views.embedding_training_async,
         name='embedding_training_async'),
    path('answer/', views.answer, name='answer'),
    path('about/', views.about, name='about'),
    path('settings/', views.settings, name='settings'),
    path('payments/', views.payments, name='payments'),
    path('contact/', views.contact, name='contact'),
    path('chat/', views.chat, name='chat'),
    path('chat2/', views.chat, name='chat2'),
    path('lab/', views.lab, name='lab'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    path('sendchat/', views.sendchat, name='sendchat'),
    path('chat_therapy/', views.chat_therapy, name='chat_therapy'),
    path('pricing/', views.pricing, name='pricing'),
    path('sendchat_home/', views.sendchat_home, name='sendchat_home'),
    path('image/', views.image, name='image'),
    path('collection/', views.collection, name='collection'),
    path('super/', views.add_prompt_model, name='add_prompt_model'),
    path('grammar_async/', views.grammar_async, name='grammar_async'),
    path('summary_async/', views.summary_async, name='summary_async'),
    path('translation_async/', views.translation_async, name='translation_async'),
    path('image_async/', views.image_async, name='image_async'),
]

urlpatterns += staticfiles_urlpatterns()