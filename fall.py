import os
from random import choice
import arabic_reshaper


def get_fall():
    return choice(os.listdir('hafez'))


def get_title(text):
        text = text[2:]
        english_numbers = "0123456789"
        persian_numbers = "۰۱۲۳۴۵۶۷۸۹"
        translation_table = str.maketrans(english_numbers, persian_numbers)
        return arabic_reshaper.reshape(f"غزل {text.translate(translation_table)}")


def show_fall():
    fall = get_fall()
    text = open(f"hafez/{fall}", 'r').read()

    text = f"""
{get_title(fall)}

{text}

@this_hafez_bot
"""

    return text, fall