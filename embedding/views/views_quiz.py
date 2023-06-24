from django.http import HttpResponse
from django.utils.translation import activate
from embedding.forms.quiz import QuizForm
from embedding.openai.features import feature_quiz
from embedding.models import OcrRecord, QuizRecord
from django.shortcuts import render
from embedding.utils import save_to_local, get_basic_data, get_user, record_consumption
from embedding.ocr import recognize_image
import embedding.static_values as sc
import json
import time
from django.utils.translation import gettext as _


def quiz_async(request):
    original_image = request.FILES.get('original_image')
    saved_file_name = save_to_local(original_image)
    ocr_result, request_time = recognize_image(saved_file_name)
    ocr_result = ocr_result.replace(r'\n+', '\n')
    llm_model = request.POST.get('llm_model')
    print("ocr_result: ", ocr_result)
    openai_response, request_time = feature_quiz(ocr_result, model=llm_model)
    ai_message = openai_response["choices"][0]["message"]["content"]
    return HttpResponse(json.dumps({'question': ocr_result, 'answer': ai_message}))


def quiz_image_async(request):
    original_image = request.FILES.get('original_image')
    saved_file_name = save_to_local(original_image)
    ocr_result, request_time = recognize_image(saved_file_name)
    ocr_result = ocr_result.replace(r'\n+', '\n')
    print("ocr_result: ", ocr_result)
    ocr_record(request, saved_file_name, ocr_result, request_time)
    return HttpResponse(json.dumps({'question': ocr_result}))


def quiz_question_async(request):
    # user_language = "zh_hans"
    # activate(user_language)
    llm_model_dic = {'kuai': 'gpt-3.5-turbo', 
                     'zhun': 'gpt-4',
                     'q_1': 'gpt-4', 
                     'q_2': 'gpt-4',
                     '': 'gpt-3.5-turbo'}
    fe_model = request.POST.get('llm_model', '')
    llm_model = llm_model_dic.get(fe_model)
    original_question = request.POST.get('original_question')
    openai_response, request_time = feature_quiz(
        original_question, model=llm_model, q_type=fe_model)
    if openai_response == 'ERROR':
        ai_message = _('Sorry but we have encountered an error.')
        error_msg = 'ERROR'
    else:
        record_consumption(request, sc.MODEL_TYPES_QUIZ, openai_response)
        ai_message = openai_response["choices"][0]["message"]["content"]
        error_msg = ''
    quiz_record(request, original_question,
                ai_message, llm_model, request_time, openai_response)
    ret = {'answer': ai_message, 'error_msg': error_msg}
    return HttpResponse(json.dumps(ret))


def quiz_record(request, question, answer, llm_model, request_time, openai_response):
    response_time = time.time()
    if "usage" in openai_response:
        token_request = openai_response["usage"]["prompt_tokens"]
        token_response = openai_response["usage"]["completion_tokens"]
    else:
        token_request = -1
        token_response = -1
    record = QuizRecord.objects.create(user=get_user(request),
                                       answer=answer,
                                       question=question,
                                       response_time=response_time,
                                       llm_model=llm_model,
                                       request_time=request_time,
                                       token_request=token_request,
                                       token_response=token_response)
    record.save()


def quiz(request):
    # user_language = "zh_hans"
    # activate(user_language)
    ret = get_basic_data(request)
    ret['form'] = QuizForm()
    return render(request, 'embedding/quiz.html', ret)


def q(request):
    # user_language = "zh_hans"
    # activate(user_language)
    ret = get_basic_data(request)
    ret['form'] = QuizForm()
    return render(request, 'embedding/q.html', ret)


def ocr_record(request, image_path, ocr_result, request_time):
    response_time = time.time()
    record = OcrRecord.objects.create(user=get_user(request),
                                      image_path=image_path,
                                      question=ocr_result,
                                      response_time=response_time,
                                      request_time=request_time)
    record.save()
