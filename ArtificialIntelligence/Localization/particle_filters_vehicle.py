from math import *
import random
import matplotlib.pyplot as plt

landmarks  = [[0.0, 100.0], [0.0, 0.0], [100.0, 0.0], [100.0, 100.0]]
world_size = 100.0


class robot:
    # --------

    # init:
    #	creates robot and initializes location/orientation
    #

    def __init__(self, length=10.0):
        self.x = random.random() * world_size  # initial x position
        self.y = random.random() * world_size  # initial y position
        self.orientation = random.random() * 2.0 * pi  # initial orientation
        self.length = length  # length of robot
        self.bearing_noise = 0.0  # initialize bearing noise to zero
        self.steering_noise = 0.0  # initialize steering noise to zero
        self.distance_noise = 0.0  # initialize distance noise to zero

    def __repr__(self):
        return '[x=%.6s y=%.6s orient=%.6s]' % (str(self.x), str(self.y), str(self.orientation))

    # --------
    # set:
    #	sets a robot coordinate
    #

    def set(self, new_x, new_y, new_orientation):
        if new_orientation < 0 or new_orientation >= 2 * pi:
            raise ValueError('Orientation must be in [0..2pi]')
        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation)

    # --------
    # set_noise:
    #	sets the noise parameters
    #

    def set_noise(self, new_b_noise, new_s_noise, new_d_noise):
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.bearing_noise = float(new_b_noise)
        self.steering_noise = float(new_s_noise)
        self.distance_noise = float(new_d_noise)

    # --------
    # move:
    #   move along a section of a circular path according to motion
    #

    def move(self, motion):
        """
        moves robot (vehicle) in a circular motion
        reference: Udacity - Circular Motion
        :param motion: [steering angle, distance driven]
        :return: instance of robot after movement
        """

        a = motion[0]                                   # steering angle
        a += random.gauss(0.0, self.steering_noise)     # add randomness to steering
        d = motion[1]                                   # distance driven
        d += random.gauss(0.0, self.distance_noise)     # add randomness to motion
        b = d / self.length * tan(a)                    # turning angle

        result = robot(self.length)                     # return a new object for particles
        result.set_noise(self.bearing_noise, self.steering_noise, self.distance_noise)

        if abs(b) < 0.001:
            x = self.x + d * cos(self.orientation)
            y = self.y + d * sin(self.orientation)
            o = self.orientation
            result.set(x, y, o)
        else:
            r = d / b                                   # turning radius
            cx = self.x - sin(self.orientation) * r     # turning point x
            cy = self.y + cos(self.orientation) * r     # turning point y

            x = cx + sin(self.orientation + b) * r
            y = cy - cos(self.orientation + b) * r
            o = (self.orientation + b) % (2 * pi)
            result.set(x, y, o)

        return result

    def sense(self, bearing_noise=1):
        Z = []
        for i in range(len(landmarks)):
            # landmarks in (y, x) form.
            bearing = atan2(landmarks[i][0] - self.y, landmarks[i][1] - self.x) - self.orientation
            if bearing_noise: bearing += random.gauss(0.0, self.bearing_noise)    # add randomness to bearing
            bearing %= 2.0 * pi
            Z.append(bearing)

        return Z


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
        x = []
        y = []

        for i in range(len(landmarks)):
            # landmarks in (y, x) form.
            x.append(landmarks[i][1])
            y.append(landmarks[i][0])
        plt.plot(x, y, 'ko')

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


length = 20.
bearing_noise = 0.1 # Noise parameter: should be included in sense function.
steering_noise = 0.1 # Noise parameter: should be included in move function.
distance_noise = 5.0 # Noise parameter: should be included in move function.

tolerance_xy = 15.0 # Tolerance for localization in the x and y directions.
tolerance_orientation = 0.25 # Tolerance for orientation.

myrobot = robot(length)
myrobot.set(30.0, 20.0, 0.0)
myrobot.set_noise(bearing_noise, steering_noise, distance_noise)

print('Robot:        ', myrobot)
print('Measurements: ', myrobot.sense())

plot([], myrobot)
