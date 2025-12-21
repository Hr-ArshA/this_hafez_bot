"""
Hafez Divination Telegram Bot
A Telegram bot for accessing Hafez's poetry, including divination (Fal-e Hafez) functionality.
Provides random poems, specific ghazals by number, interpretations, and audio recitations.
"""

import re
import logging
from bot import bot
from keyboards import fal_keyboard, philolearn_button
from utils.text import to_persian_digits, get_caption
from utils.time import is_yalda
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.formatting import format_text, hcite
from handlers import register_handlers
from services.fall import generate_fall
from services.poems import get_poem

# Configure logging to file
logging.basicConfig(
    filename='info.log', 
    filemode='a', 
    level=logging.INFO, 
    format='%(asctime)s - %(filename)s - %(message)s'
) 

register_handlers(bot)


@bot.message_handler(commands=['start', 'help'])
def start(message):
    """
    Handle the /start and /help commands.

    Sends a welcome message with usage instructions and
    interactive buttons depending on the current season (Yalda or normal).

    Args:
        message (telebot.types.Message): Incoming Telegram message.
    """
    logging.info(
        f"user={message.from_user.id} "
        f"username={message.from_user.username} "
        f"text={message.text}"
    )
    # Create inline keyboard
    markup = InlineKeyboardMarkup(row_width=1)

    if is_yalda():
        with open('text/yalda', 'r') as text:
            markup.add(
                InlineKeyboardButton("🍉 فالِ یلدایی من! 🍉", callback_data="get_fall"),
                philolearn_button()
            )

            bot.send_message(message.chat.id, text.read().encode('utf-8'), reply_markup=markup, parse_mode="MarkDown")
    
    else:
        with open('text/defaul', 'r') as text:
            markup.add(
                InlineKeyboardButton("فالم رو بگیر!", callback_data="get_fall"),
                philolearn_button()
            )
            
            bot.send_message(message.chat.id, text.read().encode('utf-8'), reply_markup=markup, parse_mode="MarkDown")


@bot.message_handler(commands=['fall'])
def handle_fall_command(message):
    """
    Handle /fall command.
    """
    result = generate_fall()

    if not result:
        bot.send_message(message.chat.id, "خطا در دریافت فال")
        return

    bot.send_message(
        message.chat.id,
        result["text"],
        parse_mode="HTML",
        reply_markup=fal_keyboard(result["omen"], True)
    )

    
@bot.message_handler(content_types=['text'])
def send_this_poem(message):
    """
    Handle text messages containing ghazal numbers.

    If a valid number is detected, the corresponding ghazal
    is retrieved from the database and sent to the user.

    Args:
        message (telebot.types.Message): Incoming Telegram message.
    """
    caption = get_caption()

    # Extract number from message text
    poem_num = re.search(r"\d+", message.text)
    if not poem_num:
        bot.send_message(message.chat.id, 'این غزل وجود ندارد!')
    
    else:
        poem_num = int(poem_num.group())

        # Check if poem number is in valid range
        if poem_num in range(1, 496):
            name_of_poem = f"sh{str(poem_num).zfill(3)}"
            text_of_poem = get_poem(name_of_poem)

            # Format poem display
            text = format_text(
                f'<b>- غزل {to_persian_digits(str(poem_num))}</b>\n',
                hcite(str(text_of_poem[1]).replace('\n', '\n\n')),
                caption,
            )

            bot.send_message(message.chat.id, text, reply_markup=fal_keyboard(poem_num, False), parse_mode="HTML")
    
        else:
            bot.send_message(message.chat.id, 'لطفا یک عدد معتبر از ۱ تا ۴۹۵ وارد کنید...')



# Start the bot with infinite polling
bot.infinity_polling()
