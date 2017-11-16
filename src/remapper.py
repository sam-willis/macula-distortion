import numpy as np
import cv2
from scipy import ndimage
from skimage.transform import warp
from math import sqrt
from remap_from_csv import get_remap
import matplotlib.pyplot as plt

NO_FLAG = 0
INV_FLAG = 2**4

# from math import expm1
# K = 1
# LOSS_FUNCTION = lambda x: -expm1(-x * K)

#LOSS_FUNCTION = lambda x: 0.5 + 0.5 * x


def main():
    #img_path = 'images/circle_image.jpg'
    img_path = 'images/me (1).JPG'
    img = ndimage.imread(img_path)
    plt.axis('off')
    img_macl = apply_macula_distortion(img, True)
    plt.imshow(img_macl)
    plt.show()


def apply_macula_distortion(img, fix_image = True):
    w, h = img.shape[:2]
    origin = (h // 2, w // 2)
    max_r = sqrt(w**2 + h**2) / 2
    polar_img = cv2.linearPolar(img, origin, max_r, NO_FLAG)
    #plt.imshow(polar_img)
    #plt.show()
    reverse_map = create_reverse_map(polar_img, fix_image)
    polar_img = warp(polar_img, reverse_map)
    warped_img = cv2.linearPolar(polar_img, origin, max_r, INV_FLAG)
    return warped_img

def create_reverse_map(img, fix=True):
    width, _, _ = img.shape
    _, _, remap_degrees = get_remap(fix)
    remap_pixels = lambda X: degrees_to_pixels(remap_degrees(pixels_to_degrees(X)))

    def pixels_to_degrees(X):
        return X * 35 / width  

    def degrees_to_pixels(X):
        return X * width / 35

    def reverse_map(xy):
        xy[:, 0] = remap_pixels(xy[:, 0])
        return xy

    return reverse_map


if __name__ == '__main__':
    main()
