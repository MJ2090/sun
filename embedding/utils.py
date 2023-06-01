import random
import string
import difflib
import os
from django.db import transaction
from embedding.models import TokenConsumption, UserProfile, EmbeddingModel
import embedding.static_values as sc
from django.conf import settings as conf_settings
from django.core.files.storage import default_storage
from PIL import Image


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


def save_to_local(original_file, sub_dir=''):
    random_prefix = load_random_string(15) + "_"
    file_dir = conf_settings.UPLOADS_PATH + sub_dir
    if not os.path.isdir(file_dir):
        print("mkdir in save_to_local.. ", file_dir)
        os.makedirs(file_dir)
    file_name = default_storage.save(os.path.join(
        file_dir, random_prefix+original_file.name), original_file)
    if sub_dir == '' and original_file.size > 3*1000*1000:
        tmp = Image.open(file_name)
        max_size = (1024, 1024)
        tmp.thumbnail(max_size, Image.ANTIALIAS)
        tmp.save(file_name, optimize=True, quality=85)
        print("size recuded: ", original_file.size,
              ' to ', os.path.getsize(file_name), tmp.size)
    return file_name


def load_embedding_models(request, ret):
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