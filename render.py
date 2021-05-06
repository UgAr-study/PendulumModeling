""" Draw the connected pendulum """
from __future__ import division

import numpy as np
import matplotlib.pyplot as plt
from draw import Point, Draw
from connected_pendulums import ConnectedPendulums
from connected_pendulums import InitState
import pygame as pg
import math


red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
dark_blue = (0, 0, 128)
white = (255, 255, 255)
black = (0, 0, 0)
pink = (255, 200, 200)
grey = (84, 84, 84)

width = 800
height = 600

pend_indent = width / 3
p11 = Point(-pend_indent, 0)
p21 = Point(0, 0)
p31 = Point(pend_indent, 0)

susp_indent = Point(-width / 50, height / 50)
lta_susp = p11 + susp_indent
susp_width = (p31 - p11 - susp_indent * 2)()[0]
susp_height = (lta_susp - p11)()[1]

pend_radius = 10


def start_modeling(pendulums: ConnectedPendulums):
    """ Show animation and plots """
    phis, phis_dot = pendulums.get_current_state()

    phis.reshape((3,))
    phis_dot.reshape((3,))

    phis1, phis2, phis3 = [phis[0]], [phis[1]], [phis[2]]
    phis1_dot, phis2_dot, phis3_dot = [phis_dot[0]], [phis_dot[1]], [phis_dot[2]]

    dt = pendulums.get_timestep()
    t = [0.0]

    scale = height / 2
    screen = pg.display.set_mode((width, height))
    canvas = Draw(screen, width / 2, height / 5)

    pg.init()
    clk = pg.time.Clock()

    end = False

    while not end:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                end = True

        screen.fill(white)

        phis, phis_dot = pendulums.get_next_state()
        phis.reshape((3,))
        phis_dot.reshape((3,))

        phis1.append(phis[0])
        phis2.append(phis[1])
        phis3.append(phis[2])

        phis1_dot.append(phis_dot[0])
        phis2_dot.append(phis_dot[1])
        phis3_dot.append(phis_dot[2])

        t.append(t[-1] + dt)

        p12 = p11 + Point(math.sin(phis[0]) * scale, -math.cos(phis[0]) * scale)
        p22 = p21 + Point(math.sin(phis[1]) * scale, -math.cos(phis[1]) * scale)
        p32 = p31 + Point(math.sin(phis[2]) * scale, -math.cos(phis[2]) * scale)

        canvas.draw_rectangle(grey, lta_susp, susp_width, susp_height)

        canvas.draw_line(green, (p12 + p11) / 2, (p22 + p21) / 2)
        canvas.draw_line(green, (p22 + p21) / 2, (p32 + p31) / 2)

        canvas.draw_line(black, p11, p12)
        canvas.draw_line(black, p21, p22)
        canvas.draw_line(black, p31, p32)

        canvas.draw_circle(red, p12, pend_radius, 0)
        canvas.draw_circle(red, p22, pend_radius, 0)
        canvas.draw_circle(red, p32, pend_radius, 0)

        pg.display.update()
        clk.tick(1 / dt)

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


if __name__ == '__main__':

    pendulum1 = InitState(0.1, 0, 1)
    pendulum2 = InitState(0.1, 0, 1)
    pendulum3 = InitState(0.1, 0, 1)

    pends = ConnectedPendulums(dt, pendulum1, pendulum2, pendulum3)

    start_modeling(pends)
