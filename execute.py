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

T = 250
N = 5
beta = 0.05
gamma = 0.9
w = 1000  # initial wealth
S = 300  # training iterations
k = 10  # step size parameter


def excecute(N, T, beta, gamma, theta, w, S, k):
    bp = initialize_bp(N, T)
    slopes = initialize_slopes(N, T)

    for s in range(S):
        R = np.asarray(dataR(N, T))
        V, h, grad, finalwealth = strategy(bp, slopes, w, R, N, T, beta, gamma, theta)
        slopes, bp = update(bp, slopes, grad, h, s, k, T, N)

    actualR = np.asarray(dataR(N, T))
    meanR = Rmean(N, T)
    meanR = meanR[0:N]
    hreal, wealthreal = test(bp, slopes, meanR, w, T, N, gamma, beta, actualR)

    return(finalwealth, h, hreal, wealthreal)
