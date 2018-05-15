import os
from PIL import Image, ImageDraw


class Visible:
    def __init__(self, image, message):
        self.image = image
        self.message = message

    def watermark(self):
        print("working dir" + os.getcwd())
        # os.chdir('/home/abhishek/PycharmProjects/watermarking/media/')
        print("working dir" + os.getcwd())
        filename = 'C:/Users/saumy/PycharmProjects/Dwt watermark/src/media/' + self.image.name
        main = Image.open(filename)
        watermark = Image.new("RGBA", main.size)
        waterdraw = ImageDraw.ImageDraw(watermark, "RGBA")
        waterdraw.text((10, 10), self.message)
        watermask = watermark.convert("L").point(lambda x: min(x, 100))
        watermark.putalpha(watermask)
        main.paste(watermark, None, watermark)
        print(filename)
        main.save(filename, "PNG")


