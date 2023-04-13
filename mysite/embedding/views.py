from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from embedding.forms.embedding import TrainingForm, QuestionForm
from embedding.forms.translation import TranslationForm
from embedding.forms.grammar import GrammarForm
from embedding.forms.prompt_model import PromptModelForm
from embedding.forms.summary import SummaryForm
from embedding.forms.image import ImageForm
from embedding.forms.chat import ChatForm
from embedding.forms.contact import ContactForm
from embedding.forms.signup import SignupForm
from embedding.forms.signin import SigninForm
from embedding.forms.home_chat import HomeChatForm
from embedding.polly.audio import generate_audio
from embedding.openai.run import run_it_translate, run_it_grammar, run_it_summary, run_it_7, run_it_image, run_it_chat
from embedding.openai.run3 import run_it_3_action, run_it_3_question, run_it_3_training
from embedding.models import TokenConsumption, PromptModel, EmbeddingModel
from django.shortcuts import render
from django.db import transaction
from .utils import load_random_string, get_basic_data, enable_new_home, parse_diff
from embedding.models import UserProfile
from embedding.models import Contact, Dialogue
import embedding.static_values as sc
import json
import random
from datetime import datetime

random.seed(datetime.now().timestamp())

def home(request):
    ret = get_basic_data(request)
    ret['home_chat_form'] = HomeChatForm()
    ret['enable_home_chat'] = True
    return render(request, 'embedding/home.html', ret)


@login_required
def embedding_training(request):
    ret = get_basic_data(request)
    ret['form'] = TrainingForm()
    return render(request, 'embedding/embedding_training.html', ret)


@login_required
def embedding_training_async(request):
    text = request.POST.get('text', '')
    name = request.POST.get('name', '')
    print('embedding_training_async', text, name)
    openai_response = run_it_3_training(text)
    new_model = EmbeddingModel.objects.get_or_create(
        name=name, owner=request.user, uuid=openai_response)
    print(openai_response)
    return HttpResponse('new model ' + name + ' has finished training.')


def embedding_question(request):
    ret = get_basic_data(request)
    ret['form'] = QuestionForm()
    owned_models = []
    public_models = []
    if not request.user.is_authenticated:
        public_models = EmbeddingModel.objects.filter(is_public=True)
    else:
        owned_models = EmbeddingModel.objects.filter(owner=request.user)
        public_models = EmbeddingModel.objects.filter(
            is_public=True).exclude(owner=request.user)

    ret['form'].fields['character'].choices = []
    for my_model in owned_models:
        ret['form'].fields['character'].choices.append(
            (my_model.uuid, my_model.name))
    for my_model in public_models:
        ret['form'].fields['character'].choices.append(
            (my_model.uuid, my_model.name))

    if len(ret['form'].fields['character'].choices) == 0:
        ret['error_msg'] = 'No Q&A bot found, please create new models.'
        return render(request, 'embedding/embedding_question.html', ret)

    return render(request, 'embedding/embedding_question.html', ret)


def embedding_question_async(request):
    question = request.POST.get('question', '')
    character = request.POST.get('character', '')
    enable_speech = request.POST.get('enable_speech', '')
    answer = run_it_3_question(question, character)
    print(answer)

    if enable_speech == 'true':
        audio_address = generate_audio(answer, 'Stephen')
    else:
        audio_address = ''
    return HttpResponse(json.dumps({'answer': answer.strip(), 'audio_address': audio_address}))


def add_prompt_model(request):
    ret = get_basic_data(request)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PromptModelForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            cd = form.cleaned_data
            name = cd.get('name', '')
            history = cd.get('history')
            new_model = PromptModel.objects.create(owner=get_user(request),
                                                   name=name,
                                                   history=history)
            new_model.save()
            return HttpResponse('Done sir.')
        else:
            print("Data not clean!")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PromptModelForm()

    return render(request, 'embedding/super.html', {'form': form, })


def sendchat_home(request):
    new_message = request.POST['message']
    use_embedding = request.POST.get('use_embedding')
    use_embedding = True
    use_gpt = True
    use_action = True
    return_dict = {}

    if use_embedding:
        answer = run_it_3_question(new_message, 'NX32LBMJ3E')
        if not answer == "I don't know.":
            return_dict['ai_message'] = answer
            # return HttpResponse(json.dumps({'ai_message': answer}))
    if use_action:
        openai_response = run_it_3_action(new_message, model='gpt-3.5-turbo')
        action_score = openai_response["choices"][0]["message"]["content"]
        action_score = action_score.replace('.', '').replace('\n', '').replace(' ', '')
        print('action_score= ', action_score, action_score.isnumeric())
        if action_score.isnumeric() and int(action_score) >= 8:
            print('inside')
            answer = "You can do a free self assessment by clicking the link below."
            return_dict['action_message'] = answer
            return_dict['ai_action'] = 1
        
    if len(return_dict) > 0:
        return HttpResponse(json.dumps(return_dict))
    
    if not use_gpt:
        return HttpResponse(json.dumps({'ai_message': 'Sorry, but I cannot help you with that.'}))

    my_m = PromptModel.objects.get(name='Done FAQ')
    messages = json.loads(my_m.history)
    history = request.POST.get('history')
    my_json = json.loads(history)
    messages.extend(my_json)
    messages.append({"role": "user", "content": new_message})

    print("Msg sent to openai: ", messages)

    openai_response = run_it_chat(messages, model='gpt-3.5-turbo')
    ai_message = openai_response["choices"][0]["message"]["content"]
    record_consumption(request, sc.MODEL_TYPES_CHAT, openai_response)

    return HttpResponse(json.dumps({'ai_message': ai_message}))


def sendchat_async(request):
    model = request.POST.get('model', '')
    new_message = request.POST['message']
    character = request.POST['character']
    enable_speech = request.POST.get('enable_speech', '')
    dialogue_id = request.POST.get('dialogue_id', '')

    my_m = PromptModel.objects.get(name=character)
    messages = json.loads(my_m.history)
    history = request.POST.get('history')
    my_json = json.loads(history)
    messages.extend(my_json)
    messages.append({"role": "user", "content": new_message})

    print("Character: ", character)
    print("Msg sent to openai: ", messages)

    openai_response = run_it_chat(messages, model=model)
    ai_message = openai_response["choices"][0]["message"]["content"]
    record_consumption(request, sc.MODEL_TYPES_CHAT, openai_response)

    record_dialogue(request, 'User', new_message, dialogue_id)
    record_dialogue(request, 'AI', ai_message, dialogue_id)
    
    if character == '3-year-old guy':
        speaker = 'Ivy'
    elif character == 'Therapist':
        speaker = 'Salli'
    else:
        speaker = 'Zhiyu'

    if enable_speech == 'true':
        audio_address = generate_audio(ai_message, speaker)
    else:
        audio_address = ''

    return HttpResponse(json.dumps({'ai_message': ai_message, 'audio_address': audio_address}))


def sendchat(request):
    model = request.POST.get('model', '')
    if model == "gpt-3.5-turbo":
        return sendchat_async(request)
    message = request.POST['message']
    character = request.POST['character']
    history = request.POST.get('history')
    print('model is ', model, history)

    pre_text_dict = {
        "Common AI": "",
        "Assistant": "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n",
        "Mr. President": "In this conversation, AI acts as the President Biden of USA. He serves his contry.\n",
        "Therapist": "In this conversation, AI acts as a top ranked Therapist. He always speaks a lot, providing advices to his patients. He is always nice, friendly and very helpful to his patients.\n",
    }
    pre_text = pre_text_dict.get(character, "")
    post_text = "\nAI: "
    openai_response = run_it_7(pre_text + message + post_text, model=model)
    ai_message = openai_response["choices"][0]["text"]
    record_consumption(request, sc.MODEL_TYPES_CHAT, openai_response)
    return HttpResponse(message + post_text + ai_message + "\nHuman: ")


def chat(request):
    ret = get_basic_data(request)
    form = ChatForm()
    ret['form'] = form
    ret['ai_emoji'] = random.choice(['🍀','🌖','🌗','🌘','🔥','🐙','🐳','😈','👑','❄️','🍕','🌰','🎲','🎮','✈️','🚀','🌋','🧸','🎉','🪩','🍯'])
    form.fields['dialogue_id'].initial = load_random_string(10)
    return render(request, 'embedding/chat.html', ret)


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


def lab(request):
    ret = get_basic_data(request)
    ret['current_page'] = 'lab'
    ret['enable_home_chat'] = True
    ret['home_chat_form'] = HomeChatForm()
    return render(request, 'embedding/home.html', ret)


def contact(request):
    ret = get_basic_data(request)
    ret['current_page'] = 'contact'
    # if this is a POST request we need to process the form data

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ContactForm(request.POST)
        print(8888888, form)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # name = form.cleaned_data["username"]
            data = Contact(
                username=form.cleaned_data["username"], email=form.cleaned_data["email"], message=form.cleaned_data["message"])
            data.save()
            print(form.cleaned_data, 88888)
            # ...
            # redirect to a new URL:
            return render(request, 'embedding/thanks.html', {})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ContactForm()
    ret['form'] = form
    return render(request, 'embedding/contact.html', ret)


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
                print(881)
                # Redirect to a success page.
                print(form.cleaned_data, 4444, request.GET, request.POST)
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
        print(884)

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


def image_async(request):
    description = request.POST.get('original_text', '')
    style = request.POST.get('style', '')
    count = request.POST.get('count', '3')
    count = int(count)
    if style != '':
        description += '. In ' + style + ' style.'
    openai_response = run_it_image(description, count)
    record_consumption(
        request, sc.MODEL_TYPES_IMAGE, openai_response)
    return HttpResponse(json.dumps({'urls': openai_response['data']}))


def image(request):
    ret = get_basic_data(request)
    ret['form'] = ImageForm()
    return render(request, 'embedding/image.html', ret)


def translation_async(request):
    original_text = request.POST.get('original_text', '')
    target = request.POST.get('target', '')
    openai_response = run_it_translate(original_text, target=target, model='gpt-3.5-turbo')
    translated_text = openai_response['choices'][0]['message']['content']
    record_consumption(
        request, sc.MODEL_TYPES_TRANSLATE, openai_response)
    print(translated_text)
    return HttpResponse(translated_text.strip())


def translation(request):
    ret = get_basic_data(request)
    ret['form'] = TranslationForm()
    return render(request, 'embedding/translation.html', ret)


def grammar_async(request):
    original_text = request.POST.get('original_text', '')
    openai_response = run_it_grammar(original_text, model='gpt-3.5-turbo')
    fixed_text = openai_response["choices"][0]["message"]["content"]
    record_consumption(
        request, sc.MODEL_TYPES_GRAMMAR, openai_response)
    print(fixed_text)
    return HttpResponse(json.dumps({'plain_result': fixed_text.strip(), 'dict': parse_diff(original_text, fixed_text.strip())}))


def grammar(request):
    ret = get_basic_data(request)
    ret['form'] = GrammarForm()
    return render(request, 'embedding/grammar.html', ret)


def summary_async(request):
    original_text = request.POST.get('original_text', '')
    openai_response = run_it_summary(original_text, model='gpt-3.5-turbo')
    summary_text = openai_response["choices"][0]["message"]["content"]
    record_consumption(
        request, sc.MODEL_TYPES_SUMMARY, openai_response)
    print(summary_text)
    return HttpResponse(summary_text.strip())


def summary(request):
    ret = get_basic_data(request)
    ret['form'] = SummaryForm()
    return render(request, 'embedding/summary.html', ret)


@login_required
def collection(request):
    ret = get_basic_data(request)
    ret['current_page'] = 'collection'
    return render(request, 'embedding/collection.html', ret)


def pricing(request):
    ret = get_basic_data(request)
    ret['current_page'] = 'pricing'
    return render(request, 'embedding/pricing.html', ret)


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


def record_dialogue(request, role, message, dialogue_id):
    dialogue = Dialogue.objects.create(role=role, message=message, dialogue_id=dialogue_id)
    dialogue.save()
    

def record_consumption(request, model_type, openai_response, secret=''):
    with transaction.atomic():
        if model_type == sc.MODEL_TYPES_IMAGE:
            token_amount = 0
        else:
            token_amount = openai_response["usage"]["total_tokens"]
        consumption = TokenConsumption.objects.create(user=get_user(request),
                                                      model_type=model_type,
                                                      token_amount=token_amount,
                                                      secret=secret)
        consumption.save()
        if request.user.is_authenticated:
            request.user.left_token -= token_amount
            request.user.used_token += token_amount
            request.user.save()


def get_user(request):
    if request.user.is_authenticated:
        return request.user
    return UserProfile.objects.get(username="default_user")


def generation(request):
    patients = ['lost his job recently, which was not due to his fault.',
                'lost his parents recently,  which loved him so much.',
                'lost his only son recently.',
                'lost his best friend he has known for years recently.',
                'lost his wife recently.',
                'lost his husband recently.',
                'suffers from work pressure from his managers.',
                'suffers from a huge lose in the stock market.',
                'suffers from depression.',
                'suffers from anxiety.',
                'suffers from a divorce which was not her fault.',
                'broke up with her boyfriend.',
                'broke up with his girlfriend.',
                'failed to pass the final exam in college.',
                'has trouble sleeping and has lost weight.',
                'recently went through a divorce and is struggling to adjust to his new life.',
                'has been experiencing high levels of stress at work, which is impacting his mental health and well-being.',
                'feels constantly worried and anxious, and finds it hard to relax or enjoy herself.',
                'feels sad and lonely, and finds it hard to engage in activities he used to enjoy.',
                'has been diagnosed with bipolar disorder and is struggling to manage her symptoms.',
                'has experienced manic episodes and is concerned about the impact on her relationships and work.',
                'has been struggling with addiction to alcohol and is ready to seek help.',
                'has been diagnosed with a chronic illness and is struggling to cope with the physical and emotional impact.',
                'has been experiencing conflict in her marriage and is concerned about the impact on her relationship.',
                'has experienced trauma in his past and is struggling to cope with the emotional impact.',
                'has been struggling with low self-esteem and body image issues.',
                'has been experiencing discrimination and harassment in his workplace due to his sexual orientation.',
                'had a baby and is struggling to adjust to motherhood.',
                'has been struggling with feelings of guilt and shame related to a past mistake where he had a car accident.',
                'recently went through a breakup and is struggling to cope with her emotions.',
                'has been experiencing intense anger and impulsivity, which is impacting his relationships and work.',
                'has been feeling "stuck" in her life and is struggling to find direction and purpose.',
                'has been struggling with a phobia of flying, which is impacting his ability to travel and enjoy life.',
                'has been struggling with disordered eating and is concerned about the impact on her health.',
                'has just moved to another city and feels uncomfortable.',
                'has just started their college and feels uncomfortable.',
                'often quarrels with her parents a lot.',
                'often quarrels with her managers a lot.',
                'often quarrels with her two sons a lot.',
                'is facing discrimination or societal oppression related to their identity',
                'just became a father and feels uncomfortable',
                'just became a mother and feels uncomfortable',
                'is experiencing difficulty managing anger or impulsivity.',
                'has been struggling with low mood and lack of motivation for several months.',
                'has been experiencing panic attacks and feels like he is losing control of his life.',
                'has been diagnosed with an eating disorder and is struggling to manage her symptoms.',
                'has been struggling with addiction to drugs and alcohol and is ready to seek help.',
                'has been experiencing intrusive thoughts and feels like she is losing her mind.',
                'has been struggling with perfectionism and feels like she is never good enough.',
                'has been experiencing symptoms of OCD and is having trouble managing his compulsions.',
                'has been struggling with social anxiety and feels like it is impacting her ability to live a full life.',
                'has been experiencing symptoms of depression and feels like he has lost his sense of purpose in life.',
                'has been struggling with grief and loss after the death of a loved one.',
                'has been struggling with chronic pain and is having trouble managing the emotional impact.',
                'has been experiencing symptoms of ADHD and is having trouble managing his time and staying focused.',
                'has been struggling with infertility and is feeling overwhelmed by her emotions.',
                'has been experiencing symptoms of PTSD after a traumatic event and is struggling to cope with the emotional impact.',
                'has been experiencing symptoms of bipolar disorder and is struggling to manage her moods.',
                'has been struggling with relationship issues and feels like he has stuck in a pattern of toxic relationships.',
                'has been experiencing symptoms of insomnia and is having trouble sleeping.',
                'suffers from PTSD after serving for 3 years in the army in Afghanistan.',
                'suffers from PTSD after being involved in a terrible car accident.',
                'suffers from PTSD after being involved in a terrible air accident.',
                'suffers from PTSD after being involved in a terrible accident in Disneyland.',
                'has been struggling with self-harm and feels like she is losing control of her impulses.',
                'has been experiencing symptoms of postpartum depression and is having trouble bonding with her newborn.',
                'has been struggling with work addiction and feels like he cannot take a break.',
                'has been struggling with trust issues and is having trouble opening up to others.',
                'has been suffering a lot since his girlfriend betrayed him two years ago.',
                'has been struggling with gambling addiction and feels like he is losing control of his finances.',
                'has been struggling with substance abuse for a long time.',
                'has been struggling with social isolation and feels like he is alone in the world.',
                'has been struggling with sexual dysfunction and is feeling anxious about intimacy.',
                'has been struggling with PTSD after serving in the military and is having trouble adjusting to civilian life.',
                'has been struggling with academic pressure and feels like she is constantly under stress.',
                'has been struggling with sexual identity issues and is feeling confused and scared.',
                'has been struggling with family issues and feels like he is caught in the middle of conflicts between his parents.',
                'has been struggling with school-related stress and is having trouble managing her workload.',
                'has been feeling overwhelmed and stressed as a single mother of three children.',
                'has been struggling with substance abuse and is having trouble managing her addiction as a single mother.',
                ]
    therapists = ['is familiar with Psychodynamic Therapy and provides mental support to the patient.',
                  'is familiar with Cognitive therapy and provides mental support to the patient.',
                  'is familiar with Behavior therapy and provides mental support to the patient.',
                  'is familiar with Humanistic therapy and provides mental support to the patient.',
                  'asks questions and listen patitenly to their patients.',
                  'cares about their patients very much.',
                  'always comes up with good ideas to solve the problems of their patients.',
                  'is professional at handling teenage problems.',
                  'guides their patients to find solutions by asking them questions.',
                  'never judges their patients.',
                  'is familiar with Family Therapy and provides mental support to the patient.',
                  'is familiar with Interpersonal Therapy and provides mental support to the patient.',
                  'is able to build a trusting and supportive relationship with their clients, especially with retired people.']
    res = []
    count = 1
    for p in patients:
        for t in therapists:
            messages=[
                {"role": "system", "content": f"Generate a dialogue with more than 550 words between a patient and a therapist. The patient {p}. The therapist {t}"},
            ]
            openai_response = run_it_chat(messages, model='gpt-3.5-turbo')
            ai_message = openai_response["choices"][0]["message"]["content"]
            file_name = f'data/therapy_{count}.txt'
            f = open(file_name, "w")
            f.write(ai_message)
            f.close()
            res.append(str(count) + "########")
            count += 1
    print(len(res))
    return render(request, 'embedding/generation.html', {'res': res})
