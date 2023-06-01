from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from .views import views_tab

from . import views

urlpatterns = [
    # ex: /summary/
    path('', views_tab.home, name='index'),
    path('answer/', views_tab.answer, name='answer'),
    path('about/', views_tab.about, name='about'),
    path('settings/', views_tab.settings, name='settings'),
    path('payments/', views_tab.payments, name='payments'),
    path('contact/', views_tab.contact, name='contact'),
    path('summary/', views.summary, name='summary'),
    path('grammar/', views.grammar, name='grammar'),
    path('translation/', views.translation, name='translation'),
    path('wuxi/', views.embedding_wuxi, name='embedding_wuxi'),
    path('embedding_question/', views.embedding_question,
         name='embedding_question'),
    path('embedding_question_async/', views.embedding_question_async,
         name='embedding_question_async'),
    path('embedding_training/', views.embedding_training,
         name='embedding_training'),
    path('embedding_training_async/', views.embedding_training_async,
         name='embedding_training_async'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    path('chat/', views.chat, name='chat'),
    path('chat2/', views.chat, name='chat2'),
    path('sendchat_async/', views.sendchat_async, name='sendchat_async'),
    path('sendchat_therapy_async/', views.sendchat_therapy_async,
         name='sendchat_therapy_async'),
    path('chat_therapy/', views.chat_therapy, name='chat_therapy'),
    path('chat_therapy_llama/', views.chat_therapy_llama,
         name='chat_therapy_llama'),
    path('chat_olivia/', views.chat_olivia, name='chat_olivia'),
    path('sendchat_home/', views.sendchat_home, name='sendchat_home'),
    path('image/', views.image, name='image'),
    path('collection/', views.collection, name='collection'),
    path('super/', views.add_prompt_model, name='add_prompt_model'),
    path('pricing/', views.pricing, name='pricing'),
    path('grammar_async/', views.grammar_async, name='grammar_async'),
    path('summary_async/', views.summary_async, name='summary_async'),
    path('demo_pdf/', views.demo_pdf, name='demo_pdf'),
    path('demo_summary/', views.demo_summary, name='demo_summary'),
    path('demo_pdf_async/', views.demo_pdf_async, name='demo_pdf_async'),
    path('demo_summary_async/', views.demo_summary_async,
         name='demo_summary_async'),
    path('translation_async/', views.translation_async, name='translation_async'),
    path('image_async/', views.image_async, name='image_async'),
    path('quiz/', views.quiz, name='quiz'),
    path('quiz_async/', views.quiz_async, name='quiz_async'),
    path('quiz_question_async/', views.quiz_question_async,
         name='quiz_question_async'),
    path('quiz_image_async/', views.quiz_image_async, name='quiz_image_async'),
    path('stream/', views.stream, name='stream'),
    path('stream_async/', views.stream_async, name='stream_async'),
]

urlpatterns += staticfiles_urlpatterns()
