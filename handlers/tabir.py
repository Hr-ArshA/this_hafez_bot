from services.poems import get_poem
from keyboards import philolearn_keyboard
from utils.text import to_persian_digits
from utils.time import is_yalda

def handle_tabir(bot, call):
    omen = call.data.split("-")[1]
    poem_id = f"sh{omen.zfill(3)}"

    poem = get_poem(poem_id)
    if not poem:
        bot.answer_callback_query(call.id, "غزل پیدا نشد")
        return

    text = (
        f"* - غزل {to_persian_digits(omen)} *\n"
        f"{poem[2].replace('---', '').replace('#', '')}"
        '\n🍉🍉 @this\\_hafez\\_bot 🍉🍉' if is_yalda() else '\n@this\\_hafez\\_bot'
    )

    bot.send_message(
        call.from_user.id,
        text,
        parse_mode="Markdown",
        reply_markup=philolearn_keyboard()
    )

