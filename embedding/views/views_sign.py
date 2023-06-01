from django.http import HttpResponseRedirect
from django.contrib import auth
from embedding.forms.signup import SignupForm
from embedding.forms.signin import SigninForm
from embedding.models import UserProfile
from django.shortcuts import render
from django.db import transaction
from embedding.utils import load_random_string, get_basic_data


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