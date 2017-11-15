import random
import pickle
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

WORD_SITE = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"


class WordGenerator:
    def __init__(self):
        try:
            with open("words.pickle", mode='rb') as file:
                self.words = pickle.load(file)
        except FileNotFoundError:
            import requests
            response = requests.get(WORD_SITE)
            self.words = response.content.splitlines()
            with open("words.pickle", mode='wb') as file:
                pickle.dump(self.words, file)

    def getRandomWord(self):
        return str(random.choice(self.words))[2:-1]


def create_new_test_image(path):
    width = 1920
    height = 1200
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("Inconsolata-g.ttf", 16)

    wordgen = WordGenerator()
    msg = wordgen.getRandomWord()
    w, h = draw.textsize(msg)
    draw.text(
        ((width - w) // 2, (height - h) // 2), msg, (255, 255, 255), font=font)
    img.save(path)
    return img
