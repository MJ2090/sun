import random
import string
import difflib
from django.db import transaction
from embedding.models import TokenConsumption, UserProfile
import embedding.static_values as sc


def load_random_string(num, seed=None):
    randStr = ''
    if not seed:
        seed = string.ascii_letters + string.digits
    for _ in range(num):
        randStr += seed[random.randrange(1, len(seed))]
    return randStr


def get_basic_data(request, params={}):
    ret = {}
    if request.user.is_authenticated:
        ret['user'] = request.user
    if params.get('hide_nav'):
        ret['hide_nav'] = True
    ret['current_page'] = 'home'
    return ret


def enable_new_home(request):
    return True


def parse_diff(text1, text2):
    seqm= difflib.SequenceMatcher(None, text1, text2)
    output= []
    for opcode, a0, a1, b0, b1 in seqm.get_opcodes():
        if opcode == 'equal':
            output.append({'original': seqm.a[a0:a1]})
        elif opcode == 'insert':
            output.append({'insert': seqm.b[b0:b1]})
        elif opcode == 'delete':
            output.append({'delete': seqm.a[a0:a1]})
        elif opcode == 'replace':
            output.append({'replace': seqm.a[b0:b1]})
        else:
            raise RuntimeError("unexpected opcode")
    return output


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