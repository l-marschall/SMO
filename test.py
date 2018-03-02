# -*- coding: utf-8 -*-
"""
Created on Fri Mar  2 20:44:04 2018

@author: kellykkl
"""

import os
currentFile = 'test.py'
dir_path = os.path.dirname(os.path.realpath(currentFile))
os.chdir(dir_path)
import copy
import numpy as np
from numpy import array
from single_period_optimizer import *
from Generator import GenerateR
from GeneratorRealData import *

#To evaluate the trained model

def test(bp,slopes,meanR,w,T,N,gamma,beta,actualR):
    """
    :param bp:      Breakpoints of trained value functions (all periods)
    :param slopes:  Slopes of trained value functions (all periods)
    :param w:       Initial wealth
    :param meanR:   Mean return of each asset (calc. over historical data) (1xN)
    :param actualR: Actual returns
    :w:             initial wealth at period t = 0
    :return:        final optimal portfolio, final wealth
    """
    hopt = np.zeros((T+1, N))  # initialize output matrix of optimal post-decision variables
    grad = np.zeros((T+1, N))  # initialize output matrix of gradients
    
    h0 = np.zeros(N)
    h0[0] = w
    R0 = np.ones(N)  # initialize return array for period = 0, 1 for first element and 0 otherwise

#    h0 = np.asarray([20] * N, dtype = float)
    
    #hopt[0] is post decision var at period 0
    hopt[0], grad[0] = optimize(h0, R0, bp[0][0].tolist(), slopes[0][0].tolist())
    #now, hopt[1] is pre decision var at period 1
    hopt[1] = hopt[0]*actualR[0] 
    
    for i in range(1, T-1):
        #post decision var at period i
        hopt[i], grad[i] = optimize(hopt[i], meanR, bp[i][0].tolist(), slopes[i][0].tolist())
        #pre decision variable at period i+1
        hopt[i+1] = hopt[i] * actualR[i]

    hopt[T][0], grad[T], finalwealth = V_lastp(hopt[T-1], actualR[T-1], gamma, beta, w)
    
    return(hopt,finalwealth)