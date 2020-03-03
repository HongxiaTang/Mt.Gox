#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2020

@author: Eric Vansteenberghe
Quantile regression on Engel 1857 data
We follow
Roger Koenker. Quantile regression. Journal of Economic Perspectives, 2001
Inspired by:
Engel, Ernst. 1857. “Die Produktions- und Konsumptionverhaltnisse des Konigreichs Sachsen.”
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import statsmodels.formula.api as smf # for OLS

# We set the working directory (useful to chose the folder where to export output files)
os.chdir('D:/espaceR')

ploton = True

#%% Engel 1857 data
# Import the data
dfengel = pd.read_csv('R_data/engel1857.csv')

# do a first scatter plot of the data
if ploton:
    dfengel.plot.scatter(x='income',y='foodexp')

# OLS
reg = smf.ols('foodexp ~ income',data = dfengel).fit()
reg.summary()

# Least Absolute Deviation (Median Regression)
LAD = smf.quantreg('foodexp ~ income',data = dfengel).fit(q=.5)
LAD.summary()


# plot the data
stepsize = 1
x = np.arange(0, 4000, stepsize)
if ploton:   
    dfengel.plot.scatter(x='income',y='foodexp')
    plt.xlabel('Income')
    plt.ylabel('Food expenditure')
    plt.plot(x, reg.params[0] + reg.params[1]*x ,'-')
    plt.plot(x, LAD.params[0] + LAD.params[1]*x ,'--')
    plt.close()

#quantiles = np.arange(0.1,1,0.1)
quantiles = [0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95]
dfquantile = pd.DataFrame(index=quantiles,columns=['alpha','t-stat alpha','beta','t-stat beta'])
models = [] 
params = []
for quantilei in quantiles:
    mod = smf.quantreg('foodexp ~ income',data = dfengel)
    res = mod.fit(q=quantilei)
    dfquantile.loc[quantilei,'alpha'] =res.params[0] 
    dfquantile.loc[quantilei,'t-stat alpha'] =res.tvalues[0]
    dfquantile.loc[quantilei,'beta'] =res.params[1] 
    dfquantile.loc[quantilei,'t-stat beta'] =res.tvalues[1]
    params.append([quantilei, res.params['Intercept'], res.params['income']] + res.conf_int().loc['income'].tolist())   

params = pd.DataFrame(data = params, columns = ['quantiles','intercept','x_coef','cf_lower_bound','cf_upper_bound'])
params['OLS_x_coef'] = reg.params['income']
params['OLS_cf_lower_bound'] = reg.conf_int().loc['income'][0]
params['OLS_cf_upper_bound'] = reg.conf_int().loc['income'][1]


# scatter plot and 0.1 and 0.9 quantiles
if ploton:
    plt.scatter(dfengel.income, dfengel.foodexp)
    for quantilei in quantiles:
        y_pred = dfquantile.loc[quantilei,'alpha'] + dfquantile.loc[quantilei,'beta'] * dfengel.income
        plt.plot(dfengel.income, y_pred,linewidth=1, label='Q Reg : '+str(quantilei))
    plt.xticks(())
    plt.yticks(())
    plt.xlabel("x")
    plt.ylabel("y and predicted y")
    plt.title("Ernst Engel 1857 quantile regression")
    plt.legend()
    plt.close()


## Plot the changes in the quantile coefficients and their confidence intervals
if ploton:
    ax = params.plot(x = 'quantiles', y = ['x_coef','cf_lower_bound', 'cf_upper_bound','OLS_x_coef','OLS_cf_lower_bound', 'OLS_cf_upper_bound'], title = 'Slope for different quantiles', kind ='line', style = ['b-','r--','g--','c-','m--','y--'])



