import os
os.chdir('/home/laurits/Desktop/BGSE/Stochastic Models and Optimization/Final Project')

import copy
import numpy as np
from numpy import array
from single_period_optimizer import *
from Generator import GenerateR
from GeneratorRealData import *

N = 3
T = 3
beta = 0.05
gamma = 0.8
w = 200
R = np.asarray(dataR(N, T))

b = np.empty((T, 1), dtype=np.object)
b1 = [[0, 1, 2, 3], [0, 2, 3, 4], [0, 2, 4, 5]]
b2 = [[0, 1, 2, 3, 5], [0, 2, 3, 4, 5], [0, 2, 4, 5, 8]]
b3 = [[0, 1, 2, 3, 5, 6], [0, 2, 3, 4, 5, 10], [0, 2, 3, 4, 5, 8]]
b[0, 0] = b1
b[1, 0] = b2
b[2, 0] = b3

s = np.empty((T, 1), dtype=np.object)
s1 = [[5, 4, 3, 0], [4, 3, 2, 1], [4, 2, 2, 0]]
s2 = [[5, 4, 3.5, 3, 0], [4, 3.8, 3, 2, 1], [4, 2, 2, 1.8, 0]]
s3 = [[5, 4, 3.5, 3, 2, 0], [4, 3.8, 3, 2, 1, 0.8], [4, 3.8, 2, 2, 1.8, 0]]
s[0, 0] = s1
s[1, 0] = s2
s[2, 0] = s3


def parameter_check(b, s):
    for i in range(0, T):
        for j in range(0, N):
            if len(b[i, 0][j]) == len(s[i, 0][j]):
                pass
            else:
                print('Different length of breakpoints and slopes at', i, j)


parameter_check(b, s)


def strategy(b, s, w, R, N, T, beta, gamma):
    """
    :param b:       Breakpoints' matrix over all periods
    :param slopes:  Slopes' matrix over all periods
    :param w:       Initial wealth
    :param R:       Return matrix
    :return:        Post-decision variable at time t + DeltaV
    :beta:          Quantile of the CVaR function
    :gamma:         Balance between return and risk in the value function (risk-aversion)
    :w:             initial wealth at period t = 0
    """
    hopt = np.zeros((T+1, N))  # initialize output matrix of optimal post-decision variables
    grad = np.zeros((T+1, N))  # initialize output matrix of gradients

    R0 = np.zeros(N)  # initialize return array for period = 0, 1 for first element and 0 otherwise
    R0[0] = 1
    h0 = np.zeros(N)
    h0[0] = w

    hopt[0], grad[0] = optimize(h0, R0, b[0][0].tolist(), s[0][0].tolist())

    for i in range(1, T):
        # find function in single_period_optimizer.py
        hopt[i], grad[i] = optimize(hopt[i-1], R[i-1], b[i][0].tolist(), s[i][0].tolist())

    hopt[T][0], grad[T], finalwealth = V_lastp(hopt[T-1], R[T-1], gamma, beta, w)

    Vold = hopt[T][0]

    return(Vold, hopt, grad, finalwealth)
