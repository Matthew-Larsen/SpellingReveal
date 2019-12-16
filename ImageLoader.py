from tkinter import *
from tkinter.filedialog import askopenfilename

from PIL import Image

pixels = None
size = None
imageSize = None


def init(total_size=20):
    global pixels, size, imageSize
    root = Tk()
    file = askopenfilename(filetypes=[("Image", ".png .jpg .jpeg")])
    root.destroy()
    im = Image.open(file)
    if im.mode != "RGB":
        im = im.convert("RGB")
    pixels = im.load()
    size1, size2 = im.size
    size = min(size1, size2)
    imageSize = total_size


def get_color_at_pos(x, y):
    return pixels[(x * size) / imageSize, (y * size) / imageSize]

# if __name__ == "__main__":
#    init()
#    print(get_color_at_pos(0, 0))
