from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper


class FallHafez():
    BLACK = (0, 0, 0)

    def __init__(self, font:str) -> None:
        self.font = ImageFont.truetype(f'src/font/{font}.ttf', 80)
        self.title = ImageFont.truetype(f'src/font/{font}.ttf', 100)


    def get_text_size(self, text, font):
        return font.getbbox(arabic_reshaper.reshape(text))[2]
    

    def get_title(self, text):
        text = text[2:]
        english_numbers = "0123456789"
        persian_numbers = "۰۱۲۳۴۵۶۷۸۹"
        translation_table = str.maketrans(english_numbers, persian_numbers)
        return arabic_reshaper.reshape(f"غزل {text.translate(translation_table)}")


    def make_image(self, file):
        self.text = str(open(f'hafez/{file}', 'r').read()).split('\n')[:4]
        image = Image.open('src/images/bg.jpg')
        _, _, length, width = image.getbbox()

        TEXT = ImageDraw.Draw(image)

        title_text = self.get_title(file)

        half_width, half_length = int(width/2), int(length/2)

        # title
        TEXT.text((half_length - int(self.get_text_size(title_text, self.title)/2), int(width/3)-100), title_text, self.BLACK, font=self.title)


        TEXT.text((half_length + 50, half_width-220), arabic_reshaper.reshape(self.text[0]), self.BLACK, font=self.font)

        TEXT.text((half_length - self.get_text_size(self.text[1], self.font) - 50, half_width-70), arabic_reshaper.reshape(self.text[1]), self.BLACK, font=self.font)


        TEXT.text((half_length + 50, half_width+80), arabic_reshaper.reshape(self.text[2]), self.BLACK, font=self.font)

        TEXT.text((half_length - self.get_text_size(self.text[3], self.font) - 50, half_width+230), arabic_reshaper.reshape(self.text[3]), self.BLACK, font=self.font)


        image.save('image.jpg', quality=80)
        return 'image.jpg'
    