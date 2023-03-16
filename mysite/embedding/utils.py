import random
import string


def load_random_string(num, seed=None):
    randStr = ''
    if not seed:
        seed = string.ascii_letters + string.digits
    for _ in range(num):
        randStr += seed[random.randrange(1, len(seed))]
    return randStr


def get_basic_data(request):
    ret = {}
    if request.user.is_authenticated:
        ret['user'] = request.user
        if request.user.username == 'z':
            ret['use_new_header'] = True
    ret['current_page'] = 'home'
    return ret


def enable_new_home(request):
    return request.user.is_authenticated and request.user.username == 'z'
