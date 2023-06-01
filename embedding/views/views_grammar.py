from django.http import HttpResponse
from embedding.forms.grammar import GrammarForm
from embedding.openai.features import feature_grammar
from django.shortcuts import render
from embedding.utils import get_basic_data, parse_diff, record_consumption
import embedding.static_values as sc
import json


def grammar_async(request):
    original_text = request.POST.get('original_text', '')
    openai_response = feature_grammar(original_text, model='gpt-3.5-turbo')
    fixed_text = openai_response["choices"][0]["message"]["content"]
    record_consumption(
        request, sc.MODEL_TYPES_GRAMMAR, openai_response)
    print(fixed_text)
    return HttpResponse(json.dumps({'plain_result': fixed_text.strip(), 'dict': parse_diff(original_text, fixed_text.strip())}))


def grammar(request):
    ret = get_basic_data(request)
    ret['form'] = GrammarForm()
    return render(request, 'embedding/grammar.html', ret)