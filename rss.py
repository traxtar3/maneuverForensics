from numpy import dot, linalg, arange, copy, char
from math import pi, sqrt, floor, pow
from math import fabs as abs
import matplotlib.pyplot as plt
import csv
import re

from itertools import islice


def twobody2(sat1, sat2):
    # sat_x = "%02d" % sat1
    # sat_y = "%02d" % sat2
    # start = mydict[sat_x]
    stop = sat2
    # start = input_stuffs.sat1[sat_x]
    # stop = input_stuffs.sat1[sat_y]
    # starttime = start[0]
    # endtime = stop[0]
    # r_i = float(start[1].replace(" ", ""))
    # r_j = float(start[2].replace(" ", ""))
    # r_k = float(start[3].replace(" ", ""))
    # v_i = float(start[4].replace(" ", ""))
    # v_j = float(start[5].replace(" ", ""))
    # v_k = float(start[6].replace(" ", ""))
    # ri = [r_i, r_j, r_k]
    # vi = [v_i, v_j, v_k]
    # print(sat1)
    ri = [sat1[1], sat1[2], sat1[3]]
    vi = [sat1[4], sat1[5], sat1[6]]

    # print(ri)
    # print(vi)

    # t_start = datetime.datetime.strptime(starttime, "%b %d %Y %H:%M:%S.%f")
    # t_end = datetime.datetime.strptime(endtime, "%b %d %Y %H:%M:%S.%f")
    # tau = ((sat2[0] - sat1[0])/60)
    tau = ((sat2[0] - sat1[0]))

    mu = 398600.4415
    tolerance = 1e-12
    u = 0
    imax = 20
    orbits = 0
    tdesired = copy(tau)
    threshold = tolerance * abs(tdesired)
    r0 = linalg.norm(ri)
    n0 = dot(ri, vi)
    beta = 2 * (mu / r0) - dot(vi, vi)
    if (beta != 0):
        umax = + 1 / sqrt(abs(beta))
        umin = - 1 / sqrt(abs(beta))
    if (beta > 0):
        orbits = beta * tau - 2 * n0
        orbits = 1 + (orbits * sqrt(beta)) / (pi * mu)
        orbits = floor(orbits / 2)
    for i in arange(1, imax, 1).reshape(-1):
        q = beta * u * u
        q = q / (1 + q)
        n = 0
        r = 1
        l = 1
        s = 1
        d = 3
        gcf = 1
        k = - 5
        gold = 0

        while (gcf != gold):
            k = - k
            l = l + 2
            d = d + 4 * l
            n = n + (1 + k) * l
            r = d / (d - n * r * q)
            s = (r - 1) * s
            gold = copy(gcf)
            gcf = gold + s

        h0 = 1 - 2 * q
        h1 = 2 * u * (1 - q)
        u0 = 2 * h0 * h0 - 1
        u1 = 2 * h0 * h1
        u2 = 2 * h1 * h1
        u3 = 2 * h1 * u2 * gcf / 3

        if (orbits != 0):
            u3 = u3 + 2 * pi * orbits / (beta * sqrt(beta))

        r1 = r0 * u0 + n0 * u1 + mu * u2
        dt = r0 * u1 + n0 * u2 + mu * u3
        slope = 4 * r1 / (1 + beta * u * u)
        terror = tdesired - dt

        if (abs(terror) < threshold):
            break
        if ((i > 1) and (u == uold)):
            break
        if ((i > 1) and (dt == dtold)):
            break

        uold = copy(u)
        dtold = copy(dt)
        ustep = terror / slope

        if (ustep > 0):
            umin = copy(u)
            u = u + ustep
            if (u > umax):
                u = (umin + umax) / 2
        else:
            umax = copy(u)
            u = u + ustep
            if (u < umin):
                u = (umin + umax) / 2
        if (i == imax):
            print('\\n\\nmax iterations in twobody2 function')

    usaved = copy(u)
    f = 1.0 - (mu / r0) * u2
    gg = 1.0 - (mu / r1) * u2
    g = r0 * u1 + n0 * u2
    ff = - mu * u1 / (r0 * r1)

    # Had to re-arrange things to make it work
    for i in arange(1):  # .reshape(-1):
        posi = f * ri[i] + g * vi[i]
        veli = ff * ri[i] + gg * vi[i]
    for j in arange(2).reshape(-1):
        posj = f * ri[j] + g * vi[j]
        velj = ff * ri[j] + gg * vi[j]
    for k in arange(3).reshape(-1):
        posk = f * ri[k] + g * vi[k]
        velk = ff * ri[k] + gg * vi[k]

    # Make "pretty" output
    position = [posi, posj, posk]
    velocity = [veli, velj, velk]
    # print(position)
    # print(velocity)
    rss = sqrt((pow((position[0] - float(stop[1])), 2)) + (pow((position[1] - float(stop[2])), 2)) + (pow((position[2] - float(stop[3])), 2)))
    return rss
