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
plt.ylabel("PbPb AOD Volume (TB)", fontsize=25)
#plt.xlabel("", fontsize=20)
ax = fig.add_subplot(111)
plt.text(0.5, 0.2, 'Total Volume in RAW data = 1450.06 TB', ha='center', va='center', transform=ax.transAxes, fontsize=30)
ax.tick_params(axis='x', labelsize=25)
ax.tick_params(axis='y', labelsize=25)
plt.grid(True)
plt.ylim(0, 800)
fig.autofmt_xdate()
plt.xlim([datetime.date(2015, 12, 24), datetime.datetime.now() + datetime.timedelta(days=1)])
fig.savefig('figVolume.png')


fig2 = plt.figure(figsize=(15,10))
plt.plot_date(x=days, y=evtSize, fmt="r-", marker='o', markersize=20, linestyle='-', color='r', linewidth=5.0, label='Number of event (M) vs. Time')
plt.legend(loc='upper left', numpoints = 1, fontsize=40)
plt.title("Total number of event vs. Time, figure made @ "+str(datetime.datetime.now())+" CST", fontsize=20)
plt.ylabel("Total number of event (M)", fontsize=25)
ax2 = fig2.add_subplot(111)
plt.text(0.5, 0.2, 'Total event in RAW data = 1122.18 M', ha='center', va='center', transform=ax2.transAxes, fontsize=30)
ax2.tick_params(axis='x', labelsize=25)
ax2.tick_params(axis='y', labelsize=25)
plt.grid(True)
plt.ylim(0, 1400)
fig2.autofmt_xdate()
plt.xlim([datetime.date(2015, 12, 24), datetime.datetime.now() + datetime.timedelta(days=1)])
fig2.savefig('figEvent.png')

fig3 = plt.figure(figsize=(15,10))
plt.plot_date(x=days, y=lumiSize, fmt="r-", marker='o', markersize=20, linestyle='-', color='r', linewidth=5.0, label='Total number of lumi vs. Time')
plt.legend(loc='upper left', numpoints = 1, fontsize=40)
plt.title("Total number of lumi vs. Time, figure made @ "+str(datetime.datetime.now())+" CST", fontsize=20)
plt.ylabel("Number of lumi section", fontsize=25)
ax3 = fig3.add_subplot(111)
plt.text(0.5, 0.2, 'Total Lumi Section in RAW data = 512,222', ha='center', va='center', transform=ax3.transAxes, fontsize=30)
ax3.tick_params(axis='x', labelsize=25)
ax3.tick_params(axis='y', labelsize=25)
plt.grid(True)
plt.ylim(0, 7e5)
fig3.autofmt_xdate()
plt.xlim([datetime.date(2015, 12, 24), datetime.datetime.now() + datetime.timedelta(days=1)])
fig3.savefig('figLumi.png')

fig4 = plt.figure(figsize=(15,10))
plt.plot_date(x=days, y=fileSize, fmt="r-", marker='o', markersize=20, linestyle='-', color='r', linewidth=5.0, label='Number of AOD file vs. Time')
plt.legend(loc='upper left', numpoints = 1, fontsize=40)
plt.title("Total number of file vs. Time, figure made @ "+str(datetime.datetime.now())+" CST", fontsize=20)
plt.ylabel("Number of AOD file", fontsize=25)
ax4 = fig4.add_subplot(111)
ax4.tick_params(axis='x', labelsize=25)
ax4.tick_params(axis='y', labelsize=25)
plt.grid(True)
plt.ylim(0, 2.5e5)
fig4.autofmt_xdate()
plt.xlim([datetime.date(2015, 12, 24), datetime.datetime.now() + datetime.timedelta(days=1)])
fig4.savefig('figFile.png')

# adding transferred volume at vandy to the next plot
with open("vandySize.txt") as f:
    lines = f.readlines()
    last_row = lines[-1]
sizeAtVandy=last_row[1:8]
# adding plot for finished events in percent
fig5 = plt.figure(figsize=(15,10))
plt.plot_date(x=days, y=evtSize*100/1122.18, fmt="r-", marker='o', markersize=20, linestyle='-', color='r', linewidth=5.0, label='nEvent in percent vs. Time')
plt.legend(loc='upper left', numpoints = 1, fontsize=40)
plt.title("nEvent in percent vs. Time, figure made @ "+str(datetime.datetime.now())+" CST", fontsize=20)
plt.ylabel("(Total AOD event)/(Total RAW event) (%)", fontsize=25)
ax5 = fig5.add_subplot(111)
plt.text(0.38, 0.75, '(Total AOD event)/(Total RAW event)', ha='center', va='center', transform=ax5.transAxes, fontsize=30)
latestAODEvt="Latest total AOD event = "+str('{:.2f}'.format(round(float(evtSize[-1]), 2)))+" M"
plt.text(0.34, 0.635, latestAODEvt, ha='center', va='center', transform=ax5.transAxes, fontsize=26)
plt.text(0.29, 0.575, 'Total RAW event = 1122.18 M', ha='center', va='center', transform=ax5.transAxes, fontsize=26)
plt.text(0.99, evtSize[-1]/1122.18/1.2, '-----', ha='center', va='center', transform=ax5.transAxes, fontsize=30)
latestRatio=str('{:.1f}'.format(round(float(evtSize[-1]*100/1122.18), 1)))+"%"
plt.text(1.076, evtSize[-1]/1122.18/1.2, latestRatio, ha='center', va='center', transform=ax5.transAxes, fontsize=30)
ax5.tick_params(axis='x', labelsize=25)
ax5.tick_params(axis='y', labelsize=25)
roundVandy='{:.3f}'.format(round(float(sizeAtVandy), 3))
volumeInVandy="Latest volume in Vandy = "+str(roundVandy)+" TB"
roundDAS='{:.3f}'.format(round(float(volumeSize[-1]), 3))
volumeInDAS="Latest volume in  DAS   = "+str(roundDAS)+" TB"
ratioVandyDAS=float(sizeAtVandy)*100/volumeSize[-1]
roundRatio='{:.2f}'.format(round(float(ratioVandyDAS), 2))
vandyOverDAS="(Vandy volume)/(DAS volume) = "+str(roundRatio)+"%"
plt.text(0.59, 0.26, volumeInVandy, ha='center', va='center', transform=ax5.transAxes, fontsize=30, color='b')
plt.text(0.59, 0.19, volumeInDAS, ha='center', va='center', transform=ax5.transAxes, fontsize=30, color='b')
plt.text(0.495, 0.11, vandyOverDAS, ha='center', va='center', transform=ax5.transAxes, fontsize=30, color='b')
plt.text(0.135, 0.23, 'Transfer:', ha='center', va='center', transform=ax5.transAxes, fontsize=30, color='b', fontweight='bold')
plt.grid(True)
plt.ylim(0, 120)
fig5.autofmt_xdate()
plt.xlim([datetime.date(2015, 12, 24), datetime.datetime.now() + datetime.timedelta(days=1)])
fig5.savefig('figEventInPercent.png')

