""" Calculate the double pendulum angles and speeds """
from __future__ import division
import numpy as np
from numpy import linalg as LA

g = 9.8


class InitState:

    def __init__(self, phi: float = 0, phi_dot: float = 1.0, m: float = 1):
        self.phi = phi
        self.phi_dot = phi_dot
        self.m = m


class ConnectedPendulums:
    """ Numerical simulation of a double pendulum system using the angles of
    the pendulums """

    def __init__(self, dt, pend1: InitState, pend3: InitState, pend2: InitState,
                 k1: float = 1.0, k2: float = 1.0,
                 l: float = 1.0, betta: float = 0.1):
        """ dt is the time-step, th10 and th20 are the initial angles, thp10 and
        thp20 are initial speeds, len is the length of the pendulums and m their
        mass """
        self.dt = dt
        self.phi = np.array([[pend1.phi, pend2.phi, pend3.phi]]).transpose()
        self.phi_dot = np.array([[pend1.phi_dot, pend2.phi_dot, pend3.phi_dot]]).transpose()
        self.A = np.diag([pend1.m * l ** 2, pend2.m * l ** 2, pend3.m * l ** 2])
        self.B = np.zeros((3, 3))
        self.B[2][2] = betta
        c11 = pend1.m * g * l + k1 * l ** 2 / 4
        c12 = -k1 * l ** 2 / 4
        c13 = 0
        c21 = c12
        c22 = pend2.m * g * l + (k1 + k2) * l ** 2 / 4
        c23 = -k2 * l ** 2 / 4
        c31 = 0
        c32 = c23
        c33 = pend3.m * g * l + k2 * l ** 2 / 4
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

        return self.phi, self.phi_dot


def main():
    """ Run the test program """
    import matplotlib.pyplot as plt
    dt = 0.1
    t = np.arange(0, 100, dt)

    pend1 = InitState(0.2, 0.1, 1)
    pend2 = InitState(0.25, 0.01, 4)
    pend3 = InitState(0.14, 0.15, 2)

    pendulums = ConnectedPendulums(dt, pend1, pend2, pend3, 2, 3, 2, 0.4)

    phis1, phis2, phis3 = [], [], []
    phis1_dot, phis2_dot, phis3_dot = [], [], []

    print('Simulating...')
    for ti in t:
        phis = pendulums.get_next_state()[0].reshape((3,))

        phis1.append(phis[0])
        phis2.append(phis[1])
        phis3.append(phis[2])

        phis_dot = pendulums.get_next_state()[1].reshape((3,))
        phis1_dot.append(phis_dot[0])
        phis2_dot.append(phis_dot[1])
        phis3_dot.append(phis_dot[2])

    phis1 = np.array(phis1)
    phis2 = np.array(phis2)
    phis3 = np.array(phis3)

    phis1_dot = np.array(phis1_dot)
    phis2_dot = np.array(phis2_dot)
    phis3_dot = np.array(phis3_dot)

    print('Finished!')

    fig, (phi1, phi1_dot, phi2, phi2_dot, phi3, phi3_dot) = plt.subplots(6, 1)
    fig.suptitle('A tale of 3 subplots')

    phi1.plot(t, phis1)
    phi1.set_ylabel('phi1')

    phi1_dot.plot(t, phis1_dot)
    phi1_dot.set_ylabel('phi1_dot')

    phi2.plot(t, phis2)
    phi2.set_ylabel('phi2')

    phi2_dot.plot(t, phis2_dot)
    phi2_dot.set_ylabel('phi2_dot')

    phi3.plot(t, phis3)
    phi3.set_ylabel('phi3')

    phi3_dot.plot(t, phis3_dot)
    phi3_dot.set_ylabel('phi3_dot')

    phi3_dot.set_xlabel('time (s)')

    plt.show()


if __name__ == '__main__':
    main()
