from django.http import StreamingHttpResponse, HttpResponse, HttpResponseRedirect
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
from embedding.vector.file_loader import load_pdf
from embedding.polly.audio import generate_audio
from embedding.openai.features import get_embedding_prompt, feature_training, feature_action, feature_question, feature_glm, feature_quiz, feature_translate, feature_grammar, feature_summary, feature_image, feature_chat, feature_chat_llama
from embedding.models import TherapyProfile, TokenConsumption, PromptModel, EmbeddingModel, OcrRecord, QuizRecord, UserProfile, Dialogue
from django.shortcuts import render
from django.db import transaction
from embedding.utils import load_random_string, get_basic_data, parse_diff
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


def image_async(request):
    description = request.POST.get('original_text', '')
    style = request.POST.get('style', '')
    count = request.POST.get('count', '3')
    count = int(count)
    if style != '':
        description += '. In ' + style + ' style.'
    openai_response = feature_image(description, count)
    record_consumption(
        request, sc.MODEL_TYPES_IMAGE, openai_response)
    return HttpResponse(json.dumps({'urls': openai_response['data']}))


def image(request):
    ret = get_basic_data(request)
    ret['form'] = ImageForm()
    return render(request, 'embedding/image.html', ret)