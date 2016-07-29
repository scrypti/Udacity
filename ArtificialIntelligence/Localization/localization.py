# https://classroom.udacity.com/courses/cs373/lessons/48739381/concepts/487350240923#


def probability_distribution(n):
    """
    initial distribution
    :param n:   size of vector
    :return:    probability distribution
    """

    prob_d = []
    p_x_i = 1.0 / n  # probability p(X_i)
    for i in range(n):
        prob_d.append(p_x_i)

    return prob_d


def posterior_distribution(p, w, Z, p_hit, p_miss):
    """
    measurement update (sense)
    adjust probability of p with regard to Z
    :param p:       places
    :param w:       world
    :param Z:       measurement
    :param p_hit    probability change for hit
    :param p_miss   probability change for miss
    :return:        normalized posterior distribution
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

w = ['green', 'red', 'red', 'green', 'green']  # world, green = door, red = wall
prob_d = probability_distribution(5)  # probability distribution, equal probability (add up to 1)
print(prob_d)  # p(X_i)

Z = 'red'  # sensed value (measurement)
post_d = posterior_distribution(prob_d, w, Z, 0.6, 0.2)  # p_hit = 0.6, p_miss = 0.2 (arbitrary values)
print(post_d)  # p(X_i | Z)
