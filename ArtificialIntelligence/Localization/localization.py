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


def move(p, U):
    """
    move robot by U steps
    :param p:   probability distribution
    :param U:   number of steps
    :return:    posterior distribution
    """

    q = []
    for i in range(len(p)):
        q.append(p[(i - U) % len(p)])
    return q

# initialize system
w = ['red', 'blue', 'red', 'blue', 'red', 'red', 'red', 'red', 'blue', 'red', 'red']  # world, blue = door, red = wall
p = uniform(len(w))  # vector size
print(p)  # p(X_i)
plt.plot(p)

# sense environment
Z = 'blue'  # sensed value (measurement)
p = sense(p, w, Z, 0.6, 0.2)  # p_hit = 0.6, p_miss = 0.2 (arbitrary values)
print(p)  # p(X_i | Z)
plt.plot(p)

# move
U = 1  # step size
p = move(p, U, True)
print(p)
plt.plot(p)

plt.show()
