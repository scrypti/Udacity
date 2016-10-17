from math import *
import random
import matplotlib.pyplot as plt

landmarks = [[20.0, 20.0], [80.0, 80.0], [20.0, 80.0], [80.0, 20.0]]
world_size = 100.0


class robot:
    def __init__(self):
        self.x = random.random() * world_size
        self.y = random.random() * world_size
        self.orientation = random.random() * 2.0 * pi
        self.forward_noise = 0.0;
        self.turn_noise = 0.0;
        self.sense_noise = 0.0;

    def set(self, new_x, new_y, new_orientation):
        if new_x < 0 or new_x >= world_size:
            raise ValueError('X coordinate out of bound')
        if new_y < 0 or new_y >= world_size:
            raise ValueError('Y coordinate out of bound')
        if new_orientation < 0 or new_orientation >= 2 * pi:
            raise ValueError('Orientation must be in [0..2pi]')
        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation)

    def set_noise(self, new_f_noise, new_t_noise, new_s_noise):
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.forward_noise = float(new_f_noise);
        self.turn_noise = float(new_t_noise);
        self.sense_noise = float(new_s_noise);

    def sense(self):
        Z = []
        for i in range(len(landmarks)):
            dist = sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
            dist += random.gauss(0.0, self.sense_noise)
            Z.append(dist)
        return Z

    def move(self, turn, forward):
        if forward < 0:
            raise ValueError('Robot cant move backwards')

            # turn, and add randomness to the turning command
        orientation = self.orientation + float(turn) + random.gauss(0.0, self.turn_noise)
        orientation %= 2 * pi

        # move, and add randomness to the motion command
        dist = float(forward) + random.gauss(0.0, self.forward_noise)
        x = self.x + (cos(orientation) * dist)
        y = self.y + (sin(orientation) * dist)
        x %= world_size  # cyclic truncate
        y %= world_size

        # set particle
        res = robot()
        res.set(x, y, orientation)
        res.set_noise(self.forward_noise, self.turn_noise, self.sense_noise)
        return res

    def Gaussian(self, mu, sigma, x):

        # calculates the probability of x for 1-dim Gaussian with mean mu and var. sigma
        return exp(- ((mu - x) ** 2) / (sigma ** 2) / 2.0) / sqrt(2.0 * pi * (sigma ** 2))

    def measurement_prob(self, measurement):

        # calculates how likely a measurement should be

        prob = 1.0;
        for i in range(len(landmarks)):
            dist = sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
            prob *= self.Gaussian(dist, self.sense_noise, measurement[i])
        return prob

    def __repr__(self):
        return '[x=%.6s y=%.6s orient=%.6s]' % (str(self.x), str(self.y), str(self.orientation))


def eval(r, p):
    sum = 0.0;
    for i in range(len(p)):  # calculate mean error
        dx = (p[i].x - r.x + (world_size / 2.0)) % world_size - (world_size / 2.0)
        dy = (p[i].y - r.y + (world_size / 2.0)) % world_size - (world_size / 2.0)
        err = sqrt(dx * dx + dy * dy)
        sum += err
    return sum / float(len(p))

# the larger the weight of the particle, the more important it is
# the probability of survival is proportional to the particle weight, heavy particles are more likely to survive


def particle_init(n):
    # places particles randomly
    p2 = []
    for i in range(n):
        r = robot()
        r.set_noise(0.05, 0.05, 5.0)
        p2.append(r)
    return p2


def particle_move(p, Z, turn, forward):
    # moves particles and collects measurement data
    w2 = []
    for i in range(len(p)):
        p[i] = p[i].move(turn, forward)
        w2.append(p[i].measurement_prob(Z))
    return w2


def particle_resample(p, w):
    # selects 1000 particles out of the current list of particles, particle weight normalized into probability
    p2 = []
    normalizer = sum(w)

    # alternatively use (optimized) version from udacity: resampling wheel
    def probability_select():
        r = random.uniform(0, 1)
        c = 0
        for i in range(len(w)):
            c += w[i] / normalizer
            if r <= c:
                return p[i]
        raise ValueError('probability select out of bounds')

    for i in range(len(p)):
        p2.append(probability_select())
    return p2


def plot(p, r):
    def plot_landmarks():
        plt.plot([20, 80, 20, 80], [20, 80, 80, 20], 'ko')

    def plot_robot(r):
        if isinstance(r, robot):
            plt.plot([r.x], [r.y], 'bo')

    def plot_particles(p):
        x = []
        y = []
        for i in range(len(p)):
            particle = p[i]
            if isinstance(particle, robot):
                x.append(particle.x)
                y.append(particle.y)
        plt.plot(x, y, 'ro')

    plot_particles(p)
    plot_robot(r)
    plot_landmarks()
    plt.axis([0, 100, 0, 100])
    plt.show()

myrobot = robot()
myrobot.set(20, 50, 0)
p = particle_init(n=1000)

# plot(p, myrobot)

for i in range(30):
    m = [0.1, 5.0]

    myrobot = myrobot.move(m[0], m[1])
    Z = myrobot.sense()

    w = particle_move(p, Z, m[0], m[1])
    p = particle_resample(p, w)

    print('particle error: ', eval(myrobot, p))
    plot(p, myrobot)
# print(p)
