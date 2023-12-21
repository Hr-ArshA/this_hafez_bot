import telebot
import logging
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from decouple import config
from fall import show_fall
from image import FallHafez


# logging info
logging.basicConfig(filename='info.log', filemode='a', level=logging.INFO, format='%(asctime)s - %(filename)s - %(message)s') 

TOKEN = config('TOKEN')
bot = telebot.TeleBot(token=TOKEN)

bot.delete_webhook()

@bot.message_handler(commands=['start'])
def start(msg):
    logging.info(f'{msg.chat.username} - {msg.chat.id}')

    text = """
سلام
برای اینکه فال خود را بگیرید دکمه ی زیر را لمس کنید.

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
        fall = show_fall()
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("تصویر فالم رو بده!", callback_data=f"get_pic-{fall[1]}"))

        bot.send_message(call.from_user.id, fall[0], reply_markup=markup)


    elif str(call.data).split('-')[0] == "get_pic":
        fall = str(call.data).split('-')[1]
        text = """
فونت مورد نظر خودتان را انتخاب کنید:
        
@this_hafez_bot
@PhiloLearn
"""
        markup = InlineKeyboardMarkup()
        markup.row_width = 2

        tanha = InlineKeyboardButton("تنها", callback_data=f"tanha-{fall}")
        parastoo = InlineKeyboardButton("پرستو", callback_data=f"parastoo-{fall}")
        shabnam = InlineKeyboardButton("شبنم", callback_data=f"shabnam-{fall}")
        vazirmatn = InlineKeyboardButton("وزیر", callback_data=f"vazirmatn-{fall}")
        
        markup.add(parastoo, tanha)
        markup.add(vazirmatn, shabnam)

        example = open('fonts.jpg', 'rb')
        bot.send_photo(call.from_user.id, example, caption=text, reply_markup=markup)


    elif str(call.data).split('-')[0] == "tanha":
        fall = str(call.data).split('-')[1]

        tanha = FallHafez('Tanha').make_image(fall)
        pic = open(tanha, 'rb')

        text = '@this_hafez_bot\n@PhiloLearn'

        bot.send_photo(call.from_user.id, pic, caption=text, reply_markup=get_fallow_markup())


    elif str(call.data).split('-')[0] == "parastoo":
        fall = str(call.data).split('-')[1]

        parastoo = FallHafez('Parastoo').make_image(fall)
        pic = open(parastoo, 'rb')

        text = '@this_hafez_bot\n@PhiloLearn'

        bot.send_photo(call.from_user.id, pic, caption=text, reply_markup=get_fallow_markup())


    elif str(call.data).split('-')[0] == "shabnam":
        fall = str(call.data).split('-')[1]

        shabnam = FallHafez('Shabnam').make_image(fall)
        pic = open(shabnam, 'rb')

        text = '@this_hafez_bot\n@PhiloLearn'

        bot.send_photo(call.from_user.id, pic, caption=text, reply_markup=get_fallow_markup())


    elif str(call.data).split('-')[0] == "vazirmatn":
        fall = str(call.data).split('-')[1]

        vazirmatn = FallHafez('Vazirmatn').make_image(fall)
        pic = open(vazirmatn, 'rb')

        text = '@this_hafez_bot\n@PhiloLearn'

        bot.send_photo(call.from_user.id, pic, caption=text, reply_markup=get_fallow_markup())


bot.infinity_polling()