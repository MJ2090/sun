from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    # ex: /summary/
    path('', views.home, name='index'),
    path('summary/', views.summary, name='summary'),
    path('demo/', views.demo, name='demo'),
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
    path('sendchat_async/', views.sendchat_async, name='sendchat_async'),
    path('sendchat_therapy_async/', views.sendchat_therapy_async, name='sendchat_therapy_async'),
    path('chat_therapy/', views.chat_therapy, name='chat_therapy'),
    path('chat_therapy_llama/', views.chat_therapy_llama, name='chat_therapy_llama'),
    path('pricing/', views.pricing, name='pricing'),
    path('sendchat_home/', views.sendchat_home, name='sendchat_home'),
    path('image/', views.image, name='image'),
    path('collection/', views.collection, name='collection'),
    path('super/', views.add_prompt_model, name='add_prompt_model'),
    path('grammar_async/', views.grammar_async, name='grammar_async'),
    path('summary_async/', views.summary_async, name='summary_async'),
    path('demo_async/', views.demo_async, name='demo_async'),
    path('translation_async/', views.translation_async, name='translation_async'),
    path('image_async/', views.image_async, name='image_async'),
    path('quiz/', views.quiz, name='quiz'),
    path('quiz_async/', views.quiz_async, name='quiz_async'),
    path('quiz_question_async/', views.quiz_question_async, name='quiz_question_async'),
    path('quiz_image_async/', views.quiz_image_async, name='quiz_image_async'),
    path('stream/', views.stream, name='stream'),
    path('stream_async/', views.stream_async, name='stream_async'),
]

urlpatterns += staticfiles_urlpatterns()