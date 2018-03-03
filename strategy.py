import os
currentFile = 'strategy.py'
dir_path = os.path.dirname(os.path.realpath(currentFile))
os.chdir(dir_path)
import copy
import numpy as np
from numpy import array
from single_period_optimizer import *
from Generator import GenerateR
from GeneratorRealData import *


def parameter_check(b, s):
    for i in range(0, T):
        for j in range(0, N):
            if len(b[i, 0][j]) == len(s[i, 0][j]):
                pass
            else:
                print('Different length of breakpoints and slopes at', i, j)


def strategy(b, s, w, R, N, T, beta, gamma, theta):
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

    R0 = np.ones(N)  # initialize return array for period = 0, 1 for first element and 0 otherwise
    """
    if R0 is all ones, we need theta to be 0, in order for
     optimizer to be willing to randomize between all assets,
     so that it will add breakpoints at all assets and start training
     else all money will stay in bank, no breakpoints or slopes will be added to assets
     (since 0 is already in breakpoints) and model will never get to try out these assets
     I suggest for the first period we can just randomize instead of optimizing
    """
    h0 = np.zeros(N)
    h0[0] = w

    hopt[0], grad[0] = optimize(h0, R0, b[0][0].tolist(), s[0][0].tolist(), theta)

    for i in range(1, T):
        # find function in single_period_optimizer.py
        hopt[i], grad[i] = optimize(hopt[i-1], R[i-1], b[i][0].tolist(), s[i][0].tolist(), theta)

    hopt[T][0], grad[T], finalwealth = V_lastp(hopt[T-1], R[T-1], gamma, beta, w)

    Vold = hopt[T][0]

    return(Vold, hopt, grad, finalwealth)
