# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import AutoDateLocator, DateFormatter
from datetime import datetime

df=pd.DataFrame(columns=['date','name'],index=np.arange(0,2,1));
df['date'][0]='2017-09-01';
df['name'][0]=100;
df['date'][1]='2016-03-01';
df['name'][1]=200;

df=df.set_index('date')
print df.index.values,df.values;

fig=plt.figure()
ax1 = fig.add_subplot(1,1,1)
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
#ax1.xaxis.set_major_locator(mdate.DayLocator())
xs = [datetime.strptime(d, '%Y-%m-%d').date() for d in df.index.values]
print xs
# 配置横坐标
#plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
ax1.xaxis.set_major_locator(AutoDateLocator())
ax1.plot(xs,df['name'].values,'gs-',label=u'中文')
ax1.set_xticks(xs);

ax1.legend();
plt.gcf().autofmt_xdate()
plt.show();