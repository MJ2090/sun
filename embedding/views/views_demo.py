from django.http import HttpResponse
from embedding.forms.demo import DemoForm
from embedding.openai.features import get_embedding_prompt, feature_glm
from django.shortcuts import render
from embedding.utils import load_embedding_models, get_basic_data
import json
import random
from datetime import datetime

random.seed(datetime.now().timestamp())



def demo_pdf_async(request):
    temperature = request.POST.get('temperature', '0.9')
    question = request.POST.get('question', '')
    character = request.POST.get('character', '')
    prompt = get_embedding_prompt(question, character, model='glm')
    print(prompt)
    gml_response, _ = feature_glm('', prompt, temperature)
    print(gml_response)
    return HttpResponse(json.dumps({'result': gml_response['ai_message']}))


def demo_summary_async(request):
    temperature = request.POST.get('temperature', '0.9')
    original_text = request.POST.get('original_text', '')
    prompt = get_summary_prompt(request.POST.get('prompt', ''), original_text)
    print(prompt)
    gml_response, _ = feature_glm('', prompt, temperature)
    print(gml_response)
    return HttpResponse(json.dumps({'result': gml_response['ai_message']}))


def get_summary_prompt(prompt, original_text):
    return prompt + "\n" + original_text


def demo_pdf(request):
    ret = get_basic_data(request)
    ret['form'] = DemoForm()
    load_embedding_models(request, ret)
    return render(request, 'embedding/demo_pdf.html', ret)


def demo_summary(request):
    ret = get_basic_data(request)
    ret['form'] = DemoForm()
    load_embedding_models(request, ret)
    return render(request, 'embedding/demo_summary.html', ret)