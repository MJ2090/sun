from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.utils.translation import activate
from embedding.forms.embedding import TrainingForm, QuestionForm
from embedding.forms.translation import TranslationForm
from embedding.forms.grammar import GrammarForm
from embedding.forms.prompt_model import PromptModelForm
from embedding.forms.summary import SummaryForm
from embedding.forms.demo import DemoForm
from embedding.forms.play import PlayForm
from embedding.forms.image import ImageForm
from embedding.forms.chat import ChatForm
from embedding.forms.contact import ContactForm
from embedding.forms.signup import SignupForm
from embedding.forms.signin import SigninForm
from embedding.forms.home_chat import HomeChatForm
from embedding.vector.file_loader import load_pdf
from embedding.polly.audio import generate_audio
from embedding.openai.features import get_embedding_prompt, feature_training, feature_action, feature_question, feature_glm, feature_quiz, feature_translate, feature_grammar, feature_summary, feature_image, feature_chat, feature_chat_llama
from embedding.models import TokenConsumption, PromptModel, EmbeddingModel, OcrRecord, QuizRecord, UserProfile, Contact, Dialogue
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
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from django.core.files.storage import default_storage
from PIL import Image

random.seed(datetime.now().timestamp())


def home(request):
    ret = get_basic_data(request)
    ret['home_chat_form'] = HomeChatForm()
    ret['enable_home_chat'] = True
    return render(request, 'embedding/home.html', ret)


@login_required
def embedding_training(request):
    ret = get_basic_data(request)
    ret['form'] = TrainingForm()
    return render(request, 'embedding/embedding_training.html', ret)


@login_required
def embedding_training_async(request):
    text = request.POST.get('text', '')
    name = request.POST.get('name', '')
    original_pdf = request.FILES.get('original_pdf', '')
    if original_pdf != '':
        pdf_file_name = save_to_local(original_pdf, 'pdf')
        pdf_pages = load_pdf(pdf_file_name)
        print(pdf_pages[0].page_content)
        text = pdf_pages[0].page_content
    print('embedding_training_async', name)
    openai_response = feature_training(text)
    new_model = EmbeddingModel.objects.get_or_create(
        name=name, owner=request.user, uuid=openai_response)
    print(openai_response)
    return HttpResponse(json.dumps({'result': 'new model ' + name + ' has finished training.'}))


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
    answer = feature_question(question, character)
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
        answer = feature_question(new_message, 'NX32LBMJ3E')
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
    print("in llama")
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
    else:
        return sendchat_therapy_async_openai(request)


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


def chat(request):
    ret = get_basic_data(request)
    form = ChatForm()
    ret['form'] = form
    ret['ai_emoji'] = random.choice(['🍀', '🐳', '🌗', '🌘', '🌵', '🐙', '🐳', '😈',
                                    '🐳', '❄️', '🦖', '🌰', '🎲', '🎮', '✈️', '🚀', '🌋', '🦑', '🎉', '🪩', '🌳', '⚽️', '🏖'])
    form.fields['dialogue_id'].initial = load_random_string(10)
    return render(request, 'embedding/chat.html', ret)


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


def lab(request):
    ret = get_basic_data(request)
    ret['current_page'] = 'lab'
    ret['enable_home_chat'] = True
    ret['home_chat_form'] = HomeChatForm()
    return render(request, 'embedding/home.html', ret)


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


def signout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return HttpResponseRedirect('/')


def signin(request):
    ret = get_basic_data(request)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SigninForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            if do_login(request, username, password):
                # Redirect to a success page.
                next_url = form.cleaned_data.get('next', '/')
                if (not next_url) or next_url.strip() == '':
                    next_url = '/'
                return HttpResponseRedirect(next_url)
            else:
                return render(request, 'embedding/error.html', {'error_message': 'Your account does not exist or has been accidently deleted, sorry about that.'})
        else:
            print("Data not clean!")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SigninForm()
        form.fields['next'].initial = request.GET.get('next', None)

    ret['form'] = form
    return render(request, 'embedding/signin.html', ret)


def signup_async(request):
    return True


def signup(request):
    ret = get_basic_data(request)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SignupForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            cd = form.cleaned_data
            username = cd["username"]
            password = cd["password"]
            do_register(cd)
            do_login(request, username, password)
            return HttpResponseRedirect("/")
        else:
            print("Data not clean!")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SignupForm()
    ret['form'] = form
    return render(request, 'embedding/signup.html', ret)


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


def translation_async(request):
    original_text = request.POST.get('original_text', '')
    target = request.POST.get('target', '')
    openai_response = feature_translate(
        original_text, target=target, model='gpt-3.5-turbo')
    translated_text = openai_response['choices'][0]['message']['content']
    record_consumption(
        request, sc.MODEL_TYPES_TRANSLATE, openai_response)
    print(translated_text)
    return HttpResponse(json.dumps({'result': translated_text.strip()}))


def translation(request):
    ret = get_basic_data(request)
    ret['form'] = TranslationForm()
    return render(request, 'embedding/translation.html', ret)


def grammar_async(request):
    original_text = request.POST.get('original_text', '')
    openai_response = feature_grammar(original_text, model='gpt-3.5-turbo')
    fixed_text = openai_response["choices"][0]["message"]["content"]
    record_consumption(
        request, sc.MODEL_TYPES_GRAMMAR, openai_response)
    print(fixed_text)
    return HttpResponse(json.dumps({'plain_result': fixed_text.strip(), 'dict': parse_diff(original_text, fixed_text.strip())}))


def grammar(request):
    ret = get_basic_data(request)
    ret['form'] = GrammarForm()
    return render(request, 'embedding/grammar.html', ret)


def summary_async(request):
    original_text = request.POST.get('original_text', '')
    openai_response = feature_summary(original_text, model='gpt-3.5-turbo')
    summary_text = openai_response["choices"][0]["message"]["content"]
    record_consumption(
        request, sc.MODEL_TYPES_SUMMARY, openai_response)
    print(summary_text)
    return HttpResponse(json.dumps({'result': summary_text.strip()}))


def summary(request):
    ret = get_basic_data(request)
    ret['form'] = SummaryForm()
    return render(request, 'embedding/summary.html', ret)


def demo_async(request):
    original_text = request.POST.get('original_text', '')
    temperature = request.POST.get('temperature', '0.9')
    question = request.POST.get('question', '')
    character = request.POST.get('character', '')
    if question != '':
        prompt = get_embedding_prompt(question, character, model='glm')
    else:
        prompt = request.POST.get('prompt', '')
    print(prompt)
    gml_response, _ = feature_glm(request, original_text, prompt, temperature)
    print(gml_response)
    return HttpResponse(json.dumps({'result': gml_response['ai_message']}))


def demo(request):
    ret = get_basic_data(request)
    ret['form'] = DemoForm()
    load_embedding_models(request, ret)
    return render(request, 'embedding/demo.html', ret)


def play_async(request):
    original_image = request.FILES.get('original_image')
    saved_file_name = save_to_local(original_image)
    ocr_result, request_time = recognize_image(saved_file_name)
    ocr_result = ocr_result.replace(r'\n+', '\n')
    llm_model = request.POST.get('llm_model')
    print("ocr_result: ", ocr_result)
    openai_response, request_time = feature_quiz(ocr_result, model=llm_model)
    ai_message = openai_response["choices"][0]["message"]["content"]
    print("openai_response: ", openai_response)
    return HttpResponse(json.dumps({'question': ocr_result, 'answer': ai_message}))


def play_image_async(request):
    original_image = request.FILES.get('original_image')
    saved_file_name = save_to_local(original_image)
    ocr_result, request_time = recognize_image(saved_file_name)
    ocr_result = ocr_result.replace(r'\n+', '\n')
    print("ocr_result: ", ocr_result)
    ocr_record(request, saved_file_name, ocr_result, request_time)
    return HttpResponse(json.dumps({'question': ocr_result}))


def ocr_record(request, image_path, ocr_result, request_time):
    response_time = time.time()
    record = OcrRecord.objects.create(user=get_user(request),
                                      image_path = image_path,
                                      question = ocr_result,
                                      response_time = response_time,
                                      request_time = request_time)
    record.save()


def play_question_async(request):
    llm_model_dic = {'kuai': 'gpt-3.5-turbo', 'zhun': 'gpt-4'}
    llm_model = llm_model_dic.get(request.POST.get('llm_model'))
    original_question = request.POST.get('original_question')
    openai_response, request_time = feature_quiz(
        original_question, model=llm_model)
    record_consumption(request, sc.MODEL_TYPES_QUIZ, openai_response)
    ai_message = openai_response["choices"][0]["message"]["content"]
    print("openai_response: ", openai_response)
    quiz_record(request, original_question, ai_message, llm_model, request_time)
    return HttpResponse(json.dumps({'answer': ai_message}))


def quiz_record(request, question, answer, llm_model, request_time):
    response_time = time.time()
    record = QuizRecord.objects.create(user=get_user(request),
                                      answer = answer,
                                      question = question,
                                      response_time = response_time,
                                      llm_model = llm_model,
                                      request_time = request_time)
    record.save()


def play(request):
    user_language = "zh_hans"
    activate(user_language)
    ret = get_basic_data(request)
    ret['form'] = PlayForm()
    return render(request, 'embedding/play.html', ret)


def quiz(request):
    user_language = "zh_hans"
    activate(user_language)
    ret = get_basic_data(request)
    ret['form'] = PlayForm()
    return render(request, 'embedding/quiz.html', ret)


def save_to_local(original_file, sub_dir=''):
    random_prefix = load_random_string(15) + "_"
    file_dir = conf_settings.UPLOADS_PATH + '/' + sub_dir
    if not os.path.isdir(file_dir):
        print("mkdir in save_to_local.. ", file_dir)
        os.mkdir(file_dir)
    file_name = default_storage.save(os.path.join(
        file_dir, random_prefix+original_file.name), original_file)
    if sub_dir == '' and original_file.size > 3*1000*1000:
        tmp = Image.open(file_name)
        max_size = (1024, 1024)
        tmp.thumbnail(max_size, Image.ANTIALIAS)
        tmp.save(file_name, optimize=True, quality=85)
        print("size recuded: ", original_file.size,
              ' to ', os.path.getsize(file_name), tmp.size)
    return file_name


@login_required
def collection(request):
    ret = get_basic_data(request)
    ret['current_page'] = 'collection'
    return render(request, 'embedding/collection.html', ret)


def pricing(request):
    ret = get_basic_data(request)
    ret['current_page'] = 'pricing'
    return render(request, 'embedding/pricing.html', ret)


def do_login(request, username, password):
    user = auth.authenticate(username=username, password=password)
    if user:
        auth.login(request, user)
        return True
    return False


def do_register(cd):
    with transaction.atomic():
        userProfile = UserProfile.objects.create_user(username=cd.get('username', ''),
                                                      password=cd.get(
                                                          'password', ''),
                                                      )
        userProfile.is_staff = False
        userProfile.is_superuser = False
        userProfile.external_id = load_random_string(20)
        userProfile.save()
    return userProfile


def record_dialogue(request, role, message, dialogue_id, source='chat', request_time=0):
    response_time = time.time()
    dialogue = Dialogue.objects.create(
        role=role, message=message, dialogue_id=dialogue_id, source=source, request_time=request_time, response_time=response_time)
    dialogue.save()


def record_consumption(request, model_type, openai_response, secret=''):
    with transaction.atomic():
        if model_type == sc.MODEL_TYPES_IMAGE:
            token_amount = 0
        else:
            token_amount = openai_response["usage"]["total_tokens"]
        consumption = TokenConsumption.objects.create(user=get_user(request),
                                                      model_type=model_type,
                                                      token_amount=token_amount,
                                                      secret=secret)
        consumption.save()
        if request.user.is_authenticated:
            request.user.left_token -= token_amount
            request.user.used_token += token_amount
            request.user.save()


def get_user(request):
    if request.user.is_authenticated:
        return request.user
    return UserProfile.objects.get(username="default_user")
