import random
import string

_gen_random_string_options_ = string.ascii_uppercase + string.ascii_lowercase + string.digits


def gen_random(length=20):
    return ''.join(random.choices(_gen_random_string_options_, k=length))


def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)
