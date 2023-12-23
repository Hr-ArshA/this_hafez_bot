import telebot
import logging
import re
import csv
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


files = dict()

with open('list.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            pass
        files[row["file"]] = row["id"]


@bot.message_handler(commands=['start', 'help'])
def start(msg):
    logging.info(f'{msg.chat.username} - {msg.chat.id}')

    text = """
سلام
ربات دیوان حافظ هستم و در تلاشم که بهتر و زیباتر به شما کمک کنم تا با حافظ ارتباط داشته باشید.

اگر غزل خاصی مد نظرتونه، عدد غزل رو با اعداد انگلیسی نوشته و ارسال کنید. مثال: 

495

اگر هم میخواهید که فال بگیرید میتونید روی دکمه ی «فالم رو بگیر!» لمس کنید یا دستور /fall رو ارسال کنید.

در هر مرحله میتونید با زدن دکمه ی  «خوانش این غزل...» به یک خوانش نمونه از اون غزل مورد نظر دسترسی داشته باشد.

پشتیبانی:
@Hr_ArshA

@this_hafez_bot
@PhiloLearn
"""

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("فالم رو بگیر!", callback_data="get_fall"),
        InlineKeyboardButton("فیلولرن", url="https://PhiloLearn.t.me"),
    )

    bot.reply_to(msg, text, reply_markup=markup)


def fall(user_id):
    omen = get_divination()
    text_of_divination = show_poem(omen)
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("تصویر فالم رو بده!", callback_data=f"get_pic-{omen}"),
        InlineKeyboardButton("خوانش این غزل...", callback_data=f"get_audio-{omen}"),
        InlineKeyboardButton("فیلولرن", url="https://PhiloLearn.t.me"),

    )

    bot.send_message(user_id, text_of_divination, parse_mode="markdown", reply_markup=markup)


@bot.message_handler(commands=['fall'])
def get_fall(msg):
    fall(msg.chat.id)


def get_fallow_markup(poem=None):
    markup = InlineKeyboardMarkup(row_width=1)
    

    if poem == None:
        markup.add(InlineKeyboardButton("فیلولرن", url="https://PhiloLearn.t.me"))

    else:
        markup.add(
            InlineKeyboardButton("تصویر بده!", callback_data=f"get_pic-{poem}"),
            InlineKeyboardButton("فیلولرن", url="https://PhiloLearn.t.me"),
        )


    return markup


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "get_fall":
        fall(call.from_user.id)

    elif str(call.data).split('-')[0] == "get_pic":
        file_name = str(call.data).split('-')[1]

        poem = make_image(file_name)
        pic = open(poem, 'rb')

        text = '@this_hafez_bot\n@PhiloLearn'
        bot.send_photo(call.from_user.id, pic, caption=text, reply_markup=get_fallow_markup())


    elif str(call.data).split('-')[0] == "get_audio":
        file_name = str(call.data).split('-')[1]

        bot.copy_message(call.from_user.id, config('STORAGE'), int(files[file_name]), reply_markup=get_fallow_markup())

        

@bot.message_handler(content_types=['text'])
def get_poem(msg):
    poem = re.findall(r"\d+", str(msg.text))

    if poem != []:
        poem = int(poem[0])

        if poem in range(1, 496):
            text_of_poem = show_poem(f"sh{poem}")

            markup = InlineKeyboardMarkup(row_width=2)
            markup.add(
                InlineKeyboardButton("تصویر بده!", callback_data=f"get_pic-sh{poem}"),
                InlineKeyboardButton("خوانش این غزل...", callback_data=f"get_audio-sh{poem}"),
                InlineKeyboardButton("فیلولرن", url="https://PhiloLearn.t.me"),

            )

            bot.send_message(msg.chat.id, text_of_poem, reply_markup=markup)
        
        else:
            bot.send_message(msg.chat.id, 'این غزل وجود ندارد!')

    else:
        bot.send_message(msg.chat.id, 'لطفا یک عدد معتبر از ۱ تا ۴۹۵ وارد کنید...')


if DEBUG:
    bot.infinity_polling()