from django.http import HttpResponse
from embedding.forms.image import ImageForm
from embedding.openai.features import feature_image
from django.shortcuts import render
from embedding.utils import get_basic_data, record_consumption
import embedding.static_values as sc
import json


def image_async(request):
    description = request.POST.get('original_text', '')
    style = request.POST.get('style', '')
    count = request.POST.get('count', '3')
    count = int(count)
    if style != '':
        description += '. In ' + style + ' style.'
    openai_response = feature_image(description, count)
    record_consumption(
        request, sc.MODEL_TYPES_IMAGE, openai_response)
    return HttpResponse(json.dumps({'urls': openai_response['data']}))


def image(request):
    ret = get_basic_data(request)
    ret['form'] = ImageForm()
    return render(request, 'embedding/image.html', ret)