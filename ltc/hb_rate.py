# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import MultiCursor
import kpi_index as kpi
import talib as ta


# dataFrame
df = pd.read_csv('./hb_data_1min.csv', sep=',', index_col=0)

#plt.plot(df['high'].values,'r-', label='high')
#plt.plot(df['low'].values,'k-', label='low')
#plt.plot(df['high'].values-df['low'].values,'g-', label='dif')

plt.plot(df['close'].values,'r-', label='close')
plt.show()