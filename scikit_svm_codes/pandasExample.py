import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

s = pd.Series([1,3,5,np.nan,6,8])
print s

dates = pd.date_range('20130101', periods=6)
df = pd.DataFrame(np.random.randn(6,4), index=dates, columns=list('ABCD'))
print df

print "head",df.head()
print "tail",df.tail(2)
print "index",df.values,df.index,df.columns
print "count:",df.describe(),df.T

print "data:",df.loc(dates[0])
print "slicing",df.loc['20130102':'20130104',['A','B']]

print "selection by posion"
print df.iloc[3]

ts = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))
ts = ts.cumsum()
ts.plot()
plt.show()


df = pd.DataFrame(np.random.randn(1000, 4), index=ts.index, columns=['A', 'B', 'C', 'D'])
df = df.cumsum()
plt.figure(); df.plot(); plt.legend(loc='best')
plt.show()
