# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 20:19:35 2020

@author: HL
"""

import networkx as nx
import pandas as pd
#from networkx.algorithms.community import greedy_modularity_communities

# import plotting library
#%matplotlib inline
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
plt.rcParams['figure.figsize'] = [12.0, 8.0]
import datetime as dt

import statistics
import seaborn as sns
import collections


#%%  2.Import the data 
mtgox15 = pd.read_csv("D:/Desktop/Bitcoin network/MtGox15+.csv")
mtgoxFull = pd.read_csv("D:/Desktop/Bitcoin network/MtGoxFull.csv")
mtgoxFull = mtgoxFull.set_index ('timestamp', drop = True)
# mtgox15.timestamp = mtgox15.timestamp.astype(str)
# print (mtgox15.timestamp.dtype)
mtgox15['timestamp'] = pd.to_datetime(mtgox15['timestamp'], unit='s')
mtgox15 = mtgox15.set_index ('timestamp', drop = True)

#%% Data Description

mtgoxFull.value.describe()

# generate activeactor list
# mtgox15000 = mtgox15[mtgoxvalue['value']>15000]
mtgox10000 = mtgox15[mtgox15['value']>10000]


activeactor =list(set( mtgox10000['target'].tolist()))

for i in mtgox10000['source']:
    if i not in activeactor:
        activeactor.append(i)
#%%


mtgoxflow1 = mtgoxFull[mtgoxFull['source'].isin(activeactor)]
mtgoxflow2 = mtgoxFull[mtgoxFull['target'].isin(activeactor)]
mtgoxflowfull = [mtgoxflow1,mtgoxflow2]
mtgoxflowfull = pd.concat(mtgoxflowfull,join= 'inner')

mtgoxflowfull.to_csv('D:/Desktop/Bitcoin network/behavoir_activeactors.csv',index = False, header = True)

mtgoxflow1 = mtgox15[mtgox15['source'].isin(activeactor)]
mtgoxflow2 = mtgox15[mtgox15['target'].isin(activeactor)]
mtgoxflow = [mtgoxflow1,mtgoxflow2]
mtgoxflow = pd.concat(mtgoxflow,join= 'inner')

# mtgoxvalue= mtgoxflow.loc[:,'value']
# mtgox15['source']=mtgox15['source'].where(activeactor)


#%%

time_interval='15Min'
tota=mtgoxFull.resample(time_interval).sum()
mtgoxFull.valueDoll.plot()

        
#%%       
mtgoxvalue= mtgox15.loc[:,['timestamp', 'value']]
mtgoxvalue= mtgoxvalue.set_index ('timestamp', drop = True)
mtgoxvalue1 = mtgoxvalue[mtgoxvalue['value']>100]

#mtgoxvalue.plot
mtgoxvalue1.plot(kind = 'line')

#%%
