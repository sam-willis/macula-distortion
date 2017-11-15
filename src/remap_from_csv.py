import csv
import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline
from scipy.integrate import cumtrapz as intergrate
import matplotlib.pyplot as plt
import pickle
from math import atan, pi

RES_STEP = 2000  # possibly should be resolution of screen i.e 2000?
loss_function = lambda x: 1 if x > 10 else 0


def main():
    X, f, _ = get_remap()
    plt.plot(X, f(X))
    plt.xlabel("Normal Eye")
    plt.ylabel("Macular Degeneration")
    plt.show()


def get_remap():
    """
    Returns a mapping of 0-45 degrees of a healthy persons visual
    field to 0-n degrees of someone with macula degeneration
    """
    with open('../textPopup/bound_1368_912.pickle', 'rb') as f:
        r, f = pickle.load(f)

    cone_density = 1 / f
    angle = to_degrees(r)

    #plt.plot(angle, cone_density)
    #plt.show()

    X = np.linspace(0, 45, RES_STEP)
    X_bar = [(X[i] + X[i + 1]) / 2 for i in range(len(X) - 1)]

    # f is the cone density function with angle

    f = InterpolatedUnivariateSpline(angle, cone_density, k=1)
    f_norm = f(X)

    #plt.plot(X, f_norm)
    #plt.show()

    f_macl = [f(x) * loss_function(x) for x in X]

    #plt.plot(X, f_macl)
    #plt.show()

    # g is the cumulative infomation function with angle

    i_norm = intergrate(f_norm, X)
    i_macl = intergrate(f_macl, X)

    #plt.plot(X, f_norm, X, f_macl, X_bar, g_norm, X_bar, g_macl)

    g_norm = InterpolatedUnivariateSpline(X_bar, i_norm, k=1)
    g_norm_inv = InterpolatedUnivariateSpline(i_norm, X_bar, k=1)
    g_macl = InterpolatedUnivariateSpline(X_bar, i_macl, k=1)
    g_macl_inv = InterpolatedUnivariateSpline(i_macl, X_bar, k=1)

    #return X, g_macl_inv(g_norm(X))
    return X, lambda X: g_macl_inv(g_norm(X)), lambda Y: g_norm_inv(g_macl(Y))


def next_column(columns):
    return [float(item) for item in next(columns) if item is not ""]


def to_degrees(dists_in_px):
    dists_in_mms = 146.5 / 1368 * dists_in_px
    return [atan(dist / 80) * 180 / pi for dist in dists_in_mms]


def iterp(x, y):
    return InterpolatedUnivariateSpline(x, y, k=1)


if __name__ == '__main__':
    main()