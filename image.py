from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper


class FallHafez():
    BLACK = (0, 0, 0)

    def __init__(self, font:str) -> None:
        self.font = ImageFont.truetype(f'src/font/{font}.ttf', 50)
        self.title = ImageFont.truetype(f'src/font/{font}.ttf', 80)


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

        TEXT.text((int(length/2) - int(self.get_text_size(title_text, self.title)/2), 200), title_text, self.BLACK, font=self.title)

        TEXT.text((((length/2)), int(width/2)-200), arabic_reshaper.reshape(self.text[0]), self.BLACK, font=self.font)
        TEXT.text((int((length/2) - self.get_text_size(self.text[1], self.font)), int(width/2)-100), arabic_reshaper.reshape(self.text[1]), self.BLACK, font=self.font)

        TEXT.text((((length/2)), int(width/2)+50), arabic_reshaper.reshape(self.text[2]), self.BLACK, font=self.font)
        TEXT.text((int((length/2) - self.get_text_size(self.text[3], self.font)), int(width/2)+150), arabic_reshaper.reshape(self.text[3]), self.BLACK, font=self.font)

        image.save('image.jpg')

        return 'image.jpg'
    

FallHafez('Vazirmatn').make_image('sh286')