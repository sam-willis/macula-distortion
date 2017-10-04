import numpy as np
import cv2
from scipy import ndimage
from skimage.transform import warp
from math import sqrt
from remap_from_csv import get_remap

NO_FLAG = 0
INV_FLAG = 2**4

def main():
    import matplotlib.pyplot as plt

    img_path = 'images/test.png'
    img = ndimage.imread(img_path)
    plt.axis('off')
    plt.imshow(apply_macula_distortion(img))
    plt.show()

def apply_macula_distortion(img):
    w, h = img.shape[:2]
    polar_img = cv2.linearPolar(img, (h//2, w//2), sqrt(w**2+h**2)/2, NO_FLAG)
    polar_img = np.flip(polar_img, 1)
    reverse_map = create_reverse_map(polar_img)
    warped = warp(polar_img, reverse_map)
    warped = np.flip(warped, 1)
    return cv2.linearPolar(warped, (h//2, w//2), sqrt(w**2+h**2)/2, INV_FLAG)
    

def create_reverse_map(img):
    _, height, _ = img.shape

    def pixels_to_degrees(X):
        return X * 45 / height

    def degrees_to_pixels(X):
        return X * height / 45

    def reverse_map(xy):
        _, remap_degrees = get_remap()
        remap_pixels = lambda X: degrees_to_pixels(remap_degrees(pixels_to_degrees(X)))

        xy[:, 0] = remap_pixels(xy[:, 0])
        return xy

    return reverse_map


if __name__ == '__main__':
    main()
