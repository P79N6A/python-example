import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import MultiCursor

x = np.arange(0., np.e, 0.1)
y1 = np.exp(-x)
y2 = np.log(x)

fig = plt.figure()

ax1 = fig.add_subplot(111)
ax1.plot(x, y1,'g>--',label='ax1-1')
ax1.plot(x, y1*0.1,'y*-',label='ax1-2')
ax1.set_ylabel('Y values for exp(-x)')
ax1.set_title("Double Y axis")
ax1.legend();

ax2 = ax1.twinx()  # this is the important function
ax2.plot(x, y2, 'r',label='ax2')
ax2.set_xlim([0, np.e])
ax2.set_ylabel('Y values for ln(x)')
ax2.set_xlabel('Same X for both exp(-x) and ln(x)')
ax2.legend();

multi = MultiCursor(fig.canvas, (ax1,ax2), color='g', horizOn=True, vertOn=True, lw=1)
plt.show()