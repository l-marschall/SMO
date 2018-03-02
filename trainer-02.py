# -*- coding: utf-8 -*-
"""
S. Hamed Mirsadeghi

This file train the model.
"""
import os
os.chdir('/home/laurits/Desktop/BGSE/Stochastic Models and Optimization/Final Project/SMO')
import numpy as np
from numpy import random as rd
from strategy import *
from single_period_optimizer import *
from Generator import GenerateR
from GeneratorRealData import *
# This function updates the slope and break points for each senario s


def update(break_point, slope, grad_v, h, s, k, T, N):
    '''
    Would be nice if you could add a short description on every input
    parameter of the function.
    '''

    alpha = k/(k+s)
    '''
    as I understand it, s is a counter of the scenarios and
    should increase after every iteration?!
    '''
    newslope = []
    newbp = []

    for i in range(T):
        newslope_t = []
        newbp_t = []

        for j in range(N):
            curr_bp = np.asarray(break_point[i][0][j])
            curr_sl = np.asarray(slope[i][0][j])

            if h[i][j] not in curr_bp:

                curr_bp = np.sort(np.hstack((curr_bp, h[i][j])))
                index = np.where(curr_bp == h[i][j])[0][0]
                new_slope = (1 - alpha) * curr_sl[index-1] + alpha * grad_v[i][j]
                curr_sl = np.insert(curr_sl, index, new_slope)
                mean = np.cumsum(curr_sl[index:]) / range(1, len(curr_sl) - index+1)

                if index < len(curr_sl)-1:
                    if curr_sl[index] < curr_sl[index + 1]:
                        print("deleted case 2")
                        c1 = -1
                        for i1 in range(len(curr_sl) - 1, index, -1):
                            if curr_sl[i1] < mean[i1 - index - 1]:
                                c1 = i1
                        if c1 == -1:
                            curr_sl[-1] = mean[-1]
                            curr_sl = np.delete(curr_sl, range(index, len(curr_sl) - 1))
                            curr_bp = np.delete(curr_bp, range(index, len(curr_sl) - 1))
                        else:
                            curr_sl[c1 - 1] = mean[c1 - index - 1]
                            curr_sl = np.delete(curr_sl, range(index, c1 - 1))
                            curr_bp = np.delete(curr_bp, range(index, c1 - 1))

                elif curr_sl[index] > curr_sl[index - 1]:
                    print("deleted case 1")
                    mean = np.cumsum(curr_sl[index::-1])[::-1] / range(1, index+2)[::-1]

                    c2 = -1
                    for i2 in range(0, index):
                        if curr_sl[i2] > mean[i2 + 1]:
                            c2 = i2
                    if c2 == -1:
                        curr_sl[0] = mean[0]
                        curr_sl = np.delete(curr_sl, range(index, 0, -1))
                        curr_bp = np.delete(curr_bp, range(index, 0, -1))
                    else:
                        curr_sl[c2 + 1] = mean[c2 + 1]
                        curr_sl = np.delete(curr_sl, range(c2+2, index + 1))
                        curr_bp = np.delete(curr_bp, range(c2+2, index + 1))

            newslope_t.append(curr_sl.tolist())
            newbp_t.append(curr_bp.tolist())

        newslope_t = np.asarray(newslope_t)
        newbp_t = np.asarray(newbp_t)

        newslope.append(np.array([newslope_t]))
        newbp.append(np.array([newbp_t]))

    return (newslope, newbp)


T = 3
N = 2
beta = 0.05
gamma = 0.8

# initialize bp,slopes
bp = np.empty((T, 1), dtype=np.object)
for i in range(T):
    bp_ij = []
    for j in range(N):
        bp_ij.append([0])
    bp[i, 0] = np.array(bp_ij, dtype=float)

slopes = np.empty((T, 1), dtype=np.object)
for i in range(T):
    slopes_ij = []
    for j in range(N):
        slopes_ij.append([2])
    slopes[i, 0] = np.array(slopes_ij, dtype=float)

# initial wealth
w = 200


# train the model
S = 40
k = 500

for s in range(S):
    R = np.asarray(dataR(N, T))
    V, h, grad, finalwealth = strategy(bp, slopes, w, R, N, T, beta, gamma)
    slopes, bp = update(bp, slopes, grad, h, s, k, T, N)

print(bp)
print(slopes)
