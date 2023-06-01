from django.http import StreamingHttpResponse, HttpResponse
from embedding.forms.translation import TranslationForm
from embedding.openai.features import feature_translate
from django.shortcuts import render
from embedding.utils import get_basic_data, record_consumption
import embedding.static_values as sc
import json


def translation_async(request):
    original_text = request.POST.get('original_text', '')
    target = request.POST.get('target', '')
    openai_response = feature_translate(
        original_text, target=target, model='gpt-3.5-turbo')
    translated_text = openai_response['choices'][0]['message']['content']
    record_consumption(
        request, sc.MODEL_TYPES_TRANSLATE, openai_response)
    print(translated_text)
    return HttpResponse(json.dumps({'result': translated_text.strip()}))


def translation(request):
    ret = get_basic_data(request)
    ret['form'] = TranslationForm()
    return render(request, 'embedding/translation.html', ret)


def stream_async(request):
    original_text = request.POST.get('original_text', '')
    target = request.POST.get('target', '')
    def event_stream():
        openai_response = feature_translate(
            original_text, target=target, model='gpt-3.5-turbo', stream=True)
        for line in openai_response:
            finished = line['choices'][0].get('finish_reason') == 'stop'
            if finished:
                yield '\n'
                break
            chunk = line['choices'][0].get('delta', {}).get('content', '')
            if chunk:
              yield chunk
    ret = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
    ret['X-Accel-Buffering'] = 'no'
    ret['Cache-Control'] = 'no-cache'
    return ret


def stream_async_get(request):
    import openai
    def event_stream():
        completion = openai.ChatCompletion.create(
            model='gpt-3.5-turbo', 
            messages=[{"role": "user", "content": "tell me a long story"}],
            stream=True)
        for line in completion:
            print(line)
            chunk = line['choices'][0].get('delta', {}).get('content', '')
            if chunk:
              yield 'data: %s\n\n' % chunk
    ret = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
    ret['X-Accel-Buffering'] = 'no'
    ret['Cache-Control'] = 'no-cache'
    return ret


def stream(request):
    ret = get_basic_data(request)
    ret['form'] = TranslationForm()
    return render(request, 'embedding/stream.html', ret)