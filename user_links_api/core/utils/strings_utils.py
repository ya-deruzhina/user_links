import re


def normalize_string(value):
    if type(value) != str:
        return ''
    return re.sub(' +', ' ', value).lower().strip()
