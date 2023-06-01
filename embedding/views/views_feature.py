from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.translation import activate
from embedding.forms.embedding import TrainingForm, QuestionForm
from embedding.forms.prompt_model import PromptModelForm
from embedding.forms.demo import DemoForm
from embedding.forms.chat import ChatForm
from embedding.vector.file_loader import load_pdf
from embedding.polly.audio import generate_audio
from embedding.openai.features import get_embedding_prompt, feature_training, feature_action, feature_question, feature_glm, feature_chat, feature_chat_llama
from embedding.models import TherapyProfile, PromptModel, EmbeddingModel, Dialogue
from django.shortcuts import render
from embedding.utils import save_to_local, load_random_string, get_basic_data, get_user, record_consumption
import embedding.static_values as sc
import json
import random
import time
from datetime import datetime

random.seed(datetime.now().timestamp())


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


def add_prompt_model(request):
    ret = get_basic_data(request)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PromptModelForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            cd = form.cleaned_data
            name = cd.get('name', '')
            history = cd.get('history')
            new_model = PromptModel.objects.create(owner=get_user(request),
                                                   name=name,
                                                   history=history)
            new_model.save()
            return HttpResponse('Done sir.')
        else:
            print("Data not clean!")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PromptModelForm()

    return render(request, 'embedding/super.html', {'form': form, })


def sendchat_home(request):
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


def demo_pdf_async(request):
    temperature = request.POST.get('temperature', '0.9')
    question = request.POST.get('question', '')
    character = request.POST.get('character', '')
    prompt = get_embedding_prompt(question, character, model='glm')
    print(prompt)
    gml_response, _ = feature_glm(request, '', prompt, temperature)
    print(gml_response)
    return HttpResponse(json.dumps({'result': gml_response['ai_message']}))


def demo_summary_async(request):
    temperature = request.POST.get('temperature', '0.9')
    original_text = request.POST.get('original_text', '')
    prompt = get_summary_prompt(request.POST.get('prompt', ''), original_text)
    print(prompt)
    gml_response, _ = feature_glm(request, '', prompt, temperature)
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


def record_dialogue(request, role, message, dialogue_id, source='chat', request_time=0):
    response_time = time.time()
    dialogue = Dialogue.objects.create(
        role=role, message=message, dialogue_id=dialogue_id, source=source, request_time=request_time, response_time=response_time)
    dialogue.save()


def load_embedding_models(request, ret):
    owned_models = []
    public_models = []
    if not request.user.is_authenticated:
        public_models = EmbeddingModel.objects.filter(is_public=True)
    else:
        owned_models = EmbeddingModel.objects.filter(owner=request.user)
        public_models = EmbeddingModel.objects.filter(
            is_public=True).exclude(owner=request.user)

    ret['form'].fields['character'].choices = []
    for my_model in owned_models:
        ret['form'].fields['character'].choices.append(
            (my_model.uuid, my_model.name))
    for my_model in public_models:
        ret['form'].fields['character'].choices.append(
            (my_model.uuid, my_model.name))