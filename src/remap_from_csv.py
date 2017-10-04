import csv
from math import expm1
from numpy import linspace
from scipy.interpolate import InterpolatedUnivariateSpline
from scipy.integrate import cumtrapz as intergrate
import matplotlib.pyplot as plt

RES_STEP = 500  # possibly should be resolution of screen i.e 2000?


def next_column(columns):
    return [float(item) for item in next(columns) if item is not ""]


def to_degrees(dists_in_mms):
    return [dist * 3.5 for dist in dists_in_mms]


def iterp(x, y):
    return InterpolatedUnivariateSpline(x, y, k=1)


def get_remap():
    """
    Returns a mapping of 0-45 degrees of a healthy persons visual
    field to 0-n degrees of someone with macula degeneration
    """

    with open('retinal_density_model.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        columns = zip(*reader)
        cone_density = next_column(columns)
        angle = to_degrees(next_column(columns))

    X = linspace(0, 45, RES_STEP)
    X_bar = [(X[i] + X[i + 1]) / 2 for i in range(len(X) - 1)]

    # f is the cone density function with angle

    f = InterpolatedUnivariateSpline(angle, cone_density, k=1)
    f_norm = f(X)
    f_macl = [f(x) * -expm1(-x) for x in X]

    # g is the cumulative infomation function with angle

    g_norm = intergrate(f_norm, X)
    g_macl = intergrate(f_macl, X)

    #plt.plot(X, f_norm, X, f_macl, X_bar, g_norm, X_bar, g_macl)

    g_norm = InterpolatedUnivariateSpline(X_bar, g_norm, k=1)
    g_macl_inv = InterpolatedUnivariateSpline(g_macl, X_bar, k=1)

    #return X, g_macl_inv(g_norm(X))
    return X, lambda X: g_macl_inv(g_norm(X))


def main():
    X, f = get_remap()
    plt.plot(X, f(X))
    plt.show()


if __name__ == '__main__':
    main()