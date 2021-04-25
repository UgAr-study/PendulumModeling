""" Calculate the double pendulum angles and speeds """
from __future__ import division
import numpy as np
from numpy import linalg as LA
from math import sin, cos

g = 9.8


class Integrator:
    """ Integrator for solving differential equations """
    def __init__(self, _sum, dx):
        """ _sum is the initial value of the target function and dx is the step
        of the independent variable """
        self.sum = _sum
        self.dx = dx

    def __call__(self, f):
        """ Get the area under the curve of f and accumulate for the
        next call """
        self.sum += self.dx * f
        return self.sum


class Solver:
    """Solve for second-order differential equations"""
    def __init__(self, A, B, C, y_dot, y):
        self.A = A
        self.B = B
        self.C = C

    def get_next(self):


    def




class ConnectedPendulums:
    """ Numerical simulation of a double pendulum system using the angles of
    the pendulums """
    def __init__(self, dt, phi1: float=0.1, phi2: float=0.1, phi3: float=0.1,
                 phi1_dot: float = 0.0, phi2_dot: float = 0.0, phi3_dot: float = 0.0,
                 k1: float=1.0, k2: float=1.0,
                 m1: float=1.0, m2: float=1.0, m3: float=1.0, l: float=1.0, betta: float=0.1):
        """ dt is the time-step, th10 and th20 are the initial angles, thp10 and
        thp20 are initial speeds, len is the length of the pendulums and m their
        mass """
        self.dt = dt
        self.phi = np.array([[phi1, phi2, phi3]]).transpose()
        self.phi_dot = np.array([[phi1_dot, phi2_dot, phi3_dot]]).transpose()
        self.A = np.diag([m1*l**2, m2*l**2, m3*l**2])
        self.B = np.zeros((3, 3))
        self.B[2][2] = betta
        c11 = m1*g*l + k1*l**2 / 4
        c12 = -k1*l**2 / 4
        c13 = 0
        c21 = c12
        c22 = m2*g*l + (k1 + k2)*l**2 / 4
        c23 = -k2*l**2 / 4
        c31 = 0
        c32 = c23
        c33 = m3*g*l + k2*l**2 / 4
        self.C = np.array([[c11, c12, c13],
                           [c21, c22, c23],
                           [c31, c32, c33]])

    def __acc(self):
        """compute the phi_dot_dot"""
        return -(np.dot(np.dot(LA.inv(self.A), self.B), self.phi_dot) +
                 np.dot(np.dot(LA.inv(self.A), self.C), self.phi))

    def get_next_state(self):
        """ Numerically solve the system angles for a single time step """
        acc = self.__acc()
        self.phi_dot += acc * self.dt
        self.phi += self.phi_dot * self.dt

        return self.phi


def main():
    """ Run the test program """
    import matplotlib.pyplot as plt
    dt = 0.1
    t = np.arange(0, 100, dt)
    pendulums = ConnectedPendulums(dt)

    phis1, phis2, phis3 = [], [], []
    print('Simulating...')
    for ti in t:
        phis = pendulums.get_next_state().reshape((3,))
        phis1.append(phis[0])
        phis2.append(phis[1])
        phis3.append(phis[2])

    phis1 = np.array(phis1)
    phis2 = np.array(phis2)
    phis3 = np.array(phis3)
    print('Finished!')

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
    fig.suptitle('A tale of 3 subplots')

    ax1.plot(t, phis1)
    ax1.set_ylabel('phis1')

    ax2.plot(t, phis2)
    ax2.set_ylabel('phis2')

    ax3.plot(t, phis3)
    ax3.set_ylabel('phis3')
    ax3.set_xlabel('time (s)')

    plt.show()


if __name__ == '__main__':
    main()
