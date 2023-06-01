from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.translation import activate
from embedding.forms.embedding import TrainingForm, QuestionForm
from embedding.forms.prompt_model import PromptModelForm
from embedding.forms.chat import ChatForm
from embedding.vector.file_loader import load_pdf
from embedding.polly.audio import generate_audio
from embedding.openai.features import get_embedding_prompt, feature_training, feature_action, feature_question, feature_chat, feature_chat_llama
from embedding.models import TherapyProfile, PromptModel, EmbeddingModel, Dialogue
from django.shortcuts import render
from embedding.utils import load_embedding_models, save_to_local, load_random_string, get_basic_data, get_user, record_consumption
import embedding.static_values as sc
import json
import random
import time
from datetime import datetime


@login_required
def embedding_training(request):
    ret = get_basic_data(request)
    ret['form'] = TrainingForm()
    return render(request, 'embedding/embedding_training.html', ret)


@login_required
def embedding_training_async(request):
    text = request.POST.get('text', '') + '\n\n'
    name = request.POST.get('name', '')
    reject_message = request.POST.get('reject_message', '')
    print("original_pdf ", request.FILES, type(request.FILES))
    for _, original_pdf in request.FILES.items():
        pdf_file_name = save_to_local(original_pdf, 'pdf')
        pdf_pages = load_pdf(pdf_file_name)
        text += '\n\n'.join([page.page_content for page in pdf_pages])
        print('current text length: ', len(text), text, f'current file name: {pdf_file_name}, pages: {len(pdf_pages)}')
    print(f'embedding_training_async started, embedding name {name}')
    openai_response = feature_training(text)
    new_model = EmbeddingModel.objects.get_or_create(
        name=name, owner=request.user, uuid=openai_response, reject_message=reject_message)
    print(openai_response)
    return HttpResponse(json.dumps({'result': f'new model {name} has finished training.'}))


def embedding_wuxi(request):
    user_language = "zh_hans"
    activate(user_language)
    ret = get_basic_data(request, {'hide_nav': True})
    ret['form'] = QuestionForm()

    load_embedding_models(request, ret)
    return render(request, 'embedding/wuxi.html', ret)


def embedding_question(request):
    ret = get_basic_data(request)
    ret['form'] = QuestionForm()

    load_embedding_models(request, ret)
    if len(ret['form'].fields['character'].choices) == 0:
        ret['error_msg'] = 'No Q&A bot found, please create new models.'
        return render(request, 'embedding/embedding_question.html', ret)

    return render(request, 'embedding/embedding_question.html', ret)


def embedding_question_async(request):
    question = request.POST.get('question', '')
    character = request.POST.get('character', '')
    enable_speech = request.POST.get('enable_speech', '')
    embedding_model = EmbeddingModel.objects.get(uuid=character)
    answer = feature_question(question, embedding_model)
    print(answer)

    if enable_speech == 'true':
        audio_address = generate_audio(answer, 'Stephen')
    else:
        audio_address = ''
    return HttpResponse(json.dumps({'answer': answer.strip(), 'audio_address': audio_address}))
