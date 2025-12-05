
from apireturn import useapi
from forensics_pd import forensics, convertTLE
import matplotlib.pyplot as plt
import os
import datetime
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
import numpy as np
register_matplotlib_converters()
from pw import username, password
xm = datetime.datetime.now()
print(xm)
credential = (username, password)
scc1 = '25544'
scc2 = '27880'
start = '2018-01-01'
stop = '2019-01-10'

toplot = 'back1'

# filename = 'TLEs/' + scc1 + '.txt'
# useapi(scc1, credential, start, stop, filename)
# filename2 = 'TLEs/' + scc2 + '.txt'
# useapi(scc2, credential, start, stop, filename2)

esvlist = [27880, 25544]
appended_data = []
for esv in esvlist:
    filename = 'TLEs/' + str(esv) + '.txt'
    useapi(esv, credential, start, stop, filename)

    if os.stat(filename).st_size == 0:
        print("Exited, no TLEs found")

    else:
        # appended_data = []
        # appended_data = pd.DataFrame(columns=['scc', 'time', 'back3', 'back2', 'back1', 'middle', 'fwd1', 'fwd2', 'fwd3'])

        run = forensics(convertTLE(filename), esv)
        # run.loc[:, 'scc'] = run.scc.astype(np.int)
        appended_data.append(run)
        print(appended_data)
appended_data = pd.DataFrame(appended_data)
sns.scatterplot(x=appended_data.time, y=toplot, data=appended_data, size=1)
plt.show()


# final_data = pd.concat(appended_data)
# data = appended_data
# print(data)
# toplot = data.columns
# print(toplot)

# g = sns.scatterplot(x='time', y=toplot, data=appended_data, size=1)


final_data = pd.concat(appended_data)
print(final_data)

# plts = sns.scatterplot(x='time', y=toplot, data=final_data, size=1)
# plts = sns.scatterplot(x='time', y=toplot, data=data, label=esv, size=1)
# g = sns.scatterplot(x='time', y=toplot, data=final_data, hue='scc', size=1)
final_data.loc[:, 'scc'] = final_data.scc.astype(np.int)

esvs = final_data.scc.unique()
print(list(esvs))
# esvs = final_data.scc.values()
# print(esvs)

# g = sns.scatterplot(x='time', y=toplot, data=final_data, size=1, palette="Set2")

start = datetime.datetime.strptime(start, '%Y-%m-%d')
stop = datetime.datetime.strptime(stop, '%Y-%m-%d')
sns.set_style("whitegrid")

g = (g.set(xlim=(start, stop)))
# plt.title("title")
plt.show()

# if os.stat(filename).st_size == 0:
#     print("Exited, no TLEs found")

# else:
#     # forensics(convertTLE(filename))
#     # plt.subplots_adjust(bottom=0.15)
#     # plt.margins(0.2)
#     # count = (len(open(filename).readlines())) / 2
#     # print("TLE Count:", count)
#     # y = datetime.datetime.now()
#     # print(y)
#     # t = y - xm
#     # print(t)
#     # plt.plot(g, c='b', marker='o', markersize=1)b
#     # plt.title(scc)
#     # plt.show()
#     # filename = 'temp.txt'
#     # scc = 25544
#     appended_data = []
#     appended_data.append(forensics(convertTLE(filename), scc1))
#     final_data = pd.concat(appended_data)
#     df = final_data
#     # df.plot.line(x='time', y='middle', c='blue')
#     df1 = df

#     appended_data = []
#     appended_data.append(forensics(convertTLE(filename2), scc2))
#     final_data = pd.concat(appended_data)
#     df = final_data
#     # df.plot.line(x='time', y='middle', c='red')
#     df2 = df

#     # print(df1.describe())
#     # print(df1.info())

#     # df_both = df1.merge(df2, left_on='scc')

#     # print(df_both.describe())
#     # print(df_both.info())

#     # df1['Key'] = 'time'
#     # df2['Key'] = 'time'

#     # DF = pd.concat([df1, df2], keys=['time', 'time'])
#     # DF = pd.concat([df1, df2])

#     # DFGroup = DF.groupby(['Key', 'middle'])

#     # DFGPlot = DFGroup.plot(kind='line')

#     # sns.relplot(x="time", y="middle", data=df)
#     start = datetime.datetime.strptime(start, '%Y-%m-%d')
#     stop = datetime.datetime.strptime(stop, '%Y-%m-%d')
#     sns.set_style("whitegrid")
#     plt1 = sns.scatterplot(x='time', y=toplot, data=df1, label=scc1, size=1)
#     plt2 = sns.scatterplot(x='time', y=toplot, data=df1, label=scc2, size=1)

#     g = sns.scatterplot(x='time', y=toplot, data=df2, label=scc2, size=1)
#     g = (g.set(xlim=(start, stop)))
#     # plt.title("title")
#     plt.show()

# # print(df1.head())


# # if __name__ == '__main__':
# # print(getTLE(25544, 'tle.txt'))

#     # sns.scatterplot(x='time',
#     #                 y='middle',
#     #                 # hue='scc',
#     #                 data=df2
#     #                 )

#     # start = datetime(*start)
#     # stop = datetime(*stop)
#     # sns.plt.xlim(start, stop)
#     # g = (g.set_axis_labels("Tip","Total bill(USD)").set(xlim=(0,15))))
#     # plt.show()

#     # tips = sns.load_dataset("df2")
