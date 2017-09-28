from math import pi
from main import convert_polar_factory


class FakeImg:
    def __init__(self, height, width):
        self.shape = (height, width, 3)


def test_convert_polar():
    img = FakeImg(10, 10)
    convert_polar = convert_polar_factory(img)
    assert convert_polar(0, 0) == (100, 3 * pi / 4)
