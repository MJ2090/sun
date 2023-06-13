from django.http import HttpResponse
from embedding.openai.features import feature_chat
from embedding.models import TherapyAssessment, DepressionAssessment, SuicideAssessment, VisitorDialogue, VisitorProfile
from django.shortcuts import render
from embedding.utils import get_time, load_random_greeting, load_random_string, get_basic_data
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

    prompt = get_prompt(visitor)
    messages = [{"role": "system", "content": prompt}]
    messages.extend(history_json)
    messages.append({"role": "user", "content": new_message})

    openai_response, _ = feature_chat(messages, model=model)
    ai_message = openai_response["choices"][0]["message"]["content"]
    ret['ai_message'] = ai_message
    dialogue = record_new_dialogue(visitor, ai_message, d_uuid, role="ai")
    ret['m_uuid'] = dialogue.msg_uuid
    ret['messages'] = messages

    thread_start(visitor, new_message, history_json, d_uuid)
    load_side_channel(visitor, ret)
    return HttpResponse(json.dumps(ret))


def olivia_async_init(request):
    if request.POST.get("t_uuid", '') != '':
        visitor = create_exist_visitor(request)
        greeting = load_random_greeting(visitor.username, first_meet=False)
    else:
        visitor = create_new_visitor(request)
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
    t_age_range = request.POST.get('t_age_range', '')
    t_gender = request.POST.get('t_gender', '')
    t_pin = request.POST.get('t_pin', '')
    uuid = load_random_string(10)
    r = VisitorProfile.objects.create(
        uuid=uuid, username=t_name, age_range=t_age_range, gender=t_gender, pin=t_pin)
    return r


def get_prompt(visitor):
    prompts = []
    prompts.append(get_base_prompt())
    prompts.append(get_stateful_prompt())
    prompts.append(get_user_prompt(visitor))
    prompts.append(get_assessment_prompt(visitor))
    return '\n'.join(prompts)


def get_assessment_prompt(visitor):
    assessments = TherapyAssessment.objects.filter(
        visitor=visitor).order_by("-timestamp")
    if len(assessments) == 0:
        return ''
    if assessments[0].result == 'None':
        return ''
    therapy_prompt = f"""
    Be aware that the visitor may suffer from {assessments[0].result}
    """
    return therapy_prompt


def get_stateful_prompt():
    stateful_prompt = f"""
    ## DO NOT privode any suggestions unless the visitor explicitly asks for that.
    ## BE CURIOUS about the visitor, ask questions based on their talk and experience. 
    """
    return stateful_prompt


def get_user_prompt(visitor):
    user_prompt = f"""
    The visitor's name is {visitor.username}, their gender is {visitor.gender}, and their age is {visitor.age_range}.
    """
    return user_prompt


def get_base_prompt():
    base_prompt = """
    You act as a professional therapist. You MUST respect these rules:
    ### Focus on Therapy, Do not answer irrelevant questions like mathematical or political ones. 
    ### If asked who you are, you are an AI powered therapist, never mention GPT or OpenAI.
    """
    return base_prompt


def add_user_prompt(visitor, prompt):
    user_prompt = f"""
    The visitor's name is {visitor.username}, their gender is {visitor.gender}, and their age is {visitor.age_range}."""
    return prompt + user_prompt


def get_visitor_from_dialogue(d_uuid):
    exist = VisitorDialogue.objects.filter(dialogue_uuid=d_uuid)[0]
    return exist.visitor


def thread_start(visitor, new_message, history_json, d_uuid):
    thread = Thread(target=thread_overall, args=(
        visitor, new_message, history_json, d_uuid))
    thread.start()


def thread_overall(visitor, new_message, history_json, d_uuid):
    thread_assessment_overall(visitor, new_message, history_json, d_uuid)


def thread_assessment_overall(visitor, new_message, history_json, d_uuid):
    current_t = get_time()
    if len(history_json) < 5:
        return
    if TherapyAssessment.objects.filter(visitor=visitor, timestamp__gte=(current_t-3600)).count() > 0:
        return
    dialogue_str = get_dialogue_str(d_uuid)
    prompt = f"""
    Based on the given Dialogue between a visitor and a therapist, tell whether it is possible that the visitor is suffering from mental health issues. 
    You MUST return ONE of the options only, no other words at all. If there is not eough information, return the option 'None'.
     
    The options are:

    'Depression',
    'Anxiety',
    'ADHD',
    'Insomnia',
    'Intermittent Explosive Disorder',
    'None'
    
    Dialogue:

    {dialogue_str}
    """
    model = "gpt-4"
    messages = [{"role": "system", "content": prompt}]
    openai_response, _ = feature_chat(messages, model=model)
    ai_message = openai_response["choices"][0]["message"]["content"]
    TherapyAssessment.objects.create(
        visitor=visitor, result=ai_message, timestamp=get_time())
    

def thread_check_suicide(visitor, new_message, history_json, d_uuid):
    current_t = get_time()
    print("current_t", current_t)
    if len(history_json) < 5:
        return
    if SuicideAssessment.objects.filter(visitor=visitor, timestamp__gte=(current_t-3600)).count() > 0:
        return
    dialogue_str = get_dialogue_str(d_uuid)
    prompt = f"""
    Based on the given Dialogue between a visitor and a therapist, tell whether the visitor has a tendency to commit suicide. 
    You MUST return ONE of the options only, no other words at all, the options are:, 'Severe suicidal', 'Moderate suicidal', 'Slight suicidal', 'None'.
    
    Dialogue:

    {dialogue_str}
    """
    model = "gpt-4"
    messages = [{"role": "system", "content": prompt}]
    openai_response, _ = feature_chat(messages, model=model)
    ai_message = openai_response["choices"][0]["message"]["content"]
    SuicideAssessment.objects.create(
        visitor=visitor, result=ai_message, timestamp=get_time())


def thread_check_diagnosis(visitor, new_message):
    pass


def get_base_ret(request):
    return {}


def load_side_channel(visitor, ret):
    side_channel = {}
    assessments = TherapyAssessment.objects.filter(
        visitor=visitor).order_by("-timestamp")
    if len(assessments) > 0 and assessments[0].result != 'None':
        side_channel['therapy_assessment'] = True
        side_channel['therapy_assessment_label'] = assessments[0].result

        if assessments[0].result == 'Depression':
            side_channel['action'] = 'PHQ-9'

    ret['side_channel'] = side_channel


def get_dialogue_str(d_uuid):
    records = VisitorDialogue.objects.filter(
        dialogue_uuid=d_uuid, ack=True).order_by("timestamp")
    dialogue = []
    for item in records:
        if item.role == 'hm':
            dialogue.append('Visitor: ' + item.message)
        else:
            dialogue.append('Therapist: ' + item.message)

    return '\n'.join(dialogue)
