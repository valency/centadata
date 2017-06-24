import re
from datetime import datetime

from termcolor import colored


def clean(html):
    b = re.sub(re.compile('<.*?>'), '', html)
    b = b.replace('&nbsp;', ' ').strip()
    return b


def extract_words(text):
    not_letters_or_digits = '.,()[]{}<>!?:;@#$%^&*+=`~/\\'
    return text.translate(None, not_letters_or_digits)


def log(msg, color=None):
    print(colored('[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ']', 'green'), colored(msg, color))
