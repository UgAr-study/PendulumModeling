""" Draw the connected pendulum """
from __future__ import division

import numpy as np
import matplotlib.pyplot as plt
from draw import Point, Draw
from connected_pendulums import ConnectedPendulums
import pygame as pg 
import math

fps = 60

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

def main():
    """ Run the program """
    phi1 = float(input('phi1 (degrees): '))
    phi2 = float(input('phi2 (degrees): '))
    phi3 = float(input('phi3 (degrees): '))

    #phi_dots input also

    phi1 *= math.pi / 180
    phi2 *= math.pi / 180
    phi3 *= math.pi / 180

    m1 = float(input('Mass 1 (kg): '))
    m2 = float(input('Mass 2 (kg): '))
    m3 = float(input('Mass 3 (kg): '))

    l = float(input('Length (m): '))
    betta = float(input('betta : '))

    dt = 1 / fps

    pendulums = ConnectedPendulums(dt, phi1, phi2, phi3, m1=m1, m2=m2, m3=m3, l=l, betta=betta)

    scale = height / 2
    screen = pg.display.set_mode((width, height))
    canvas = Draw(screen, width / 2, height / 5)
    
    pg.init()
    clk = pg.time.Clock()
    end = False

    phis1, phis2, phis3 = [phi1], [phi2], [phi3]

    t = [0.0]

    while not end:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                end = True
        screen.fill(white)
        
        phis = pendulums.get_next_state().reshape((3,))

        phis1.append(phis[0])
        phis2.append(phis[1])
        phis3.append(phis[2])

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
        clk.tick(fps)

    phis1 = np.array(phis1)
    phis2 = np.array(phis2)
    phis3 = np.array(phis3)

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
    fig.suptitle('Phi(t)')

    ax1.plot(t, phis1)
    ax1.set_ylabel('phi1')

    ax2.plot(t, phis2)
    ax2.set_ylabel('phi2')

    ax3.plot(t, phis3)
    ax3.set_ylabel('phi3')
    ax3.set_xlabel('time (s)')

    plt.show()

if __name__ == '__main__':
    main()
