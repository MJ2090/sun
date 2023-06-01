from django.http import StreamingHttpResponse, HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.utils.translation import activate
from embedding.forms.embedding import TrainingForm, QuestionForm
from embedding.forms.translation import TranslationForm
from embedding.forms.grammar import GrammarForm
from embedding.forms.prompt_model import PromptModelForm
from embedding.forms.summary import SummaryForm
from embedding.forms.demo import DemoForm
from embedding.forms.quiz import QuizForm
from embedding.forms.image import ImageForm
from embedding.forms.chat import ChatForm
from embedding.forms.contact import ContactForm
from embedding.forms.signup import SignupForm
from embedding.forms.signin import SigninForm
from embedding.forms.home_chat import HomeChatForm
from embedding.vector.file_loader import load_pdf
from embedding.polly.audio import generate_audio
from embedding.openai.features import get_embedding_prompt, feature_training, feature_action, feature_question, feature_glm, feature_quiz, feature_translate, feature_grammar, feature_summary, feature_image, feature_chat, feature_chat_llama
from embedding.models import TherapyProfile, TokenConsumption, PromptModel, EmbeddingModel, OcrRecord, QuizRecord, UserProfile, Contact, Dialogue
from django.shortcuts import render
from django.db import transaction
from .utils import load_random_string, get_basic_data, enable_new_home, parse_diff
from embedding.ocr import recognize_image
import embedding.static_values as sc
import os
import json
import random
import time
from datetime import datetime
from django.conf import settings as conf_settings
from django.core.files.storage import default_storage
from PIL import Image

random.seed(datetime.now().timestamp())


def home(request):
    ret = get_basic_data(request)
    ret['home_chat_form'] = HomeChatForm()
    ret['enable_home_chat'] = True
    return render(request, 'embedding/home.html', ret)


def answer(request):
    ret = get_basic_data(request)
    return render(request, 'embedding/answer.html', ret)


def about(request):
    ret = get_basic_data(request)
    ret['current_page'] = 'about'
    return render(request, 'embedding/about.html', ret)


def payments(request):
    ret = get_basic_data(request)
    return render(request, 'embedding/payments.html', ret)


def settings(request):
    ret = get_basic_data(request)
    return render(request, 'embedding/settings.html', ret)


def contact(request):
    ret = get_basic_data(request)
    ret['current_page'] = 'contact'
    # if this is a POST request we need to process the form data

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ContactForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # name = form.cleaned_data["username"]
            data = Contact(
                username=form.cleaned_data["username"], email=form.cleaned_data["email"], message=form.cleaned_data["message"])
            data.save()
            # ...
            # redirect to a new URL:
            return render(request, 'embedding/thanks.html', {})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ContactForm()
    ret['form'] = form
    return render(request, 'embedding/contact.html', ret)