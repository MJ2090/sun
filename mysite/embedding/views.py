from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from embedding.forms.training import TrainingForm
from embedding.forms.translation import TranslationForm
from embedding.openai.run4 import run_it_4
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


def answer(request):
    return render(request, 'embedding/answer.html', {'aa': 'sssss'})


def translation(request):
    # if this is a POST request we need to process the form data
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
