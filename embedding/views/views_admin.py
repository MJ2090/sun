from django.http import HttpResponse
from embedding.forms.prompt_model import PromptModelForm
from embedding.openai.features import feature_action, feature_question, feature_chat, feature_chat_llama
from embedding.models import PromptModel
from django.shortcuts import render
from embedding.utils import get_basic_data, get_user
import random
from datetime import datetime

random.seed(datetime.now().timestamp())


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