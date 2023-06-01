from embedding.forms.contact import ContactForm
from embedding.forms.home_chat import HomeChatForm
from embedding.models import Contact
from django.shortcuts import render
from embedding.utils import get_basic_data


def home(request):
    ret = get_basic_data(request)
    ret['home_chat_form'] = HomeChatForm()
    ret['enable_home_chat'] = True
    return render(request, 'embedding/home.html', ret)


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