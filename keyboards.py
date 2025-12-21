from utils.time import is_yalda
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

PHILOLEARN_URL = "https://PhiloLearn.t.me"

def philolearn_button():
    text = "فیلولرن 🍉" if is_yalda() else "فیلولرن"
    return InlineKeyboardButton(text, url=PHILOLEARN_URL)


def fal_keyboard(omen: int, is_omen:bool=True):
    if is_omen:
        poem_type = 'فالم'
    else:
        poem_type = 'غزل'
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton(
            f"تفسیر {poem_type}... (تفسیر هوش مصنوعی)",
            callback_data=f"get_tabir-{omen}"
        )
    )
    kb.add(
        InlineKeyboardButton(
            f"تصویر {poem_type} رو بده!",
            callback_data=f"get_pic-{omen}"
        ),
        InlineKeyboardButton(
            f"استوری {poem_type} رو بده!",
            callback_data=f"get_story-{omen}"
        )
    )
    kb.add(
        InlineKeyboardButton(
            "خوانش این غزل...",
            callback_data=f"get_audio-{omen}"
        )
    )
    kb.add(
        philolearn_button()
    )
    return kb



def philolearn_keyboard() -> InlineKeyboardMarkup:
    """
    Create an inline keyboard containing the Philolearn button.

    The button text changes automatically during Yalda nights.

    Returns:
        InlineKeyboardMarkup: Keyboard with a single Philolearn button.
    """
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        philolearn_button()
    )
    return markup