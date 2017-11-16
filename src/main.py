import scipy.misc
from scipy import ndimage
from create_test import create_new_test_image
from remapper import apply_macula_distortion
import pickler


def main():
    random_images()

def random_images():
    for c in ["me (1)","me (2)","me (3)","me (4)","me (5)","me (6)"]:
    #for c in ["me (1)"]:
        img_path = './images/{}.jpg'.format(c)
        img = ndimage.imread(img_path)
        img_hole = apply_macula_distortion(img, fix_image = False)
        img_macl = apply_macula_distortion(img, fix_image = True)
        scipy.misc.imsave('./images/{}_hole.png'.format(c), img_hole)
        scipy.misc.imsave('./images/{}_macl.png'.format(c), img_macl)

def random_word_image():
    try:
        c = pickler.load('imgCount')
    except FileNotFoundError:
        c = 0
    img_path = './images/test_{}.png'.format(c)
    create_new_test_image(img_path)

    img_path = './images/face1.png'
    img = ndimage.imread(img_path)
    img_macl = apply_macula_distortion(img)
    scipy.misc.imsave('./images/test_macl_{}.png'.format(c), img_macl)

    pickler.save('imgCount', c + 1)


if __name__ == '__main__':
    main()
