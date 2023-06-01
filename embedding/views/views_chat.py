from django.http import HttpResponse
from embedding.forms.chat import ChatForm
from embedding.polly.audio import generate_audio
from embedding.openai.features import feature_action, feature_question, feature_chat, feature_chat_llama
from embedding.models import TherapyProfile, PromptModel, EmbeddingModel
from django.shortcuts import render
from embedding.utils import record_dialogue, load_random_emoji, load_random_string, get_basic_data, record_consumption
import embedding.static_values as sc
import json


def chat_async_customer_service(request):
    new_message = request.POST['message']
    use_embedding = request.POST.get('use_embedding')
    use_embedding = True
    use_gpt = True
    use_action = True
    return_dict = {}

    if use_embedding:
        embedding_model = EmbeddingModel.objects.get(uuid='NX32LBMJ3E')
        answer = feature_question(new_message, embedding_model)
        if not answer == "I don't know.":
            return_dict['ai_message'] = answer
            # return HttpResponse(json.dumps({'ai_message': answer}))
    if use_action:
        openai_response = feature_action(new_message, model='gpt-3.5-turbo')
        action_score = openai_response["choices"][0]["message"]["content"]
        action_score = action_score.replace(
            '.', '').replace('\n', '').replace(' ', '')
        print('action_score= ', action_score, action_score.isnumeric())
        if action_score.isnumeric() and int(action_score) >= 80:
            print('inside')
            answer = "You can do a free self assessment by clicking the link below."
            return_dict['action_message'] = answer
            return_dict['ai_action'] = 1

    if len(return_dict) > 0:
        return HttpResponse(json.dumps(return_dict))

    if not use_gpt:
        return HttpResponse(json.dumps({'ai_message': 'Sorry, but I cannot help you with that.'}))

    my_m = PromptModel.objects.get(name='Done FAQ')
    messages = json.loads(my_m.history)
    history = request.POST.get('history')
    print("history: ", history)
    my_json = json.loads(history)
    messages.extend(my_json)
    messages.append({"role": "user", "content": new_message})

    print("Msg sent to openai: ", messages)

    openai_response, request_time = feature_chat(
        messages, model='gpt-3.5-turbo')
    ai_message = openai_response["choices"][0]["message"]["content"]
    print("\nMsg returned from openai: ", ai_message)
    record_consumption(request, sc.MODEL_TYPES_CHAT, openai_response)

    return HttpResponse(json.dumps({'ai_message': ai_message}))


def chat_async(request):
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


def chat_therapy_gpt(request):
    ret = get_basic_data(request)
    form = ChatForm()
    ret['form'] = form
    ret['welcome_word'] = 'Chat with AI Therapist'
    ret['ai_emoji'] = load_random_emoji()
    form.fields['dialogue_id'].initial = load_random_string(10)
    return render(request, 'embedding/chat_therapy.html', ret)


def chat_therapy_llama(request):
    ret = get_basic_data(request)
    form = ChatForm(initial={'source_id': 'llama'})
    ret['form'] = form
    ret['welcome_word'] = 'Chat with Llama Therapist'
    ret['ai_emoji'] = load_random_emoji()
    form.fields['dialogue_id'].initial = load_random_string(10)
    return render(request, 'embedding/chat_therapy.html', ret)


def chat_olivia(request):
    ret = get_basic_data(request, {'hide_nav': True})
    form = ChatForm(initial={'source_id': 'stateful'})
    ret['form'] = form
    ret['welcome_word'] = 'Chat with Olivia'
    ret['ai_emoji'] = load_random_emoji()
    form.fields['dialogue_id'].initial = load_random_string(10)
    return render(request, 'embedding/chat_olivia.html', ret)


def chat(request):
    ret = get_basic_data(request)
    form = ChatForm()
    ret['form'] = form
    ret['ai_emoji'] = load_random_emoji(list_id=1)
    form.fields['dialogue_id'].initial = load_random_string(10)
    return render(request, 'embedding/chat.html', ret)
