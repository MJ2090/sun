import random
import string
import difflib


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