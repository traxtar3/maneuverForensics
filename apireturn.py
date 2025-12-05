# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from pprint import pprint
from space_track_api import SpaceTrackApi

import os


# scc = '25544'
# TLE file, no empty lines
# filename = 'TLEs/25544.txt'
print("WORKING")

# graph_satdic(convertTLE(filename))


# https://www.space-track.org/basicspacedata/query/class/tle/NORAD_CAT_ID/35491/orderby/EPOCH%20asc/limit/1000/format/tle/emptyresult/show
# https://www.space-track.org/basicspacedata/query/class/tle/NORAD_CAT_ID/[SATCAT#]/orderby/EPOCH%20asc/limit/[number of samples]/format/tle/emptyresublt/show


import requests


def useapi(scc, credential, start, stop, filename):
    with SpaceTrackApi(login=credential[0], password=credential[1]) as api:
        # tle_list = api.tle(EPOCH='>now-3',
        # epstr = '>' + start + ', <' + stop
        # print(epstr)
        epstr = start + '--' + stop
        tle_list = api.tle(EPOCH=epstr,
                           OBJECT_NUMBER=(scc),
                           order_by=('EPOCH asc'))
 # >2008-01-18,<2009-02-10/OBJECT_NUMBER/25544/orderby/EPOCH asc/format/tle/emptyresult/show
        # format=('TLE_LINE0'))
        # predicate=('EPOCH', 'NORAD_CAT_ID', 'TLE_LINE0', 'TLE_LINE1', 'TLE_LINE2',))

        # pprint(tle_list, indent=2)
        # file = open("temp.txt", "w")
        with open(filename, mode='w') as file:
            for x in tle_list:
                pants = x
                # pants = tle_list[1]
                xf = pants.get("TLE_LINE1")
                yf = pants.get("TLE_LINE2")
                file.write(xf)
                file.write("\n")
                file.write(yf)
                file.write("\n")
        if os.stat(filename).st_size == 0:
            print("TLEs were not returned for ", scc)
        else:
            print("TLEs returned for ", scc)
            # out = (xf, yf)
            # print(out)
        # return (out)
        # file.close
        # print(out)
        # print(yf)


# credential = ('traxtar3@gmail.com', '1qaz!QAZ1qaz!QAZ')
# scc = '25544'
# start = "2016-01-01"
# stop = "2018-01-17"

# useapi(scc, credential, start, stop)
# count = (len(open("temp1.txt").readlines())) / 2
# print("TLE Count:", count)


#     # print(getTLE(25544, 'tle.txt'))

#     credential = ('traxtar3@gmail.com', '1qaz!QAZ1qaz!QAZ')
#     scc = '25544'
#     start = "2016-01-01"
#     stop = "2018-01-17"

#     useapi(scc, credential, start, stop)
#     count = (len(open("temp1.txt").readlines())) / 2
#     print("TLE Count:", count)


if __name__ == '__main__':
    from pw import username, password
    credential = (username, password)
    scc = '25556'
    start = '2017-01-01'
    stop = '2019-12-31'
    filename = 'TLEs/' + scc + '.txt'
    useapi(scc, credential, start, stop, filename)
    count = (len(open(filename).readlines())) / 2
    print("TLE Count:", count)
