
from apireturn import useapi
from forensics_pd import forensics, convertTLE
import matplotlib.pyplot as plt
import os
import datetime
import pandas as pd
import seaborn as sns
from ratelimiter import RateLimiter
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from pw import username, password
xm = datetime.datetime.now()
print(xm)
credential = (username, password)


ymaxl = []
yminl = []
sns.set_style("whitegrid")


def scc_grapher(scc, start, stop, toplot):

    filename = 'TLEs/' + scc + '.txt'
    useapi(scc, credential, start, stop, filename)
    if os.stat(filename).st_size == 0:
        print("Exited, no TLEs found")
        exit()

    else:

        appended_data = []
        appended_data.append(forensics(convertTLE(filename), scc))
        final_data = pd.concat(appended_data)
        df = final_data

        plt1 = sns.scatterplot(x='time', y=toplot, data=df, label=scc, marker='.')

        ymin = final_data[toplot].min()
        ymax = final_data[toplot].max()
        yavg = final_data[toplot].mean()

        if ymax > (yavg * 10):
            ymax = yavg * 7
        else:
            ymax = ymax

        ymaxl.append(ymax)

        ymin = yavg * -0.15
        yminl.append(ymin)

    start = datetime.datetime.strptime(start, '%Y-%m-%d')
    stop = datetime.datetime.strptime(stop, '%Y-%m-%d')
    plt1 = (plt1.set(xlim=(start, stop), ylim=(ymin, ymax)))
    # plt1 = (plt1.set(xlim=(start, stop)))


if __name__ == '__main__':

    sccsx = ['25544']
    sccsx = ['19548', '21639', '22314', '23613', '38860', '38997', '39013', '39084']
    sccsx = ['26880']  # DSP21
    sccsx = ['28158']  # DSP22
    sccsx = ['37481', '39120', '43162', '41937']  # SBIRS GEO
    sccsx = ['42934']
    sccsx = ['00634', '00858', '01317', '02608', '02639', '02717', '02969', '03029', '03431', '03691', '04250', '04353', '04376', '04902', '05587', '05588', '05709', '05775', '06052', '06437', '07229', '07250', '07324', '07392']
    sccsx = ['07392', '07466', '07544', '07547', '07578', '07790', '08132', '08330', '08357', '08366', '08476', '08513', '08585', '08620', '08746', '08747', '08808', '08838', '09009', '09047', '09416', '09503', '09852', '09862', '10159', '10294', '10365', '10489', '10557']

    sccs = ['12003', '05398', '01520']
    sccs = ['05398', '01520', '01512']
    sccs = ['05398']

    start = '2017-01-01'
    stop = '2019-06-10'
    toplot = 'middle'

    rate_limiter = RateLimiter(max_calls=1, period=10)
    rate_limiter = RateLimiter(max_calls=10000000, period=10)

    if type(sccs) is not list:
        scc_grapher(sccs, start, stop, toplot)
        # print('1')
    else:
        for scc in sccs:
            # print(scc)
            with rate_limiter:
                print("Starting " + scc)
                scc_grapher(scc, start, stop, toplot)

    plt.show()
