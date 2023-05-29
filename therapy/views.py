from django.shortcuts import render

# Create your views here.



def therapy(request):
    ret = {}
    return render(request, 'therapy/home.html', ret)