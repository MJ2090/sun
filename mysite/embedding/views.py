from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from embedding.forms.embedding import TrainingForm, QuestionForm
from embedding.forms.translation import TranslationForm
from embedding.forms.grammar import GrammarForm
from embedding.forms.prompt_model import PromptModelForm
from embedding.forms.summary import SummaryForm
from embedding.forms.image import ImageForm
from embedding.forms.chat import ChatForm
from embedding.forms.contact import ContactForm
from embedding.forms.signup import SignupForm
from embedding.forms.signin import SigninForm
from embedding.polly.audio import generate_audio
from embedding.openai.run import run_it_4, run_it_5, run_it_6, run_it_7, run_it_8, run_it_9
from embedding.openai.run3 import run_it_3, run_it_3_question, run_it_3_training
from embedding.models import TokenConsumption, PromptModel, EmbeddingModel
from django.shortcuts import render
from django.db import transaction
from .utils import load_random_string, get_basic_data
from embedding.models import UserProfile
from embedding.models import Contact
import embedding.static_values as sc
import json


def home(request):
    ret = get_basic_data(request)
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
    print(8888, text, name)
    openai_response = run_it_3_training(text)
    new_model = EmbeddingModel.objects.get_or_create(
        name=name, owner=request.user, uuid=openai_response)
    print(openai_response)
    return HttpResponse('new model ' + name + ' has finished training.')


def embedding_question(request):
    ret = get_basic_data(request)
    ret['form'] = QuestionForm()
    owned_models = []
    public_models = []
    if not request.user.is_authenticated:
        public_models = EmbeddingModel.objects.filter(is_public=True)
    else:
        owned_models = EmbeddingModel.objects.filter(owner=request.user)
        public_models = EmbeddingModel.objects.filter(is_public=True).exclude(owner=request.user)

    ret['form'].fields['character'].choices = []
    for my_model in owned_models:
        ret['form'].fields['character'].choices.append(
            (my_model.uuid, my_model.name))
    for my_model in public_models:
        ret['form'].fields['character'].choices.append(
            (my_model.uuid, my_model.name))
        
    if len(ret['form'].fields['character'].choices) == 0:
        ret['error_msg'] = 'No Q&A bot found, please create new models.'
        return render(request, 'embedding/embedding_question.html', ret)

    return render(request, 'embedding/embedding_question.html', ret)


def embedding_question_async(request):
    question = request.POST.get('question', '')
    character = request.POST.get('character', '')
    enable_speech = request.POST.get('enable_speech', '')
    answer = run_it_3_question(question, character)
    print(answer)

    if enable_speech == 'true':
        audio_address = generate_audio(answer, 'Zhiyu')
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


def sendchat_t(request):
    model = request.POST.get('model', '')
    new_message = request.POST['message']
    character = request.POST['character']
    enable_speech = request.POST.get('enable_speech', '')

    my_m = PromptModel.objects.get(name=character)
    messages = json.loads(my_m.history)
    history = request.POST.get('history')
    my_json = json.loads(history)
    messages.extend(my_json)
    messages.append({"role": "user", "content": new_message})

    print("Character: ", character)
    print("Msg sent to openai: ", messages)

    openai_response = run_it_9(messages, model=model)
    ai_message = openai_response["choices"][0]["message"]["content"]
    record_consumption(request, sc.MODEL_TYPES_CHAT, openai_response)

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


def sendchat(request):
    model = request.POST.get('model', '')
    if model == "gpt-3.5-turbo":
        return sendchat_t(request)
    message = request.POST['message']
    character = request.POST['character']
    history = request.POST.get('history')
    print('model is ', model, history)

    pre_text_dict = {
        "Common AI": "",
        "Assistant": "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n",
        "Mr. President": "In this conversation, AI acts as the President Biden of USA. He serves his contry.\n",
        "Therapist": "In this conversation, AI acts as a top ranked Therapist. He always speaks a lot, providing advices to his patients. He is always nice, friendly and very helpful to his patients.\n",
    }
    pre_text = pre_text_dict.get(character, "")
    post_text = "\nAI: "
    openai_response = run_it_7(pre_text + message + post_text, model=model)
    ai_message = openai_response["choices"][0]["text"]
    record_consumption(request, sc.MODEL_TYPES_CHAT, openai_response)
    return HttpResponse(message + post_text + ai_message + "\nHuman: ")


def chat(request):
    ret = get_basic_data(request)
    form = ChatForm()
    ret['form'] = form
    return render(request, 'embedding/chat.html', ret)


def answer(request):
    ret = get_basic_data(request)
    return render(request, 'embedding/answer.html', ret)


def about(request):
    ret = get_basic_data(request)
    return render(request, 'embedding/about.html', ret)


def payments(request):
    ret = get_basic_data(request)
    return render(request, 'embedding/payments.html', ret)


def settings(request):
    ret = get_basic_data(request)
    return render(request, 'embedding/settings.html', ret)


def contact(request):
    ret = get_basic_data(request)
    # if this is a POST request we need to process the form data

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ContactForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # name = form.cleaned_data["username"]
            data = Contact(username=form.cleaned_data["username"], email=form.cleaned_data["email"], message=form.cleaned_data["message"])
            data.save()
            print(form.cleaned_data, 88888)
            # ...
            # redirect to a new URL:
            # return render(request, 'embedding/contact.html', {'name': name})
            return HttpResponseRedirect('/')

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
                print(881)
                # Redirect to a success page.
                print(form.cleaned_data, 4444, request.GET, request.POST)
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
        print(884)

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


def send_translation(request):
    ret = get_basic_data(request)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TranslationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            original_text = form.cleaned_data["text"]
            openai_response = run_it_4(original_text, model='text-davinci-003')
            translated_text = openai_response["choices"][0]["text"]
            print(translated_text)
            ret['translated_text'] = translated_text
            record_consumption(
                request, sc.MODEL_TYPES_TRANSLATE, openai_response)
            return render(request, 'embedding/answer.html', ret)
        else:
            print("Data not clean!")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TranslationForm()

    ret['form'] = form
    return render(request, 'embedding/translation.html', ret)


def image_async(request):
    description = request.POST.get('original_text', '')
    style = request.POST.get('style', '')
    if style != '':
        description += '. In ' + style + ' style.'
    openai_response = run_it_8(description)
    generated_url = openai_response['data'][0]['url']
    record_consumption(
        request, sc.MODEL_TYPES_IMAGE, openai_response)
    print(generated_url)
    return HttpResponse(generated_url.strip())


def image(request):
    ret = get_basic_data(request)
    ret['form'] = ImageForm()
    return render(request, 'embedding/image.html', ret)


def translation_async(request):
    original_text = request.POST.get('original_text', '')
    openai_response = run_it_4(original_text, model='text-davinci-003')
    translated_text = openai_response["choices"][0]["text"]
    record_consumption(
        request, sc.MODEL_TYPES_TRANSLATE, openai_response)
    print(translated_text)
    return HttpResponse(translated_text.strip())


def translation(request):
    ret = get_basic_data(request)
    ret['form'] = TranslationForm()
    return render(request, 'embedding/translation.html', ret)


def grammar_async(request):
    original_text = request.POST.get('original_text', '')
    openai_response = run_it_5(original_text, model='text-davinci-003')
    fixed_text = openai_response["choices"][0]["text"]
    record_consumption(
        request, sc.MODEL_TYPES_GRAMMAR, openai_response)
    print(fixed_text)
    return HttpResponse(fixed_text.strip())


def grammar(request):
    ret = get_basic_data(request)
    ret['form'] = GrammarForm()
    return render(request, 'embedding/grammar.html', ret)


def summary_async(request):
    original_text = request.POST.get('original_text', '')
    openai_response = run_it_6(original_text, model='text-davinci-003')
    summary_text = openai_response["choices"][0]["text"]
    record_consumption(
        request, sc.MODEL_TYPES_SUMMARY, openai_response)
    print(summary_text)
    return HttpResponse(summary_text.strip())


def summary(request):
    ret = get_basic_data(request)
    ret['form'] = SummaryForm()
    return render(request, 'embedding/summary.html', ret)


@login_required
def collection(request):
    ret = get_basic_data(request)
    return render(request, 'embedding/collection.html', ret)


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
