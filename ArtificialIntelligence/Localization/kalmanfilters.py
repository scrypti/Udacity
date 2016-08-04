from math import *
import warnings

# measurement meant updating our belief (and renormalizing our distribution).
# motion meant keeping track of where all of our probability "went" when we moved
# (which meant using the law of Total Probability)

# Kalman Filter:
# measurement update: bayes rule (multiplication)
# motion update prediction: total probability (addition)


def f(m, v, x):
    """
    gaussian computation (deprecated)
    """
    return 1 / sqrt(2.0 * pi * v) * exp(-0.5 * (x - m) ** 2 / v)


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

    m = (v2 * m1 + v1 * m2) / (v1 + v2)
    v = 1.0 / (1.0 / v1 + 1.0 / v2)
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

measurements = [5., 6., 7., 9., 10.]
motion = [1., 1., 2., 1., 1.]
measurement_sig = 4.
motion_sig = 2.
mu = 0.
sig = 10000.

# print(update(10, 8, 13, 2))
# print(predict(10, 4, 12, 4))

for i in range(len(measurements)):
    [mu, sig] = update(mu, sig, measurements[i], measurement_sig)
    print('update:  ', [mu, sig])
    [mu, sig] = predict(mu, sig, motion[i], motion_sig)
    print('predict: ', [mu, sig])
