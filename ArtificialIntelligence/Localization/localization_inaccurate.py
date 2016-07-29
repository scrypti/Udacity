# https://classroom.udacity.com/courses/cs373/lessons/48739381/concepts/487350240923#
import matplotlib.pyplot as plt


def uniform(n):
    """
    initial uniform distribution (equal, add up to 1)
    :param n:   size of vector
    :return:    probability distribution
    """

    prob_d = []
    p_x_i = 1.0 / n  # probability p(X_i)
    for i in range(n):
        prob_d.append(p_x_i)

    return prob_d


def sense(p, w, Z, p_hit, p_miss):
    """
    recalculates probability distribution based on sensed value
    :param p:       probability distribution
    :param w:       world
    :param Z:       measurement
    :param p_hit    probability change for hit
    :param p_miss   probability change for miss
    :return:  posterior distribution
    """

    # we have sensed z, probability increases by p_hit if equal
    post_d = []  # q
    for i in range(len(p)):
        if w[i] == Z:
            post_d.append(p[i] * p_hit)
        else:
            post_d.append(p[i] * p_miss)

    # normalize into probablity distribution
    p_m_sum = sum(post_d)
    for i in range(len(post_d)):
        post_d[i] /= p_m_sum

    return post_d


def move(p, U, p_over, p_under):
    """
    move robot by U steps
    :param p:       probability distribution
    :param U:       number of steps
    :param p_over   probability to overshoot  p(X_i+U+1 | X_i)
    :param p_under  probability to undershoot p(X_i+U-1 | X_i)
    :return:    posterior distribution
    """

    p_exact = 1 - p_over - p_under  # p(X_i+U | X_i)

    q = []
    for i in range(len(p)):
        s = p_exact * p[(i - U) % len(p)]
        s += p_over * p[(i - U - 1) % len(p)]
        s += p_under * p[(i - U + 1) % len(p)]
        q.append(s)  # p(X_i) = p_exact * p(X_i - U) + p_over * p(X_i - U - 1) + p_under * p(X_i - U + 1)
    return q

# initialize syste
world = ['green', 'red', 'red', 'green', 'green']  # world, green = door, red = wall
measurements = ['red', 'green']
motions = [1, 1]
p = uniform(len(world))

# sense environment
# Z = 'blue'  # sensed value (measurement)
# p = sense(p, w, Z, 0.6, 0.2)  # p_hit = 0.6, p_miss = 0.2 (arbitrary values)
# print(p)  # p(X_i | Z)

# move
U = 1  # step size
p = move(p, U, 0.1, 0.1)
print(p)

for i in range(len(measurements)):
    
