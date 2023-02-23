from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from embedding.forms.training import TrainingForm
from django.shortcuts import render


def index(request):
    template = loader.get_template('embedding/index.html')
    context = {
        'aa': 'ssss',
    }
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TrainingForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TrainingForm()

    return render(request, 'embedding/index.html', {'form': form, 'aa': 'sssss'})