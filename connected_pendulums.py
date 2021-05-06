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

    def __init__(self, dt: float, pend1: InitState, pend3: InitState, pend2: InitState,
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

    def get_timestep(self):
        return self.dt

    def __acc(self):
        """compute the phi_dot_dot"""
        return -(np.dot(np.dot(LA.inv(self.A), self.B), self.phi_dot) +
                 np.dot(np.dot(LA.inv(self.A), self.C), self.phi))

    def get_next_state(self):
        """ Numerically solve the system angles for a single time step """
        acc = self.__acc()
        self.phi_dot = self.phi_dot + acc * self.dt
        self.phi = self.phi + self.phi_dot * self.dt
        return self.phi, self.phi_dot

    def get_current_state(self):
        return self.phi, self.phi_dot


def show_plots(pendulums: ConnectedPendulums, duration: float = 40.0):
    """ Make plots without animation """
    import matplotlib.pyplot as plt

    t = np.arange(0, duration, dt)

    phis, phis_dot = pendulums.get_current_state()
    phis.reshape((3,))
    phis_dot.reshape((3,))

    phis1, phis2, phis3 = [phis[0]], [phis[1]], [phis[2]]
    phis1_dot, phis2_dot, phis3_dot = [phis_dot[0]], [phis_dot[1]], [phis_dot[2]]

    size = t.size
    i = 1
    while i < size:

        phis, phis_dot = pendulums.get_next_state()
        phis.reshape((3,))
        phis_dot.reshape((3,))

        phis1.append(phis[0])
        phis2.append(phis[1])
        phis3.append(phis[2])

        phis1_dot.append(phis_dot[0])
        phis2_dot.append(phis_dot[1])
        phis3_dot.append(phis_dot[2])

        i += 1

    phis1 = np.array(phis1)
    phis2 = np.array(phis2)
    phis3 = np.array(phis3)

    phis1_dot = np.array(phis1_dot)
    phis2_dot = np.array(phis2_dot)
    phis3_dot = np.array(phis3_dot)

    fig, (phi1_plt, phi1_dot_plt, phi2_plt, phi2_dot_plt,
          phi3_plt, phi3_dot_plt) = plt.subplots(6, 1)

    fig.suptitle(r'$\varphi$ and $\dot \varphi$ plots')

    phi1_plt.plot(t, phis1)
    phi1_plt.set_ylabel(r'$\varphi_1$', rotation=0)

    phi1_dot_plt.plot(t, phis1_dot)
    phi1_dot_plt.set_ylabel(r'$\dot \varphi_1$', rotation=0)

    phi2_plt.plot(t, phis2)
    phi2_plt.set_ylabel(r'$\varphi_2$', rotation=0)

    phi2_dot_plt.plot(t, phis2_dot)
    phi2_dot_plt.set_ylabel(r'$\dot \varphi_2$', rotation=0)

    phi3_plt.plot(t, phis3)
    phi3_plt.set_ylabel(r'$\varphi_3$', rotation=0)

    phi3_dot_plt.plot(t, phis3_dot)
    phi3_dot_plt.set_ylabel(r'$\dot \varphi_3$', rotation=0)

    phi3_dot_plt.set_xlabel('time (s)')

    plt.show()


dt = 1 / 60
print(dt)

if __name__ == '__main__':

    pendulum1 = InitState(0.01, 0, 1)
    pendulum2 = InitState(0.01, 0, 1)
    pendulum3 = InitState(0.01, 0, 1)

    pends = ConnectedPendulums(dt, pendulum1, pendulum2, pendulum3)

    show_plots(pends)
