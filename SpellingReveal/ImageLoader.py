from PIL import Image

pixels = None
size = None


def init():
    global pixels, size
    im = Image.open("image.jpg")
    pixels = im.load()
    size, _ = im.size


def get_color_at_pos(x, y, total_size):
    global pixels, size
    if not pixels:
        init()

    return pixels[x * size / total_size, y * size / total_size]
