import os
from random import choice
import arabic_reshaper


def get_divination():
    return choice(os.listdir('hafez'))


def get_en_num(text):
    text = text[2:]
    english_numbers = "0123456789"
    persian_numbers = "۰۱۲۳۴۵۶۷۸۹"
    translation_table = str.maketrans(english_numbers, persian_numbers)
    return text.translate(translation_table)


def show_poem(divination):
    text = open(f"hafez/{divination}", 'r').read()

    text = f"""
غزل {get_en_num(divination)}

{text}

@this_hafez_bot
"""

    return text
