from math import *
import warnings

# make predictions about future positions

# measurement meant updating our belief (and renormalizing our distribution).
# motion meant keeping track of where all of our probability "went" when we moved

# Kalman Filter:
# measurement update: bayes rule (multiplication)
# motion update prediction: total probability (addition)


def f(m, v, x):
    """
    gaussian computation (deprecated)
    :param m: mean (mu)
    :param v: variance (sigma squared)
    :param x: x
    """

    return 1 / sqrt(2.0 * pi * v) * exp(-0.5 * (x - m)**2 / v)


def update(m1, v1, m2, v2):
    """
    measurement update step (kalman filter)
    updates mean and variance based on previous measurement and new observation
    :param m1: previous mean (mu)
    :param v1: previous variance (sigma^2)
    :param m2: observed mean (mu)
    :param v2: observed variance (sigma^2)
    :return: new mean and variance [m, v]
    """

    m = (v1 * m2 + v2 * m1) / (v1 + v2)
    v = 1. / (1. / v1 + 1. / v2)
    return [m, v]


def predict(m1, v1, m2, v2):
    """
    predicts mean and variance based on movement
    :param m1: previous mean (mu)
    :param v1: previous variance (sigma^2)
    :param m2: observed mean (mu)
    :param v2: observed variance (sigma^2)
    :return: new mean and variance [m, v]
    """

    m = m1 + m2
    v = v1 + v2
    return [m, v]


def main():
    measurements = [5., 6., 7., 9., 10.]
    motion = [1., 1., 2., 1., 1.]
    measurement_sig = 4.
    motion_sig = 2.
    mu = 0.
    sig = 10000.

    result = [mu, sig]
    for i in range(len(measurements)):
        # sense
        result = update(result[0], result[1], measurements[i], measurement_sig)
        print('update:  ', result)
        # move
        result = predict(result[0], result[1], motion[i], motion_sig)
        print('predict: ', result)

    # print(update(10, 4, 12, 4))

if __name__ == "__main__":
    main()
