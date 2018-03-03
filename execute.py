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
T = 52  # we always consider now for one iteration one year (= 52 weeks)!
interest_rate = 1.0001  # interst rate of the riskless asset per week!
beta = 0.05
gamma = 0.9
theta = 0.001
w = 1000  # initial wealth
k = 10  # step size parameter


def excecute(N, T, interest_rate, beta, gamma, theta, w, k, file_csv='finaldf.csv'):

    data_train, data_test = dataR(N, T, interest_rate, file_csv)
    nrows = data_train.shape[0]  # number of rows of the available training data
    # the training iterations are always maximized now and determined by the numer of datapoints!
    S = nrows - T

    # training part:
    bp = initialize_bp(N, T)
    slopes = initialize_slopes(N, T)

    V_optimization = []  # initialize empty array and append V-value after every iteration

    for s in range(S):
        R = np.asarray(data_train.iloc[s:(T+s)])
        V, h, grad, finalwealth = strategy(bp, slopes, w, R, N, T, beta, gamma, theta)
        bp, slopes = update(bp, slopes, grad, h, s, k, T, N)
        V_optimization.append(V)

    # testing part:
    R = np.asarray(data_test)
    V_test, h_test, grad_test, finalwealth_test = strategy(
        bp, slopes, w, R, N, T, beta, gamma, theta)

    return(finalwealth, h, slopes, V_optimization, finalwealth_test)


finalwealth, h, slopes, V_optimization, finalwealth_test = execute(
    N, T, interest_rate, beta, gamma, theta, w, k, file_csv='finaldf.csv')
