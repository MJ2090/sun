from django.http import HttpResponse
from embedding.forms.chat import ChatForm
from embedding.polly.audio import generate_audio
from embedding.openai.features import feature_chat, feature_chat_llama
from embedding.models import TherapyProfile, PromptModel, Dialogue
from django.shortcuts import render
from embedding.utils import load_random_string, get_basic_data, record_consumption
import embedding.static_values as sc
import json
import random
import time
from datetime import datetime

random.seed(datetime.now().timestamp())


def sendchat_async(request):
    model = request.POST.get('model', '')
    new_message = request.POST['message']
    character = request.POST['character']
    enable_speech = request.POST.get('enable_speech', '')
    dialogue_id = request.POST.get('dialogue_id', '')

    my_m = PromptModel.objects.get(name=character)
    messages = json.loads(my_m.history)
    history = request.POST.get('history')
    my_json = json.loads(history)
    for item in my_json:
        if item['content'].strip() != '':
            messages.append(item)
    # messages.extend(my_json)
    if new_message.strip() != '':
        messages.append({"role": "user", "content": new_message})

    print("Character: ", character)
    print("Msg sent to openai: ", messages)

    openai_response, request_time = feature_chat(messages, model=model)
    ai_message = openai_response["choices"][0]["message"]["content"]
    print("\nMsg returned from openai: ", ai_message)
    record_consumption(request, sc.MODEL_TYPES_CHAT, openai_response)

    record_dialogue(request, 'User', new_message,
                    dialogue_id, request_time=request_time)
    record_dialogue(request, 'AI', ai_message, dialogue_id,
                    request_time=request_time)

    if character == '3-year-old guy':
        speaker = 'Ivy'
    elif character == 'Therapist':
        speaker = 'Salli'
    else:
        speaker = 'Zhiyu'

    if enable_speech == 'true':
        audio_address = generate_audio(ai_message, speaker)
    else:
        audio_address = ''

    return HttpResponse(json.dumps({'ai_message': ai_message, 'audio_address': audio_address}))


def sendchat_therapy_async_llama(request):
    model = 'llama'
    new_message = request.POST['message']
    enable_speech = request.POST.get('enable_speech', '')
    dialogue_id = request.POST.get('dialogue_id', '')

    history = request.POST.get('history')
    messages = json.loads(history)
    messages.append({"role": "user", "content": new_message})

    print("Msg sent to llama: ", messages)

    llama_response, request_time = feature_chat_llama(
        request, messages, model=model)
    print('llama_response = ', llama_response)
    ai_message = llama_response['ai_message']
    print("\nMsg returned from llama: ", ai_message)

    record_dialogue(request, 'User', new_message,
                    dialogue_id, 'therapy', request_time=request_time)
    record_dialogue(request, 'AI', ai_message, dialogue_id,
                    'therapy', request_time=request_time)

    speaker = 'Salli'
    if enable_speech == 'true':
        audio_address = generate_audio(ai_message, speaker)
    else:
        audio_address = ''

    return HttpResponse(json.dumps({'ai_message': ai_message, 'audio_address': audio_address}))


def sendchat_therapy_async(request):
    if request.POST.get('source_id') == 'llama':
        return sendchat_therapy_async_llama(request)
    elif request.POST.get('source_id') == 'openai':
        return sendchat_therapy_async_openai(request)
    else:
        return sendchat_async_olivia(request)
    

def sendchat_async_olivia(request):
    model = 'gpt-4'
    new_message = request.POST['message']
    character = 'TT_3'
    enable_speech = request.POST.get('enable_speech', '')
    dialogue_id = request.POST.get('dialogue_id', '')

    my_m = PromptModel.objects.get(name=character)
    messages = json.loads(my_m.history.replace('###QUESTION###', 'did you travel to a park last week?'))
    history = request.POST.get('history')
    my_json = json.loads(history)
    messages.extend(my_json)
    messages.append({"role": "user", "content": new_message})

    print("Character: ", character)
    print("Msg sent to openai: ", messages)

    openai_response, request_time = feature_chat(messages, model=model)
    ai_message = openai_response["choices"][0]["message"]["content"]
    print("\nMsg returned from openai: ", ai_message)
    record_consumption(request, sc.MODEL_TYPES_CHAT, openai_response)

    record_dialogue(request, 'User', new_message,
                    dialogue_id, 'therapy', request_time=request_time)
    record_dialogue(request, 'AI', ai_message, dialogue_id,
                    'therapy', request_time=request_time)

    speaker = 'Salli'
    if enable_speech == 'true':
        audio_address = generate_audio(ai_message, speaker)
    else:
        audio_address = ''

    return HttpResponse(json.dumps({'ai_message': ai_message, 'audio_address': audio_address}))


def sendchat_therapy_async_openai(request):
    model = 'gpt-4'
    new_message = request.POST['message']
    character = 'T3'
    enable_speech = request.POST.get('enable_speech', '')
    dialogue_id = request.POST.get('dialogue_id', '')

    my_m = PromptModel.objects.get(name=character)
    messages = json.loads(my_m.history)
    history = request.POST.get('history')
    my_json = json.loads(history)
    messages.extend(my_json)
    messages.append({"role": "user", "content": new_message})

    print("Character: ", character)
    print("Msg sent to openai: ", messages)

    openai_response, request_time = feature_chat(messages, model=model)
    ai_message = openai_response["choices"][0]["message"]["content"]
    print("\nMsg returned from openai: ", ai_message)
    record_consumption(request, sc.MODEL_TYPES_CHAT, openai_response)

    record_dialogue(request, 'User', new_message,
                    dialogue_id, 'therapy', request_time=request_time)
    record_dialogue(request, 'AI', ai_message, dialogue_id,
                    'therapy', request_time=request_time)

    speaker = 'Salli'
    if enable_speech == 'true':
        audio_address = generate_audio(ai_message, speaker)
    else:
        audio_address = ''

    return HttpResponse(json.dumps({'ai_message': ai_message, 'audio_address': audio_address}))


def chat_therapy(request):
    ret = get_basic_data(request)
    form = ChatForm()
    ret['form'] = form
    ret['welcome_word'] = 'Chat with AI Therapist'
    ret['ai_emoji'] = random.choice(
        ['🍀', '🍏', '🌗', '🌘', '🐳', '❄️', '🌵', '🪴', '🌳', '👩🏽‍⚕️', '🌱', '🌿', '☘️', '🌲'])
    form.fields['dialogue_id'].initial = load_random_string(10)
    return render(request, 'embedding/chat_therapy.html', ret)


def chat_therapy_llama(request):
    ret = get_basic_data(request)
    form = ChatForm(initial={'source_id': 'llama'})
    ret['form'] = form
    ret['welcome_word'] = 'Chat with Llama Therapist'
    ret['ai_emoji'] = random.choice(
        ['🍀', '🍃', '🌗', '🌘', '🐳', '❄️', '🍕', '🪴', '🌳', '👩🏽‍⚕️', '🌵', '🌿', '☘️', '🌲'])
    form.fields['dialogue_id'].initial = load_random_string(10)
    return render(request, 'embedding/chat_therapy.html', ret)


def chat_olivia(request):
    ret = get_basic_data(request, {'hide_nav': True})
    form = ChatForm(initial={'source_id': 'stateful'})
    ret['form'] = form
    ret['welcome_word'] = 'Chat with Olivia'
    ret['ai_emoji'] = random.choice(
        ['🍀', '🍃', '🌗', '🌘', '🐳', '❄️', '🍕', '🪴', '🌳', '👩🏽‍⚕️', '🌵', '🌿', '☘️', '🌲'])
    form.fields['dialogue_id'].initial = load_random_string(10)
    return render(request, 'embedding/chat_olivia.html', ret)


def chat(request):
    ret = get_basic_data(request)
    form = ChatForm()
    ret['form'] = form
    ret['ai_emoji'] = random.choice(['🍀', '🐳', '🌗', '🌘', '🌵', '🐙', '🐳', '😈',
                                    '🐳', '❄️', '🦖', '🌰', '🎲', '🎮', '✈️', '🚀', '🌋', '🦑', '🎉', '🪩', '🌳', '⚽️', '🏖'])
    form.fields['dialogue_id'].initial = load_random_string(10)
    return render(request, 'embedding/chat.html', ret)


def record_dialogue(request, role, message, dialogue_id, source='chat', request_time=0):
    response_time = time.time()
    dialogue = Dialogue.objects.create(
        role=role, message=message, dialogue_id=dialogue_id, source=source, request_time=request_time, response_time=response_time)
    dialogue.save()