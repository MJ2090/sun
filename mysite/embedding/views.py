from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from embedding.forms.training import TrainingForm
from embedding.forms.translation import TranslationForm
from embedding.forms.grammar import GrammarForm
from embedding.forms.summary import SummaryForm
from embedding.forms.image import ImageForm
from embedding.forms.chat import ChatForm
from embedding.forms.signuo import SignupForm
from embedding.openai.run3 import run_it_3
from embedding.openai.run4 import run_it_4
from embedding.openai.run5 import run_it_5
from embedding.openai.run6 import run_it_6
from embedding.openai.run7 import run_it_7
from embedding.openai.run8 import run_it_8
from django.shortcuts import render


def home(request):
    return render(request, 'embedding/home.html', {'aa': 'sssss'})


def embedding(request):
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
            return render(request, 'embedding/answer.html', {'ans': ans})
        else:
            print("Data not clean!")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TrainingForm()

    return render(request, 'embedding/embedding.html', {'form': form, 'aa': 'sssss'})


def sendchat(request):
    message = request.POST['message']
    password = request.POST['password']
    if password != "sky":
        return HttpResponse("wrong secret word.")

    pre_text = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n"
    post_text = "\nAI: "
    openai_response = run_it_7(pre_text + message + post_text)
    ai_message = openai_response["choices"][0]["text"]
    return HttpResponse(message + post_text + ai_message + "\nHuman: ")


def chat(request):
    initial_dict = {"message": 'Human: '}
    form = ChatForm(initial = initial_dict)
    return render(request, 'embedding/chat.html', {'form': form})


def answer(request):
    return render(request, 'embedding/answer.html')


def about(request):
    return render(request, 'embedding/about.html')


def contact(request):
    return render(request, 'embedding/contact.html')


def signin(request):
    return render(request, 'embedding/signin.html')


def signup_async(request):
    return True


def signup(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SignupForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            if form.cleaned_data["password"] != "sky":
                return render(request, 'embedding/error.html', {})
            original_text = form.cleaned_data["text"]
            openai_response = run_it_6(original_text)
            summary_text = openai_response["choices"][0]["text"]
            print(summary_text)
            return render(request, 'embedding/answer.html', {'summary_text': summary_text})
        else:
            print("Data not clean!")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SignupForm()

    return render(request, 'embedding/signup.html', {'form': form})


def translation(request):
    # if this is a POST request we need to process the form data
    print('iom here trans')
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TranslationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            if form.cleaned_data["password"] != "sky":
                return render(request, 'embedding/error.html', {})
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            original_text = form.cleaned_data["text"]
            openai_response = run_it_4(original_text)
            translated_text = openai_response["choices"][0]["text"]
            print(translated_text)
            return render(request, 'embedding/answer.html', {'translated_text': translated_text})
        else:
            print("Data not clean!")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TranslationForm()

    return render(request, 'embedding/translation.html', {'form': form, 'aa': 'sssss'})


def image(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ImageForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            if form.cleaned_data["password"] != "sky":
                return render(request, 'embedding/error.html', {})
            description = form.cleaned_data["text"]
            openai_response = run_it_8(description)
            image_url = openai_response['data'][0]['url']
            print(image_url)
            return render(request, 'embedding/answer.html', {'image_url': image_url})
        else:
            print("Data not clean!")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ImageForm()

    return render(request, 'embedding/image.html', {'form': form})


def grammar(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = GrammarForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            if form.cleaned_data["password"] != "sky":
                return render(request, 'embedding/error.html', {})
            original_text = form.cleaned_data["text"]
            openai_response = run_it_5(original_text)
            fixed_text = openai_response["choices"][0]["text"]
            print(fixed_text)
            return render(request, 'embedding/answer.html', {'fixed_text': fixed_text})
        else:
            print("Data not clean!")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = GrammarForm()

    return render(request, 'embedding/grammar.html', {'form': form})


def summary(request):
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
            return render(request, 'embedding/answer.html', {'summary_text': summary_text})
        else:
            print("Data not clean!")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SummaryForm()

    return render(request, 'embedding/summary.html', {'form': form})