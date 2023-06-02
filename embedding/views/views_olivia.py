from django.http import HttpResponse
from embedding.forms.chat import ChatForm
from embedding.polly.audio import generate_audio
from embedding.openai.features import feature_chat
from embedding.models import PromptModel
from django.shortcuts import render
from embedding.utils import record_dialogue, load_random_emoji, load_random_string, get_basic_data, record_consumption
import embedding.static_values as sc
import json


def olivia_async_init(request):
    t_name = request.POST.get('t_name', '')
    t_age = request.POST.get('t_age', '')
    t_gender = request.POST.get('t_gender', '')
    

def entrance(request):
    ret = get_basic_data(request, {'hide_nav': True})
    return render(request, 'embedding/olivia_entrance.html', ret)


def chat_async_olivia(request):
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


def chat_olivia(request):
    ret = get_basic_data(request, {'hide_nav': True})
    form = ChatForm(initial={'source_id': 'stateful'})
    ret['form'] = form
    ret['welcome_word'] = 'Chat with Olivia'
    ret['ai_emoji'] = load_random_emoji()
    form.fields['dialogue_id'].initial = load_random_string(10)
    return render(request, 'embedding/chat_olivia.html', ret)