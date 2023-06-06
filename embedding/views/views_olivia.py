from django.http import HttpResponse
from embedding.forms.chat import ChatForm
from embedding.polly.audio import generate_audio
from embedding.openai.features import feature_chat
from embedding.models import PromptModel, VisitorProfile
from django.shortcuts import render
from embedding.utils import get_int, load_random_greeting, record_dialogue, load_random_emoji, load_random_string, get_basic_data, record_consumption
import embedding.static_values as sc
import json


def olivia_async_chat(request):
    model = 'gpt-4'
    new_message = request.POST.get('message')
    uuid = request.POST.get('uuid', '')
    history_json = json.loads(request.POST.get('history', ''))

    base_prompt = """
    You act as a professional therapist who uses Cognitive Behavioral Therapy to treat patients. You must respect these rules: 
    #1. If visitors want to commit suicide or hurt someone, immediately lead them to hotline 988 or 911. 
    #2. Do not answer questions irrelevant to therapy, for example mathematical or political questions. 
    #3. If asked who you are, you are an AI powered therapist, never mention GPT or OpenAI.
    """
    user_prompt = """
    The visitor's name is Maria, and she is 23 years old."""
    prompt = base_prompt + user_prompt
    messages = [{"role": "system", "content": prompt}]
    messages.extend(history_json)
    messages.append({"role": "user", "content": new_message})

    print("\nMsg sent to openai: ", messages)
    openai_response, _ = feature_chat(messages, model=model)
    ai_message = openai_response["choices"][0]["message"]["content"]
    print("\nMsg returned from openai: ", ai_message)

    return HttpResponse(json.dumps({'ai_message': ai_message}))


def olivia_async_init(request):
    t_name = request.POST.get('t_name', '')
    t_age = get_int(request.POST.get('t_age', ''))
    t_gender = request.POST.get('t_gender', '')
    uuid = load_random_string(10)
    VisitorProfile.objects.create(
        uuid=uuid, username=t_name, age=t_age, gender=t_gender)
    greeting = load_random_greeting(t_name)
    base_prompt = """
    You act as a professional therapist who uses Cognitive Behavioral Therapy to treat patients. You must respect these rules: 
    #1. If visitors want to commit suicide or hurt someone, immediately lead them to hotline 988 or 911. 
    #2. Do not answer questions irrelevant to therapy, for example mathematical or political questions. 
    #3. If asked who you are, you are an AI powered therapist, never mention GPT or OpenAI.
    """
    return HttpResponse(json.dumps({'ai_message': greeting}))


def entrance(request):
    ret = get_basic_data(request, {'hide_nav': True})
    return render(request, 'embedding/olivia_entrance.html', ret)