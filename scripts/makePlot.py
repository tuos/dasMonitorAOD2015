import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

days, volumeSize, evtSize, lumiSize, fileSize = np.loadtxt("volumeEventSize.txt", unpack=True,
        converters={ 0: mdates.strpdate2num('%m/%d/%Y-%H:%M')})

fig = plt.figure(figsize=(15,10))
plt.plot_date(x=days, y=volumeSize, fmt="r", marker='o', markersize=20, linestyle='-', color='r', linewidth=5.0, label='Volume in TB vs. Time')
plt.legend(loc='upper left', numpoints = 1, fontsize=40)
plt.title("Volume in TB vs. Time, figure made @ "+str(datetime.datetime.now())+" CST", fontsize=20)
plt.ylabel("PbPb AOD Volume (TB)", fontsize=20)
#plt.xlabel("", fontsize=20)
ax = fig.add_subplot(111)
plt.text(0.5, 0.2, 'Total Volume in RAW data = 1450.06 TB', ha='center', va='center', transform=ax.transAxes, fontsize=30)
plt.grid(True)
plt.ylim(0, 800)
fig.autofmt_xdate()
plt.xlim([datetime.date(2015, 12, 24), datetime.datetime.now() + datetime.timedelta(days=1)])
fig.savefig('figVolume.png')


fig2 = plt.figure(figsize=(15,10))
plt.plot_date(x=days, y=evtSize, fmt="r-", marker='o', markersize=20, linestyle='-', color='r', linewidth=5.0, label='Number of event (M) vs. Time')
plt.legend(loc='upper left', numpoints = 1, fontsize=40)
plt.title("Total number of event vs. Time, figure made @ "+str(datetime.datetime.now())+" CST", fontsize=20)
plt.ylabel("Total number of event (M)", fontsize=20)
ax2 = fig2.add_subplot(111)
plt.text(0.5, 0.2, 'Total event in RAW data = 1122.18 M', ha='center', va='center', transform=ax2.transAxes, fontsize=30)
plt.grid(True)
plt.ylim(0, 1200)
fig2.autofmt_xdate()
plt.xlim([datetime.date(2015, 12, 24), datetime.datetime.now() + datetime.timedelta(days=1)])
fig2.savefig('figEvent.png')

fig3 = plt.figure(figsize=(15,10))
plt.plot_date(x=days, y=lumiSize, fmt="r-", marker='o', markersize=20, linestyle='-', color='r', linewidth=5.0, label='Total number of lumi vs. Time')
plt.legend(loc='upper left', numpoints = 1, fontsize=40)
plt.title("Total number of lumi vs. Time, figure made @ "+str(datetime.datetime.now())+" CST", fontsize=20)
plt.ylabel("Number of lumi section", fontsize=20)
ax3 = fig3.add_subplot(111)
plt.text(0.5, 0.2, 'Total Lumi Section in RAW data = 512,222', ha='center', va='center', transform=ax3.transAxes, fontsize=30)
plt.grid(True)
plt.ylim(0, 7e5)
fig3.autofmt_xdate()
plt.xlim([datetime.date(2015, 12, 24), datetime.datetime.now() + datetime.timedelta(days=1)])
fig3.savefig('figLumi.png')

fig4 = plt.figure(figsize=(15,10))
plt.plot_date(x=days, y=fileSize, fmt="r-", marker='o', markersize=20, linestyle='-', color='r', linewidth=5.0, label='Number of AOD file vs. Time')
plt.legend(loc='upper left', numpoints = 1, fontsize=40)
plt.title("Total number of file vs. Time, figure made @ "+str(datetime.datetime.now())+" CST", fontsize=20)
plt.ylabel("Number of AOD file", fontsize=20)
plt.grid(True)
plt.ylim(0, 2.3e5)
fig4.autofmt_xdate()
plt.xlim([datetime.date(2015, 12, 24), datetime.datetime.now() + datetime.timedelta(days=1)])
fig4.savefig('figFile.png')


