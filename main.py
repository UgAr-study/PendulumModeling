import argparse
import math
from connected_pendulums import ConnectedPendulums
from connected_pendulums import InitState
from render import start_modeling
from connected_pendulums import show_plots

fps = 60

if __name__ == '__main__':
    """ Run the program """

    parser = argparse.ArgumentParser()

    parser.add_argument('-plt', action='store_const', const=True,
                        help='show plots only')

    parser.add_argument('-t', type=float, default=None,
                        help='duration in seconds')

    args = parser.parse_args()

    if args.plt and args.t is None:
        parser.error('you must specify the duration for showing only the plots')

    phi1 = float(input('phi1 (degrees): '))
    phi1_dot = float(input('phi1_dot (degrees/sec): '))
    phi2 = float(input('phi2 (degrees): '))
    phi2_dot = float(input('phi2_dot (degrees/sec): '))
    phi3 = float(input('phi3 (degrees): '))
    phi3_dot = float(input('phi3_dot (degrees/sec): '))

    phi1 *= math.pi / 180
    phi2 *= math.pi / 180
    phi3 *= math.pi / 180

    phi1_dot *= math.pi / 180
    phi2_dot *= math.pi / 180
    phi3_dot *= math.pi / 180

    m1 = float(input('Mass 1 (kg): '))
    m2 = float(input('Mass 2 (kg): '))
    m3 = float(input('Mass 3 (kg): '))

    pendulum1 = InitState(phi1, phi1_dot, m1)
    pendulum2 = InitState(phi2, phi2_dot, m2)
    pendulum3 = InitState(phi3, phi3_dot, m3)

    k1 = float(input('k1 (N/kg): '))
    k2 = float(input('k2 (N/kg): '))

    l = float(input('Length (m): '))
    betta = float(input('betta : '))

    dt = 1 / fps

    pendulums = ConnectedPendulums(dt, pendulum1, pendulum2, pendulum3,
                                   k1=k1, k2=k2, l=l, betta=betta)

    if args.plt:
        show_plots(pendulums, args.t)
    else:
        start_modeling(pendulums)
