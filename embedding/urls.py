from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from .views import views_tab, views_feature, views_sign, views_image, views_translation, views_grammar


urlpatterns = [
    # ex: /summary/
    path('', views_tab.home, name='index'),
    path('answer/', views_tab.answer, name='answer'),
    path('about/', views_tab.about, name='about'),
    path('settings/', views_tab.settings, name='settings'),
    path('payments/', views_tab.payments, name='payments'),
    path('contact/', views_tab.contact, name='contact'),
    path('summary/', views_feature.summary, name='summary'),
    path('grammar/', views_grammar.grammar, name='grammar'),
    path('translation/', views_translation.translation, name='translation'),
    path('wuxi/', views_feature.embedding_wuxi, name='embedding_wuxi'),
    path('embedding_question/', views_feature.embedding_question,
         name='embedding_question'),
    path('embedding_question_async/', views_feature.embedding_question_async,
         name='embedding_question_async'),
    path('embedding_training/', views_feature.embedding_training,
         name='embedding_training'),
    path('embedding_training_async/', views_feature.embedding_training_async,
         name='embedding_training_async'),
    path('signin/', views_sign.signin, name='signin'),
    path('signup/', views_sign.signup, name='signup'),
    path('signout/', views_sign.signout, name='signout'),
    path('chat/', views_feature.chat, name='chat'),
    path('chat2/', views_feature.chat, name='chat2'),
    path('sendchat_async/', views_feature.sendchat_async, name='sendchat_async'),
    path('sendchat_therapy_async/', views_feature.sendchat_therapy_async,
         name='sendchat_therapy_async'),
    path('chat_therapy/', views_feature.chat_therapy, name='chat_therapy'),
    path('chat_therapy_llama/', views_feature.chat_therapy_llama,
         name='chat_therapy_llama'),
    path('chat_olivia/', views_feature.chat_olivia, name='chat_olivia'),
    path('sendchat_home/', views_feature.sendchat_home, name='sendchat_home'),
    path('image/', views_image.image, name='image'),
    path('collection/', views_feature.collection, name='collection'),
    path('super/', views_feature.add_prompt_model, name='add_prompt_model'),
    path('pricing/', views_feature.pricing, name='pricing'),
    path('grammar_async/', views_grammar.grammar_async, name='grammar_async'),
    path('summary_async/', views_feature.summary_async, name='summary_async'),
    path('demo_pdf/', views_feature.demo_pdf, name='demo_pdf'),
    path('demo_summary/', views_feature.demo_summary, name='demo_summary'),
    path('demo_pdf_async/', views_feature.demo_pdf_async, name='demo_pdf_async'),
    path('demo_summary_async/', views_feature.demo_summary_async,
         name='demo_summary_async'),
    path('translation_async/', views_translation.translation_async, name='translation_async'),
    path('image_async/', views_image.image_async, name='image_async'),
    path('quiz/', views_feature.quiz, name='quiz'),
    path('quiz_async/', views_feature.quiz_async, name='quiz_async'),
    path('quiz_question_async/', views_feature.quiz_question_async,
         name='quiz_question_async'),
    path('quiz_image_async/', views_feature.quiz_image_async, name='quiz_image_async'),
    path('stream/', views_translation.stream, name='stream'),
    path('stream_async/', views_translation.stream_async, name='stream_async'),
]

urlpatterns += staticfiles_urlpatterns()
