import numpy as np
from scipy import ndimage
from math import sqrt, atan2


def convert_polar_factory(img):
    width, height, _ = img.shape

    def convert_polar(x_abs, y_abs):
        x_centred = width // 2 - x_abs
        y_centred = height // 2 - y_abs
        r = sqrt(x_centred**2 + y_centred**2)
        theta = atan2(y_centred, x_centred)
        return r, theta

    return convert_polar


def main():
    img = ndimage.imread('images/test.png')

    import matplotlib.pyplot as plt
    plt.imshow(img)
    plt.axis('off')
    plt.show()


if __name__ == '__main__':
    main()