# https://classroom.udacity.com/courses/cs373/lessons/48739381/concepts/487350240923#


def localize(world, measurements, motions, p_sensor=1.0, p_motion=1.0):
    """
    localize position of robot in world based on measurements at varying positions
    :param world:           world matrix (colors)
    :param measurements:    measurements list (colors)
    :param motions:         motion list ([x, y])
    :param p_sensor:        probability sensor measurement is correct
    :param p_motion:        probability motion execution is correct
    :return:                posterior probability distribution
    """

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

    def normalize(p):
        """
        normalize probability distribution to sum up to 1
        :param p: probability distribution
        """

        p_sum = 0
        for i in range(len(p)):
            p_sum += sum(p[i])

        normalizer = 1.0 / p_sum

        for i in range(len(p)):
            for j in range(len(p[i])):
                p[i][j] *= normalizer

    def move(p, motion, p_motion):
        """
        move robot [0, 0] = stay, [0, 1] = right, [0, -1] = left, [1, 0] = down, [-1, 0] = up
        :param p:       probability distribution matrix
        :param motion:  motion vector [x, y]
        :param p_motion probability motion execution is accurate, the robot will either move correctly or stay
        :return:        posterior distribution
        """

        q = []
        for i in range(len(p)):
            q_row = []
            for j in range(len(p[i])):
                s = (p_motion * p[(i - motion[0]) % len(p)][(j - motion[1]) % len(p[i])]) + ((1 - p_motion) * p[i][j])
                q_row.append(s)
            q.append(q_row)
        return q

    def sense(p, w, z, p_sensor=1.0):
        """
        recalculates probability distribution based on sensed value
        :param p:       probability distribution matrix [[p,...,p],[],...]
        :param w:       world matrix
        :param z:       measurement
        :param p_sensor probability sensor measurement is correct
        :return:        posterior distribution
        """

        # we have sensed z, probability increases by p_hit if equal
        q = []
        for i in range(len(p)):
            q_row = []
            for j in range(len(p[i])):
                if w[i][j] == z:
                    q_row.append(p[i][j] * p_sensor)
                else:
                    q_row.append(p[i][j] * (1.0 - p_sensor))
            q.append(q_row)
        normalize(q)
        return q

    p = uniform(len(world[0]), len(world))

    for i in range(len(measurements)):
        p = move(p, motion=motions[i], p_motion=p_motion)
        p = sense(p, world, measurements[i], p_sensor=p_sensor)

    return p


def show(p):
    """
    print matrix in a more readable format
    :param p: probability distributon
    """
    rows = ['[' + ', '.join(map(lambda x: '{0:.5f}'.format(x), r)) + ']' for r in p]
    print('\n'.join(rows) + '\n')

world = [['R', 'G', 'G', 'R', 'R'],
         ['R', 'R', 'G', 'R', 'R'],
         ['R', 'R', 'G', 'G', 'R'],
         ['R', 'R', 'R', 'R', 'R']]
measurements = ['G', 'G', 'G', 'G', 'G']
motions = [[0, 0], [0, 1], [1, 0], [1, 0], [0, 1]]

p = localize(world, measurements, motions, p_sensor=0.7, p_motion=0.8)
show(p)
