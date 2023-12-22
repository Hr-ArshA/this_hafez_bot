from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from fall import get_en_num


def get_text_size(text, font):
    return font.getbbox(arabic_reshaper.reshape(text))[2]


def make_image(file):
    BLACK = (0, 0, 0)
    font = ImageFont.truetype(f'src/font/Tanha.ttf', 80)
    title = ImageFont.truetype(f'src/font/Tanha.ttf', 100)

    text = str(open(f'hafez/{file}', 'r').read()).split('\n')[:4]

    image = Image.open('src/images/bg.jpg')
    TEXT = ImageDraw.Draw(image)
    
    _, _, length, width = image.getbbox()
    half_width, half_length = int(width/2), int(length/2)

    title_text = arabic_reshaper.reshape(f"غزل {get_en_num(file)}")

    # title
    TEXT.text((half_length - int(get_text_size(title_text, title)/2), int(width/3)-100), title_text, BLACK, font=title)

    # The first bit
    TEXT.text((half_length + 50, half_width-220), arabic_reshaper.reshape(text[0]), BLACK, font=font)
    TEXT.text((half_length - get_text_size(text[1], font) - 50, half_width-70), arabic_reshaper.reshape(text[1]), BLACK, font=font)

    # The second bit
    TEXT.text((half_length + 50, half_width+80), arabic_reshaper.reshape(text[2]), BLACK, font=font)
    TEXT.text((half_length - get_text_size(text[3], font) - 50, half_width+230), arabic_reshaper.reshape(text[3]), BLACK, font=font)


    image.save('image.jpg', quality=80)
    return 'image.jpg'


make_image('sh286')