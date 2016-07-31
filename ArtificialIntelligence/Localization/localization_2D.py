# https://classroom.udacity.com/courses/cs373/lessons/48739381/concepts/487350240923#
import matplotlib.pyplot as plt


def uniform(w, h):
    """
    initial uniform distribution (equal, add up to 1)
    :param w:   width
    :param h:   height
    :return:    probability distribution
    """

    prob_d = []
    p_x_i = 1.0 / (w * h)  # probability p(X_i)
    for i in range(h):
        prob_w = []
        for j in range(w):
            prob_w.append(p_x_i)
        prob_d.append(prob_w)
    return prob_d


def sense(p, w, Z, p_hit, p_miss, p_sensor=1.0):
    """
    recalculates probability distribution based on sensed value
    :param p:       probability distribution matrix [[p,...,p],[],...]
    :param w:       world matrix
    :param Z:       measurement
    :param p_hit    probability change for hit
    :param p_miss   probability change for miss
    :param p_sensor probability sensor measurement is correct
    :return:  posterior distribution
    """

    q = [[0.0 for row in range(len(p[0]))] for col in range(len(p))]

    s = 0.0
    for i in range(len(p)):
        for j in range(len(p[i])):
            hit = (Z == w[i][j])
            q[i][j] = p[i][j] * (hit * p_sensor + (1 - hit) * (1 - p_sensor))
            s += q[i][j]
    for i in range(len(q)):
        for j in range(len(p[i])):
            q[i][j] /= s
    return q

    # we have sensed z, probability increases by p_hit if equal
    # q = []
    # for i in range(len(p)):
    #     prob_w = []
    #     for j in range(len(p[i])):
    #         hit = (w[i][j] == Z)
    #         prob_w.append((p[i][j] * (hit * p_sensor + (1 - hit) * (1.0 - p_sensor))))
    #         # if w[i][j] == Z:
    #         #     prob_w.append(p[i][j] * (p_hit - (1.0 - p_sensor)))
    #         # else:
    #         #     prob_w.append(p[i][j] * (p_miss + (1.0 - p_sensor)))
    #     q.append(prob_w)
    #
    # # normalize into probablity distribution
    # p_m_sum = 0
    # for i in range(len(q)):
    #     p_m_sum += sum(q[i])
    #
    # for i in range(len(q)):
    #     for j in range(len(q[i])):
    #         q[i][j] /= p_m_sum

    return q


def move(p, U, p_over=0.0, p_under=0.0, p_motion=1.0):
    """
    move robot by U steps
    :param p:       probability distribution matrix
    :param U:       motion vector [x, y]
    :param p_over   probability to overshoot  p(X_i+U+1 | X_i)
    :param p_under  probability to undershoot p(X_i+U-1 | X_i)
    :param p_motion probability motion execution is accurate
    :return:    posterior distribution
    """

    q = [[0.0 for row in range(len(p[0]))] for col in range(len(p))]
    for i in range(len(p)):
        for j in range(len(p[i])):
            q[i][j] = (p_motion * p[(i - U[0]) % len(p)][(j - U[1]) % len(p[i])]) + ((1.0 - p_motion) * p[i][j])

    # p_exact = 1 - p_over - p_under  # p(X_i+U | X_i)
    #
    # q = []
    # for i in range(len(p)):
    #     q_width = []
    #     for j in range(len(p[i])):
    #         s = (p_motion * p[(i - U[0]) % len(p)][(j - U[1]) % len(p[i])]) + ((1.0 - p_motion) * p[i][j])
    #         # s = p_exact * p[(i - U[1]) % len(p)][(j - U[0]) % len(p)]
    #         # s += p_over * p[(i - U - 1) % len(p)]
    #         # s += p_under * p[(i - U + 1) % len(p)]
    #         q_width.append(s)
    #     q.append(q_width)
    return q

# initialize system
world = [['green', 'green', 'green'],
         ['green', 'red', 'red'],
         ['green', 'green', 'green']]
measurements = ['red', 'red']
motions = [[0, 0], [0, 1]] # [0, 0] = stay, [0, 1] = right, [0, -1] = left, [1, 0] = down, [-1, 0] = up
p = uniform(len(world[0]), len(world))
p_sensor = 0.8  # probability sensor measurement is correct
p_motion = 1.0  # probability motion is executed correctly

# sense and move multiple times
for i in range(len(measurements)):
    p = sense(p, world, measurements[i], 1.0, 0.0, p_sensor)
    p = move(p, motions[i])
    print(p)

