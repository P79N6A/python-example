import pandas as pd;
import numpy as np;
import datetime;

data=[[1,2,3],[4,5,6],[3,2,1],[3,7,1],[0,2,9]]

df=pd.DataFrame(data,columns={'A','B','C'})
df['D']=88;


print(df)
df2 = df.reindex([2,1,3],fill_value=0)
print(df2)

df2=df2.sort_index()
print(df2)

df2=df2.sort_index(axis=1)
print(df2)

df2=df2.sort_values(by=['A'],ascending=True)
print(df2)
print(df2['A'].isin([1,2,3]))
df=(df2.query(" A>5.0 & (B>3.5 | C<2) "))
print(df)
print('=====')
df2=df2.sort_index()
print(df2)

print(df2.loc[[1,3],['A','B']])

df1 = pd.DataFrame({'key': ['a', 'b', 'b'], 'data1': range(3)})
df2 = pd.DataFrame({'key': ['a', 'b', 'c'], 'data2': range(3)})
print('==df1=')
print(df1)
print('==df2=')
print(df2)
print('==merge=')
print(pd.merge(df1,df2));
print('==join===')
print(df1.join(df2,lsuffix='x',rsuffix='y'));
print('==concat===')
print(pd.concat([df1,df2],ignore_index=True,sort=True));

ds=pd.Series(['a','o','b','c','e','g'])
print(ds[ds>'b']);


## read
data=[['2015',1,2,3],['2016',4,5,6],['2017',3,2,1],['2018',3,7,9],['2019',0,2,9]]
df=pd.DataFrame({'date':['2015','2016','2017','2018','2019'],'A':[2,3,2,1,4]})
print(df)
df.sort_values(by=['date'],inplace=True);
print(df)
print(df['A'].rank(method='average'))
print(df['A'].rank(method='first')[0])
print(df['A'].shape[0])
df=df['A']
print(df.shape);
print(df.drop_duplicates().rank());

#print(int(df.shape[0]/10))


#df.set_index(['A'],inplace=True)
#print(df)

#df.index=np.arange(0,df.shape[0],1)
#print(df)
print(list(range(2,8,1)))

df=pd.DataFrame([[2,3],[5,3]],columns=['a','b']);
print(df)
new_df=df[df['a']>2];
print(new_df)
print(df)

a=df[df['a']==5].index.values;
print(a[0])
print(len(a)==1)

now=datetime.datetime.now()
print(now.strftime('%Y-%m-%d'))

start=datetime.datetime.strptime('2018-10-01','%Y-%m-%d');
ds=(now-start).days;

while(ds>=0):
    start_str = start.strftime('%Y-%m-%d')
    print(start_str);
    start=start+datetime.timedelta(days=1);
    ds=(now-start).days;


df=pd.DataFrame([[2,4],[5,3]],columns=['a','b']);
print(df.loc[df.shape[0]-1,'b'])
print(df)
print(df[df['b']==4].index.values[0])
print('000-----')
print(df.loc[0:0,'a'])
df.loc[0,'a']=9;
print(df)
df=pd.DataFrame();
print(df.empty)

x=map(lambda x:not x,[True,False])
print(list(x))
