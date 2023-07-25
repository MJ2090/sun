from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from .views import views_gaga, views_yangmei, views_tele, views_pay, views_olivia, views_admin, views_chat, views_embedding, views_demo, views_quiz, views_summary, views_tab, views_sign, views_image, views_translation, views_grammar


urlpatterns = [
    path('', views_tab.home, name='index'),
    path('answer/', views_tab.answer, name='answer'),
    path('about/', views_tab.about, name='about'),
    path('settings/', views_tab.settings, name='settings'),
    path('payments/', views_tab.payments, name='payments'),
    path('contact/', views_tab.contact, name='contact'),
    path('pricing/', views_tab.pricing, name='pricing'),
    path('collection/', views_tab.collection, name='collection'),

    path('summary/', views_summary.summary, name='summary'),
    path('summary_async/', views_summary.summary_async, name='summary_async'),

    path('grammar/', views_grammar.grammar, name='grammar'),
    path('grammar_async/', views_grammar.grammar_async, name='grammar_async'),

    path('translation/', views_translation.translation, name='translation'),
    path('translation_async/', views_translation.translation_async,
         name='translation_async'),
    path('stream/', views_translation.stream, name='stream'),
    path('stream_async/', views_translation.stream_async, name='stream_async'),

    path('image/', views_image.image, name='image'),
    path('image_async/', views_image.image_async, name='image_async'),

    path('wuxi/', views_embedding.embedding_wuxi, name='embedding_wuxi'),
    path('embedding_question/', views_embedding.embedding_question,
         name='embedding_question'),
    path('embedding_question_async/', views_embedding.embedding_question_async,
         name='embedding_question_async'),
    path('embedding_training/', views_embedding.embedding_training,
         name='embedding_training'),
    path('embedding_training_async/', views_embedding.embedding_training_async,
         name='embedding_training_async'),
    path('embedding_fetch_model_async/', views_embedding.embedding_fetch_model_async,
         name='embedding_fetch_model_async'),
    path('embedding_add_doc_async/', views_embedding.embedding_add_doc_async,
         name='embedding_add_doc_async'),

    path('signin/', views_sign.signin, name='signin'),
    path('signup/', views_sign.signup, name='signup'),
    path('signout/', views_sign.signout, name='signout'),

    path('demo_pdf/', views_demo.demo_pdf, name='demo_pdf'),
    path('demo_summary/', views_demo.demo_summary, name='demo_summary'),
    path('demo_pdf_async/', views_demo.demo_pdf_async, name='demo_pdf_async'),
    path('demo_summary_async/', views_demo.demo_summary_async,
         name='demo_summary_async'),

    path('quiz/', views_quiz.quiz, name='quiz'),
    path('q/', views_quiz.q, name='q'),
    path('quiz_async/', views_quiz.quiz_async, name='quiz_async'),
    path('quiz_question_async/', views_quiz.quiz_question_async,
         name='quiz_question_async'),
    path('quiz_image_async/', views_quiz.quiz_image_async, name='quiz_image_async'),

    path('chat/', views_chat.chat, name='chat'),
    path('chat_therapy_gpt/', views_chat.chat_therapy_gpt, name='chat_therapy_gpt'),
    path('chat_therapy_llama/', views_chat.chat_therapy_llama,
         name='chat_therapy_llama'),

    path('chat_async/', views_chat.chat_async, name='chat_async'),
    path('chat_async_customer_service/', views_chat.chat_async_customer_service,
         name='chat_async_customer_service'),
    path('chat_async_therapy/', views_chat.chat_async_therapy,
         name='chat_async_therapy'),

    path('chat_olivia/', views_chat.chat_olivia, name='chat_olivia'),

    path('olivia/', views_olivia.olivia_entrance, name='olivia_entrance'),
    path('olivia_async_init/', views_olivia.olivia_async_init,
         name='olivia_async_init'),
    path('olivia_async_chat/', views_olivia.olivia_async_chat,
         name='olivia_async_chat'),
    path('olivia_async_ack/', views_olivia.olivia_async_ack,
         name='olivia_async_ack'),

    path('super/', views_admin.add_prompt_model, name='add_prompt_model'),
    path('pay/', views_pay.pay, name='pay'),
    path('pay_success/', views_pay.pay_success, name='pay_success'),
    path('pay_session/', views_pay.pay_session, name='pay_session'),
#     path('stripe_call/', views_pay.stripe_call, name='stripe_call'),

    path('tele/', views_tele.tele, name='tele'),

    path('yangmei/', views_yangmei.yangmei, name='yangmei'),
    path('yangmei_intent/', views_yangmei.yangmei_intent, name='yangmei_intent'),
    path('stripe_call/', views_yangmei.yangmei_stripe_call, name='yangmei_stripe_call'),

    path('gaga/', views_gaga.chat_gaga, name='chat_gaga'),
    path('chat_async_gaga/', views_gaga.chat_async_gaga, name='chat_async_gaga'),
    path('gagapay/', views_gaga.gagapay, name='gagapay'),
    path('gaga_pay_session/', views_gaga.gaga_pay_session, name='gaga_pay_session'),
    path('gaga_intent/', views_gaga.gaga_intent, name='gaga_intent'),
]

urlpatterns += staticfiles_urlpatterns()
