from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.translation import activate
from embedding.forms.embedding import TrainingForm, QuestionForm
from embedding.vector.file_loader import load_pdf
from embedding.polly.audio import generate_audio
from embedding.openai.features import feature_summary, feature_add_embedding_doc, feature_training, feature_question
from embedding.models import EmbeddingDocument, EmbeddingModel
from django.shortcuts import render
from embedding.utils import move_to_static, load_embedding_models, save_to_local, get_basic_data
import json
from threading import Thread


@login_required
def embedding_training(request):
    ret = get_basic_data(request)
    ret['form'] = TrainingForm()
    return render(request, 'embedding/embedding_training.html', ret)


def embedding_add_doc_async(request):
    model = request.POST.get('model', '')
    embedding_model = EmbeddingModel.objects.get(uuid=model)
    print("original_files ", request.FILES, type(request.FILES))
    text = ''
    print(f'embedding_add_doc_async started, embedding uuid {model}')
    for _, original_file in request.FILES.items():
        pdf_file_name = save_to_local(original_file, 'pdf')
        move_to_static(pdf_file_name, pdf_file_name)
        pdf_pages = load_pdf(pdf_file_name)
        text = '\n\n'.join([page.page_content for page in pdf_pages])
        page_numbers = len(pdf_pages)
        openai_response = feature_training(text)
        print(openai_response)
        EmbeddingDocument.objects.create(
            model=embedding_model, filename=pdf_file_name, pages=page_numbers)
        feature_add_embedding_doc(embedding_model, openai_response)
    return HttpResponse(json.dumps({'result': 'docs added.'}))


@login_required
def embedding_training_async(request):
    text = request.POST.get('text', '') + '\n\n'
    name = request.POST.get('name', '')
    reject_message = request.POST.get('reject_message', '')
    print("original_pdf ", request.FILES, type(request.FILES))
    documents = {}
    for _, original_pdf in request.FILES.items():
        pdf_file_name = save_to_local(original_pdf, 'pdf')
        move_to_static(pdf_file_name, pdf_file_name)
        pdf_pages = load_pdf(pdf_file_name)
        text += '\n\n'.join([page.page_content for page in pdf_pages])
        print('current text length: ', len(text), text,
              f'current file name: {pdf_file_name}, pages: {len(pdf_pages)}')
        documents[pdf_file_name] = len(pdf_pages)
    print(f'embedding_training_async started, embedding name {name}')
    openai_response = feature_training(text)
    embedding_model = EmbeddingModel.objects.create(
        name=name, owner=request.user, uuid=openai_response, reject_message=reject_message)
    for key, v in documents.items():
        EmbeddingDocument.objects.create(
            model=embedding_model, filename=key, pages=v)
    print(openai_response)
    return HttpResponse(json.dumps({'result': f'new model {name} has finished training.'}))


def embedding_wuxi(request):
    user_language = "zh_hans"
    activate(user_language)
    ret = get_basic_data(request, {'hide_nav': True})
    ret['form'] = QuestionForm()

    load_embedding_models(request, ret)
    return render(request, 'embedding/wuxi.html', ret)


def text_summary_async(doc):
    # Define async function
    def hello_world():
        print("Hello")
        pdf_pages = load_pdf(doc.filename)
        text = '\n\n'.join([page.page_content for page in pdf_pages])
        openai_response = feature_summary(text, max_words=150)
        summary_text = openai_response["choices"][0]["message"]["content"]
        doc.summarization = summary_text
        doc.save()
        print("World finished")
    thread = Thread(target=hello_world)
    thread.start()


def embedding_fetch_model_async(request):
    uuid = request.POST.get('model', '')
    model = EmbeddingModel.objects.get(uuid=uuid)
    docs = EmbeddingDocument.objects.filter(model=model)
    res = []
    for doc in docs:
        if doc.summarization == 'Processing':
            text_summary_async(doc)
        res.append({'name': doc.filename, 'summarization': doc.summarization})
    return HttpResponse(json.dumps({'result': res}))


def embedding_question(request):
    ret = get_basic_data(request)
    ret['form'] = QuestionForm()

    load_embedding_models(request, ret)
    if len(ret['form'].fields['character'].choices) == 0:
        ret['error_msg'] = 'No Q&A bot found, please create new models.'
        return render(request, 'embedding/embedding_question.html', ret)

    return render(request, 'embedding/embedding_question.html', ret)


def embedding_question_async(request):
    question = request.POST.get('question', '')
    uuid = request.POST.get('character', '')
    enable_speech = request.POST.get('enable_speech', '')
    embedding_model = EmbeddingModel.objects.get(uuid=uuid)
    answer = feature_question(question, embedding_model)
    print(answer)

    if enable_speech == 'true':
        audio_address = generate_audio(answer, 'Stephen')
    else:
        audio_address = ''
    return HttpResponse(json.dumps({'answer': answer.strip(), 'audio_address': audio_address}))
