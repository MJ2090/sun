from django.http import HttpResponse
from embedding.openai.features import feature_chat
from embedding.models import DepressionAssessment, SuicideAssessment, VisitorDialogue, VisitorProfile
from django.shortcuts import render
from embedding.utils import get_time, get_int, load_random_greeting, load_random_string, get_basic_data
import json
from threading import Thread


def olivia_async_chat(request):
    ret = get_base_ret(request)
    model = 'gpt-4'
    new_message = request.POST.get('message')
    history_json = json.loads(request.POST.get('history', ''))
    d_uuid = request.POST.get('d_uuid', '')
    visitor = get_visitor_from_dialogue(d_uuid=d_uuid)
    record_new_dialogue(visitor, new_message, d_uuid=d_uuid, role="hm")

    prompt = get_prompt(name=visitor.username)
    messages = [{"role": "system", "content": prompt}]
    messages.extend(history_json)
    messages.append({"role": "user", "content": new_message})

    openai_response, _ = feature_chat(messages, model=model)
    ai_message = openai_response["choices"][0]["message"]["content"]
    ret['ai_message'] = ai_message
    dialogue = record_new_dialogue(visitor, ai_message, d_uuid, role="ai")
    ret['m_uuid'] = dialogue.msg_uuid

    thread_start(visitor, new_message, history_json, d_uuid)
    load_side_channel(visitor, ret)
    return HttpResponse(json.dumps(ret))


def olivia_async_init(request):
    if request.POST.get("t_uuid", '') != '':
        print("333333333")
        visitor = create_exist_visitor(request)
    else:
        visitor = create_new_visitor(request)
        print("444444444")
    greeting = load_random_greeting(visitor.username)
    dialogue = record_new_dialogue(visitor, greeting, None, "ai")
    return HttpResponse(json.dumps({'ai_message': greeting, 'uuid': visitor.uuid, 'd_uuid': dialogue.dialogue_uuid, 'm_uuid': dialogue.msg_uuid}))


def olivia_async_ack(request):
    m_uuid = request.POST.get('m_uuid')
    dialogues = VisitorDialogue.objects.filter(msg_uuid=m_uuid)
    if len(dialogues) != 1:
        print(f"olivia_async_ack: {m_uuid} does not exist")
        return HttpResponse(json.dumps({'ai_message': 'failed'}))
    
    dialogues[0].ack = True
    dialogues[0].save()
    return HttpResponse(json.dumps({'ai_message': 'acked'}))


def olivia_entrance(request):
    ret = get_basic_data(request, {'hide_nav': True})
    return render(request, 'embedding/olivia_entrance.html', ret)


def record_new_dialogue(visitor, message, d_uuid=None, role="ai"):
    if not d_uuid:
        d_uuid = load_random_string(10)
    m_uuid = load_random_string(10)
    ack = role == "hm"
    r = VisitorDialogue.objects.create(
        visitor=visitor, message=message, role=role, msg_uuid=m_uuid, dialogue_uuid=d_uuid, timestamp=get_time(), ack=ack)
    return r


def create_exist_visitor(request):
    uuid = request.POST.get("t_uuid", '')
    r = VisitorProfile.objects.get(uuid=uuid)
    print("existing user found..")
    return r


def create_new_visitor(request):
    t_name = request.POST.get('t_name', '')
    t_age = get_int(request.POST.get('t_age', ''))
    t_gender = request.POST.get('t_gender', '')
    t_pin = request.POST.get('t_pin', '')
    uuid = load_random_string(10)
    r = VisitorProfile.objects.create(
        uuid=uuid, username=t_name, age=t_age, gender=t_gender, pin=t_pin)
    return r


def get_prompt(name):
    base_prompt = """
    You act as a professional therapist who uses Cognitive Behavioral Therapy to treat patients. You must respect these rules: 
    #1. If visitors want to commit suicide or hurt someone, immediately lead them to hotline 988 or 911. 
    #2. Do not answer questions irrelevant to therapy, for example mathematical or political questions. 
    #3. If asked who you are, you are an AI powered therapist, never mention GPT or OpenAI.
    """
    user_prompt = f"""
    The visitor's name is {name}, and she is 23 years old."""
    return base_prompt + user_prompt


def get_visitor_from_dialogue(d_uuid):
    exist = VisitorDialogue.objects.filter(dialogue_uuid=d_uuid)[0]
    return exist.visitor


def thread_start(visitor, new_message, history_json, d_uuid):
    thread = Thread(target = thread_overall, args = (visitor, new_message, history_json, d_uuid))
    thread.start()


def thread_overall(visitor, new_message, history_json, d_uuid):
    thread_check_suicide(visitor, new_message, history_json, d_uuid)


def thread_check_suicide(visitor, new_message, history_json, d_uuid):
    current_t = get_time()
    print("current_t", current_t)
    if len(history_json)<10:
        return
    if SuicideAssessment.objects.filter(visitor=visitor, timestamp__gte=(current_t-3600)).count() > 0:
        return
    dialogue_str = get_dialogue_str(d_uuid)
    prompt = f"""
    Based on the given dialogue between a visitor and a therapist, tell whether the visitor has a strong tendency to commit suicide. You MUST return ONE letter only, Y or N, no other words.
    Dialogue:

    {dialogue_str}
    """
    model = "gpt-4"
    messages = [{"role": "system", "content": prompt}]
    openai_response, _ = feature_chat(messages, model=model)
    ai_message = openai_response["choices"][0]["message"]["content"]
    SuicideAssessment.objects.create(visitor=visitor, result=ai_message, timestamp=get_time())
    # if "suicide" in new_message:
    #     SuicideAssessment.objects.create(visitor=visitor, result='Y', timestamp=get_time())


def thread_check_diagnosis(visitor, new_message):
    pass


def get_base_ret(request):
    return {}


def load_side_channel(visitor, ret):
    side_channel = {}
    assessments = SuicideAssessment.objects.filter(visitor=visitor).order_by("timestamp")
    if len(assessments)>0 and assessments[0].result== 'Y':
        side_channel['suicide'] = True
    assessments = DepressionAssessment.objects.filter(visitor=visitor).order_by("timestamp")
    if len(assessments)>0 and assessments[0].result== 'Y':
        side_channel['suicide'] = True
    ret['side_channel'] = side_channel


def get_dialogue_str(d_uuid):
    records = VisitorDialogue.objects.filter(dialogue_uuid=d_uuid, ack=True).order_by("timestamp")
    dialogue = []
    for item in records:
        if item.role == 'hm':
            dialogue.append('Visitor: ' + item.message)
        else:
            dialogue.append('Therapist: ' + item.message)

    return '\n'.join(dialogue)
