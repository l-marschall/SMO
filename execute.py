"""
This file executes the final model and set all parameter values.
"""
import os
currentFile = 'execute.py'
dir_path = os.path.dirname(os.path.realpath(currentFile))
os.chdir(dir_path)
import numpy as np
import pandas as pd
from numpy import array

from trainer import *
from strategy import *
from single_period_optimizer import *
from GeneratorRealData import *

N = 10  # number of stocks selected including the riskless assset (bank account); max: 10!
year = 52  # each year has 52 weeks
T = year * 3  # we always consider now for one iteration three years (= 52 weeks * 3)!
interest_rate = 1.0001  # interst rate of the riskless asset per week!
beta = 0.05
gamma = 1
theta = 0.001
w = 1000  # initial wealth
k = 100  # step size parameter


def execute(N, T, interest_rate, beta, gamma, theta, w, k, file_csv='finaldf.csv'):

    data_train, data_test = dataR(N, T, interest_rate, file_csv)
    #data_test = data_train[200:357]
    #data_train = data_train[:157]

    nrows = data_train.shape[0]  # number of rows of the available training data
    # the training iterations are always maximized now and determined by the numer of datapoints!
    S = nrows - T

    # training part:
    bp = initialize_bp(N, T)
    slopes = initialize_slopes(N, T)

    V_optimization = []  # initialize empty array and append V-value after every iteration
    finalwealth_array = []

    for s in range(S):
        R = np.asarray(data_train.iloc[s:(T+s)])
        try:
            V, h, grad, finalwealth = strategy(bp, slopes, w, R, N, T, beta, gamma, theta)
            print(finalwealth)
            finalwealth_array.append(finalwealth)
            bp, slopes = update(bp, slopes, grad, h, s, k, T, N)
            V_optimization.append(V)
        except:
            pass

    # testing part:
    R = np.asarray(data_test)
    V_test, h_test, grad_test, finalwealth_test = strategy(
        bp, slopes, w, R, N, T, beta, gamma, theta)

    return(finalwealth, finalwealth_array, h_test, bp, slopes, V_optimization, finalwealth_test)


finalwealth, finalwealth_array, h_test, bp, slopes, V_optimization, finalwealth_test = execute(
    N, T, interest_rate, beta, gamma, theta, w, k, file_csv='finaldf.csv')

#finalwealth_test is 1077.279376331775

x, y = getcoord(bp[-1][-1].tolist(),slopes[-1][-1].tolist())

x1 = pd.Series(x,name="x")
y1 = pd.Series(y,name="y")
xy_df = pd.concat([x1,y1],axis=1)
h_test_df = pd.DataFrame(h_test)
finalwealthar_df = pd.DataFrame(finalwealth_array)
V_optimization_df = pd.DataFrame(V_optimization)
slopes_df = pd.DataFrame(slopes)
bp_df = pd.DataFrame(bp)

xy_df.to_csv("xy2.csv")
h_test_df.to_csv("htest2.csv")
finalwealthar_df.to_csv("finalwealthar2.csv")
V_optimization_df.to_csv("V_optimization2.csv")
slopes_df.to_csv("slopes2.csv")
bp_df.to_csv("bp2.csv")

