import re
from datetime import datetime


def clean(html):
    b = re.sub(re.compile('<.*?>'), '', html).strip()
    return b


def extract_words(text):
    not_letters_or_digits = '.,()[]{}<>!?:;@#$%^&*+=`~/\\'
    return text.translate(None, not_letters_or_digits)


def log(msg):
    print "[" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "]", msg
