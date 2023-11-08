from django.http import HttpResponse
from embedding.forms.summary import SummaryForm
from embedding.openai.features import feature_summary
from django.shortcuts import render
from embedding.utils import get_basic_data, record_consumption
import embedding.static_values as sc
import json


def summary_async(request):
    original_text = request.POST.get('original_text', '')
    openai_response = feature_summary(original_text, model='gpt-3.5-turbo-16k')
    summary_text = openai_response.choices[0].message.content
    record_consumption(
        request, sc.MODEL_TYPES_SUMMARY, openai_response)
    print(summary_text)
    return HttpResponse(json.dumps({'result': summary_text.strip()}))


def summary(request):
    ret = get_basic_data(request)
    ret['form'] = SummaryForm()
    return render(request, 'embedding/summary.html', ret)