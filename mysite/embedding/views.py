from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from embedding.forms.training import TrainingForm
from embedding.forms.translation import TranslationForm
from embedding.forms.grammar import GrammarForm
from embedding.forms.summary import SummaryForm
from embedding.forms.image import ImageForm
from embedding.forms.chat import ChatForm
from embedding.forms.contact import ContactForm
from embedding.forms.signup import SignupForm
from embedding.forms.signin import SigninForm
from embedding.openai.run3 import run_it_3
from embedding.openai.run4 import run_it_4
from embedding.openai.run5 import run_it_5
from embedding.openai.run6 import run_it_6
from embedding.openai.run7 import run_it_7
from embedding.openai.run8 import run_it_8
from embedding.models import TokenConsumption
from django.shortcuts import render
from django.db import transaction
from .utils import load_random_string, get_basic_data
from embedding.models import UserProfile
import embedding.static_values as sc


def home(request):
    ret = get_basic_data(request)
    return render(request, 'embedding/home.html', ret)


def embedding(request):
    ret = get_basic_data(request)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TrainingForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            if form.cleaned_data["password"] != "sky":
                return render(request, 'embedding/error.html', {})
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            my_text = form.cleaned_data["message"]
            qs = [form.cleaned_data["q1"]]
            if "q2" in form.cleaned_data and form.cleaned_data["q2"] != "":
                qs.append(form.cleaned_data["q2"])
            if "q3" in form.cleaned_data and form.cleaned_data["q3"] != "":
                qs.append(form.cleaned_data["q3"])
            if "q4" in form.cleaned_data and form.cleaned_data["q4"] != "":
                qs.append(form.cleaned_data["q4"])
            ans = run_it_3(my_text, qs)
            ret['ans'] = ans
            return render(request, 'embedding/answer.html', ret)
        else:
            print("Data not clean!")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TrainingForm()

    return render(request, 'embedding/embedding.html', {'form': form, 'aa': 'sssss'})


def sendchat(request):
    message = request.POST['message']
    password = request.POST['password']
    character = request.POST['character']
    if password != "sky":
        return HttpResponse("wrong secret word.")

    print("c is", character)
    pre_text_dict = {
        "Common AI": "",
        "Assistant": "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n",
        "Mr. President": "In this conversation, AI acts as the President Biden of USA. He serves his contry.\n",
        "Therapist": "In this conversation, AI acts as a top ranked Therapist. He always speaks a lot, providing advices to his patients. He is always nice, friendly and very helpful to his patients.\n",
    }
    print(999, pre_text_dict)
    pre_text = pre_text_dict.get(character, "")
    post_text = "\nAI: "
    openai_response = run_it_7(pre_text + message + post_text)
    ai_message = openai_response["choices"][0]["text"]
    record_consumption(request, sc.MODEL_TYPES_CHAT, openai_response, password)
    return HttpResponse(message + post_text + ai_message + "\nHuman: ")


def chat(request):
    ret = get_basic_data(request)
    initial_dict = {"message": 'Human: '}
    form = ChatForm(initial=initial_dict)
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
            print(form.cleaned_data, 88888)
            # ...
            # redirect to a new URL:
            # return render(request, 'embedding/contact.html', {'name': name})
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ContactForm()
    ret['form'] =form
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

            print(88)
            if do_login(request, username, password):
                print(881)
                # Redirect to a success page.
                print(form.cleaned_data, 4444, request.GET, request.POST)
                next_url = form.cleaned_data.get('next', '/')
                if (not next_url) or next_url.strip() == '':
                    next_url = '/'
                return HttpResponseRedirect(next_url)
            else:

                print(882)
                return render(request, 'embedding/error.html', {})
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


def translation(request):
    ret = get_basic_data(request)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TranslationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            if form.cleaned_data["password"] != "sky":
                return render(request, 'embedding/error.html', ret)
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            original_text = form.cleaned_data["text"]
            openai_response = run_it_4(original_text)
            translated_text = openai_response["choices"][0]["text"]
            print(translated_text)
            ret['translated_text'] = translated_text
            record_consumption(request, sc.MODEL_TYPES_TRANSLATE, openai_response, form.cleaned_data["password"])
            return render(request, 'embedding/answer.html', ret)
        else:
            print("Data not clean!")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TranslationForm()

    ret['form'] = form
    return render(request, 'embedding/translation.html', ret)


def image(request):
    ret = get_basic_data(request)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ImageForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            if form.cleaned_data["password"] != "sky":
                return render(request, 'embedding/error.html', ret)
            description = form.cleaned_data["text"]
            openai_response = run_it_8(description)
            image_url = openai_response['data'][0]['url']
            print(image_url)
            ret['image_url'] = image_url
            return render(request, 'embedding/answer.html', ret)
        else:
            print("Data not clean!")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ImageForm()
    ret['form'] = form
    return render(request, 'embedding/image.html', ret)


def grammar(request):
    ret = get_basic_data(request)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = GrammarForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            if form.cleaned_data["password"] != "sky":
                return render(request, 'embedding/error.html', ret)
            original_text = form.cleaned_data["text"]
            openai_response = run_it_5(original_text)
            fixed_text = openai_response["choices"][0]["text"]
            print(fixed_text)
            ret['fixed_text'] = fixed_text
            record_consumption(request, sc.MODEL_TYPES_GRAMMAR, openai_response, form.cleaned_data["password"])
            return render(request, 'embedding/answer.html', ret)
        else:
            print("Data not clean!")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = GrammarForm()

    ret['form'] = form
    return render(request, 'embedding/grammar.html', ret)


def summary(request):
    ret = get_basic_data(request)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SummaryForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            if form.cleaned_data["password"] != "sky":
                return render(request, 'embedding/error.html', {})
            original_text = form.cleaned_data["text"]
            openai_response = run_it_6(original_text)
            summary_text = openai_response["choices"][0]["text"]
            print(summary_text)
            ret['summary_text'] = summary_text
            record_consumption(request, sc.MODEL_TYPES_SUMMARY, openai_response, form.cleaned_data["password"])
            return render(request, 'embedding/answer.html', {'summary_text': summary_text})
        else:
            print("Data not clean!")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SummaryForm()

    ret['form'] = form
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
                                                      password=cd.get('password', ''),
                                                      )
        userProfile.is_staff = False
        userProfile.is_superuser = False
        userProfile.external_id = load_random_string(20)
        userProfile.save()
    return userProfile


def record_consumption(request, model_type, openai_response, secret):
    with transaction.atomic():
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
    return UserProfile.objects.get(username="a")