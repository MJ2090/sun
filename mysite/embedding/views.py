from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from embedding.forms.training import TrainingForm
from embedding.openai.run3 import run_it_3
from django.shortcuts import render


def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TrainingForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            my_text = form.cleaned_data["message"]
            qs = [form.cleaned_data["q1"]]
            if "q2" in form.cleaned_data:
                qs.append(form.cleaned_data["q2"])
            if "q3" in form.cleaned_data:
                qs.append(form.cleaned_data["q3"])
            if "q4" in form.cleaned_data:
                qs.append(form.cleaned_data["q4"])
            print(my_text, qs)
            ans = run_it_3(my_text, qs)
            return HttpResponseRedirect("thanks/")
        else:
            print("Data not clean!")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TrainingForm()

    return render(request, 'embedding/index.html', {'form': form, 'aa': 'sssss'})


def thanks(request):
    return render(request, 'embedding/thanks.html', {'aa': 'sssss'})