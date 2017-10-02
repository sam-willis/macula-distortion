from math import pi, sqrt
from pytest import approx
from main import Something


class FakeImg:
    def __init__(self, height, width):
        self.shape = (height, width, 3)


def test_convert_polar():
    img = FakeImg(10, 10)
    something = Something(img)
    r, theta = something.convert_polar(0, 0)
    assert r == approx(sqrt(50))
    assert theta % (2 * pi) == approx(5 * pi / 4 % (2 * pi))


def test_build_dict():
    img = FakeImg(10, 10)
    something = Something(img)
    something.build_dictionary()
