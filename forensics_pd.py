__author__ = 'traxtar3'

from propagation import sgp4
from inout import twoline2rv
from earth_gravity import EarthGravity, wgs84
from rss import twobody2
from numpy import arange, average
from ext import invjday
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
scc = '25544'


def convertTLE(filename):
    # make and empty dictionary
    sat_dic = {}
    # declare "N" to be used later. Requried to properly read file
    N = 1
    # open file, read mode
    with open(filename, mode='r') as infile:
        for line in infile:
            # Need to read both lines of the TLE at a time
            line1 = line
            line2 = next(infile)
            # use Vallado's sgp4 code to input TLE and output r,v
            satout = sgp4(twoline2rv(line1, line2, wgs84), 0)
            # set up to convert to touple
            position = satout[0]
            velocity = satout[1]
            # convert jday at beginning of TLE to seconds
            jsec = (twoline2rv(line1, line2, wgs84)).jdsatepoch * 86400
            # convert vector to list
            vector = position[0], position[1], position[2], velocity[0], velocity[1], velocity[2]
            # create empty dictionary
            sat_dic.setdefault('x', [])
            # add vector to dictionary
            sat_dic.update({N: [jsec, position[0], position[1], position[2], velocity[0], velocity[1], velocity[2]]})
            # itterate N so it will moove to next line for next loop
            N = N + 1
    # remove first entry of dictionary that was created earlier
    sat_dic.pop('x')
    # ouput dictionary with satellite info
    # format:
    # {1: [time, r_i, r_j, r_k, v_i, v_j, v_k], 2: [time, r_i, r_j, r............
    # example:
    # {1: [211813453159.0004, -3094.1818207205138, 5207.334755689673, -3010.7542426581717, -3.32038458151474, -4.8315823003948895, -4.950156866283181], 2: [21181346......
    print("TLEs converted")
    return sat_dic


def forensics(sat_dic, scc):
    # make and empty dictionary
    # need to set the first entry to the 3rd entry so it can go back 3 days to compare
    begin = int(sorted(sat_dic.keys())[0]) + 3
    # need to set the last entry to the 3rd entry from the end so it can compare the last 3 days
    final = int(sorted(sat_dic.keys())[-1]) - 3
    df = pd.DataFrame(columns=['scc', 'time', 'back3', 'back2', 'back1', 'middle', 'fwd1', 'fwd2', 'fwd3'])

    for i in arange(begin, final, 1):
        # ref1 = i
        # convert j-day seconds to something timedate can understand
        ref0 = invjday(sat_dic[i][0] / 86400)
        ref0 = list(ref0)
        ref0[5] = int(ref0[5])
        ref0 = tuple(ref0)
        # convert ref0 to a datetime object
        ref2 = datetime(*ref0)
        # ref2 = (i - datetime(1970, 1, 1)).total_seconds()
        # ref1 = datetime(*i)

        # time is the x-axis values
        # x = ref2

        # this is the magic. RSS between 2 TLE entries...chronologically
        back3 = twobody2(sat_dic[i], sat_dic[i - 3])
        back2 = twobody2(sat_dic[i], sat_dic[i - 2])
        back1 = twobody2(sat_dic[i], sat_dic[i - 1])
        fwd1 = twobody2(sat_dic[i], sat_dic[i + 1])
        fwd2 = twobody2(sat_dic[i], sat_dic[i + 2])
        fwd3 = twobody2(sat_dic[i], sat_dic[i + 3])
        middle = (back1 + fwd1) / 2
        df = df.append({'scc': scc, 'time': ref2, 'back3': back3, 'back2': back2, 'back1': back1, 'middle': middle, 'fwd1': fwd1, 'fwd2': fwd2, 'fwd3': fwd3}, ignore_index=True)


        # print(df)
        # set RSS returns as a list
        # yval = [back3, back2, back1, middle, fwd1, fwd2, fwd3]
        # midthing = (back3 + fwd3) / 2
        # yval = [middle]
        # yval = (back3 + back2 + back1 + fwd1 + fwd2 + fwd3) / 6
        # yval = [back3, back2, back1, middle, fwd1, fwd2, fwd3]
        # yval = [back3, back2, back1, fwd1, fwd2, fwd3]
        # print(yval)
        # RSS list is the y-axis values
        # y = [yval]
        # print(df)
        # print(ref2)

        # plt.plot(x, y, c='b', marker='o', markersize=1)

        # set up the graph and add all the entries. This just keeps adding stuff until the for-loop is complete
    # print(type(i))
    print("Math complete")
    # finaldata = pd.concat()
    # print(df)
    return df


if __name__ == '__main__':

    filename = 'temp.txt'
    scc = 25544
    # forensics(convertTLE(filename))
    appended_data = []
    appended_data.append(forensics(convertTLE(filename), scc))
    final_data = pd.concat(appended_data)
    df = final_data
    df.plot.line(x='time', y='middle')
    # final_data = final_data.sort_values(by=['time'])
    # final_data.to_csv('test.csv', index=False)

    # x = df([2])
    # x = (final_data['time'], final_data['time'])  # , 'back2', 'back1', 'fwd1', 'fwd2', 'fwd3']
    # y = (final_data['back3'], final_data['back2'])  # , 'back2', 'back1', 'fwd1', 'fwd2', 'fwd3']

    # plt.plot(x, y, c='b', marker='o', markersize=1)
    # plt.subplots_adjust(bottom=0.15)
    # x = final_data['time'].values.tolist()
    # # back1 = final_data['back1']
    # back2 = final_data['back2']
    # y = (final_data['back3'], final_data['back2'], final_data['back1'], final_data['middle'], final_data['fwd1'], final_data['fwd2'], final_data['fwd3'])
    # # print(y)
    # # y = y.values.tolist()

    # back3 = final_data['back3']
    # back3 = back3.values.tolist()
    # back2 = final_data['back2']
    # back2 = back2.values.tolist()
    # y = [back3, back2]
    # y = [y]
    # print(final_data['time'])
    # x = final_data['time'].values.tolist()
    # print(final_data.columns)
    # final_data.plot('time', 'back2', kind='scatter')
    # plt.plot(df['time'].tolist(), df['back2'], c='b', marker='o', markersize=1)
    # y = back3.append(back2)
    # y = y.append(final_data['back2'].values.tolist())
    # print(y)

    # plt.plot(final_data['time'], final_data['back1'], c='b', marker='o', markersize=1)
    # plt.plot(final_data['time'], final_data['back2'], c='b', marker='o', markersize=1)
    # plt.plot(x, y, c='b', marker='o', markersize=1)

    # plt.plot(final_data['time'], y, c='b', marker='o', markersize=1)
    # plt.title(scc)
    plt.show()
