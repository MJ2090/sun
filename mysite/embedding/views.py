from django.http import HttpResponse
from django.template import loader


def index(request):
    print(999)
    template = loader.get_template('index.html')
    context = {
        'aa': 'ssss',
    }
    return HttpResponse(template.render(context, request))