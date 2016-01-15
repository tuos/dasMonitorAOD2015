import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

nJob, days, runningSite = np.loadtxt("condorjobnumberscsv.csv", delimiter=",", unpack=True,
        converters={ 1: mdates.strpdate2num('%d-%b-%y %H:%M:%S')}, dtype=np.str)

fig = plt.figure(figsize=(15,10))
plt.plot_date(x=days, y=nJob, fmt="r", marker='o', markersize=20, linestyle='-', color='r', linewidth=5.0, label='Running jobs @ T0_CH_CERN')
plt.legend(loc='upper left', numpoints = 1, fontsize=40)
plt.title("Running jobs @ T0_CH_CERN", fontsize=20)
plt.ylabel("Running jobs", fontsize=25)
ax = fig.add_subplot(111)
#plt.text(0.5, 0.2, 'Total Volume in RAW data = 1450.06 TB', ha='center', va='center', transform=ax.transAxes, fontsize=30)
ax.tick_params(axis='x', labelsize=25)
ax.tick_params(axis='y', labelsize=25)
plt.grid(True)
plt.ylim(0, 3000)
fig.autofmt_xdate()
#plt.xlim([datetime.date(2015, 12, 24), datetime.datetime.now() + datetime.timedelta(days=1)])
fig.savefig('figJob.png')



