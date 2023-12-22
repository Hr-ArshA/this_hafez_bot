import telebot
import logging
import re
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from decouple import config
from fall import show_poem, get_divination
from image import make_image
from flask import Flask, request


# logging info
logging.basicConfig(filename='info.log', filemode='a', level=logging.INFO, format='%(asctime)s - %(filename)s - %(message)s') 

DEBUG = config('DEBUG', default=True, cast=bool)


TOKEN = config('TOKEN')
bot = telebot.TeleBot(token=TOKEN, threaded=False)


if not DEBUG:
    secret = config('SECRET')
    url = f'{config("URL")}/{secret}'


    bot.remove_webhook()
    bot.set_webhook(url=url)

    app = Flask(__name__)

    message_bool = False

    @app.route(f'/{secret}', methods=['POST'])
    def webhook():
        update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
        bot.process_new_updates([update])
        return 'ok', 200


@bot.message_handler(commands=['start'])
def start(msg):
    logging.info(f'{msg.chat.username} - {msg.chat.id}')

    text = """
سلام
برای اینکه فال خود را بگیرید دکمه ی زیر را لمس کنید.
و اگر غزل خاصی مد نظرتان است، شماره ی آن را تایپ کنید

@this_hafez_bot
@PhiloLearn
"""

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("فالم رو بگیر!", callback_data="get_fall"))

    bot.reply_to(msg, text, reply_markup=markup)
    

def get_fallow_markup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("فیلولرن", url="https://PhiloLearn.t.me"))

    return markup


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "get_fall":
        omen = get_divination()
        text_of_divination = show_poem(omen)
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("تصویر فالم رو بده!", callback_data=f"get_pic-{omen}"))

        bot.send_message(call.from_user.id, text_of_divination, reply_markup=markup)


    elif str(call.data).split('-')[0] == "get_pic":
        file_name = str(call.data).split('-')[1]

        poem = make_image(file_name)
        pic = open(poem, 'rb')

        text = '@this_hafez_bot\n@PhiloLearn'

        bot.send_photo(call.from_user.id, pic, caption=text, reply_markup=get_fallow_markup())


@bot.message_handler(content_types=['text'])
def get_poem(msg):
    poem = re.findall(r"\d+", str(msg.text))

    if poem != []:
        poem = int(poem[0])

        if poem in range(1, 496):
            text_of_poem = show_poem(f"sh{poem}")

            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("تصویر بده!", callback_data=f"get_pic-sh{poem}"))

            bot.send_message(msg.chat.id, text_of_poem, reply_markup=markup)
        
        else:
            bot.send_message(msg.chat.id, 'این غزل وجود ندارد!')

    else:
        bot.send_message(msg.chat.id, 'لطفا یک عدد معتبر از ۱ تا ۴۹۵ وارد کنید...')


if DEBUG:
    bot.infinity_polling()