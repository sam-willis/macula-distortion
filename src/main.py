import numpy as np
from scipy import ndimage
from math import sqrt, atan2

# make sensible assumptions about the size of the retina the image takes up
# i.e. which pixels correlate to what density
# load csv, times pixel
# 1 - exp

# intergrate function 
# assume -45 to 45 degree arc
# what part of the retina is that
# 1mm ~3.5 degrees http://hubel.med.harvard.edu/book/b10.htm
# 0-~11mm on retina (very very roughly) 


class Something:
    def __init__(self, img):
        self.img = img
        self.width, self.height, _ = img.shape
        self.dict = {}

    def build_dictionary(self):
        for x in range(self.width):
            for y in range(self.height):
                self.dict[x, y] = self.convert_polar(x, y)

    def convert_polar(self, x_abs, y_abs):
        x_centred = x_abs - self.width // 2
        y_centred = y_abs - self.height // 2
        r = sqrt(x_centred**2 + y_centred**2)
        theta = atan2(y_centred, x_centred)
        return r, theta


def main():
    img = ndimage.imread('images/test.png')
    Something(img)
    import matplotlib.pyplot as plt
    plt.imshow(img)
    plt.axis('off')
    plt.show()


if __name__ == '__main__':
    main()
