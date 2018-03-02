# -*- coding: utf-8 -*-
"""
S. Hamed Mirsadeghi

This file train the model.
"""
import os
currentFile = 'trainer-02'
dir_path = os.path.dirname(os.path.realpath(currentFile))
os.chdir(dir_path)
import numpy as np
from numpy import random as rd
from strategy import *
from single_period_optimizer import *
from Generator import GenerateR
from GeneratorRealData import *
# This function updates the slope and break points for each senario s


def fixcase2(index, curr_bp, curr_sl):

    mean = np.cumsum(curr_sl[index:]) / range(1, len(curr_sl) - index+1)

    if curr_sl[index] < curr_sl[index + 1]:
        print("deleted case 2")
        c1 = -1
        
        if index > len(curr_sl)-2:
            for i1 in range(1, len(curr_sl)-index):
                if curr_sl[index+i1+1] < mean[i1]:
                    c1 = index + i1  # index of last breakpoint to delete
                    break
        if c1 == -1:
            curr_sl[-1] = mean[-1]
            curr_sl = np.delete(curr_sl, range(index, len(curr_sl) - 1))
            curr_bp = np.delete(curr_bp, range(index+1, len(curr_bp)))
        else:
            curr_sl = np.delete(curr_sl, range(index, c1+1))
            curr_bp = np.delete(curr_bp, range(index+1, c1+1))
            curr_sl = np.insert(curr_sl, index, mean[c1-index])

    return(curr_bp, curr_sl)

#test for c1 != -1
#curr_bp = np.array([0,2,2.5,3,4],dtype = float)
#curr_sl = np.array([4,3,1.8,2,1],dtype = float)
#index = 2

#test for c1 == -1
#curr_bp = np.array([0,2,2.5,3,4],dtype = float)
#curr_sl = np.array([4,3,1.8,2,1],dtype = float)
#index = 2


def fixcase1(index, curr_bp, curr_sl):
    print("deleted case 1")
    mean = np.cumsum(curr_sl[index::-1])[::-1] / range(1, index+2)[::-1]

    c2 = -1
    for i2 in range(1, index+1):
        if mean[-i2] < curr_sl[index-i2]:
            c2 = index-i2+2  # index of first breakpoint to delete
            break
    if c2 == -1:
        curr_sl = np.delete(curr_sl, range(index+1))
        curr_bp = np.delete(curr_bp, range(1, index+1))
        curr_sl = np.insert(curr_sl, 0, mean[0])
    else:
        curr_sl = np.delete(curr_sl, range(c2-1, index + 1))
        curr_bp = np.delete(curr_bp, range(c2, index + 1))
        curr_sl = np.insert(curr_sl, c2-1, mean[c2-index-2])

    return(curr_bp, curr_sl)

#test for c2 != -1
#curr_bp = np.array([0,2,2.5,3,4],dtype = float)
#curr_sl = np.array([4,3,4,2,1],dtype = float)
#index = 2


#test for c2 == -1
#curr_bp = np.array([0,2,2.5,3,4],dtype = float)
#curr_sl = np.array([4,3,10,2,1],dtype = float)
#index = 2
    
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
                
                if j != 0:
                    print("addbp")
                curr_bp = np.sort(np.hstack((curr_bp, h[i][j])))
                index = np.where(curr_bp == h[i][j])[0][0]
                new_slope = (1 - alpha) * curr_sl[index-1] + alpha * grad_v[i][j]
                curr_sl = np.insert(curr_sl, index, new_slope)

                if index < len(curr_sl)-1:
                    if curr_sl[index] < curr_sl[index + 1]:
                        curr_bp, curr_sl = fixcase2(index, curr_bp, curr_sl)

                if curr_sl[index] > curr_sl[index - 1]:
                    curr_bp, curr_sl = fixcase1(index, curr_bp, curr_sl)

            newslope_t.append(curr_sl.tolist())
            newbp_t.append(curr_bp.tolist())

        newslope_t = np.asarray(newslope_t)
        newbp_t = np.asarray(newbp_t)

        newslope.append(np.array([newslope_t]))
        newbp.append(np.array([newbp_t]))

    return (newslope, newbp)


T = 30
N = 5
beta = 0.05
gamma = 0.9
w = 200  # initial wealth
S = 50  # training iterations
k = 5  # step size parameter



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
        slopes_ij.append([3])
    slopes[i, 0] = np.array(slopes_ij, dtype=float)



#break_point1 = np.empty((T, 1), dtype=np.object)
#break_point1[0,0] = np.array ([[0, 2, 3, 4],[0, 1.5, 22, 30]] , dtype=float)
#break_point1[1,0] = np.array ([[0, 1, 2, 3, 5], [0, 2, 3, 4, 5]]  , dtype=float)
#break_point1[2,0] = np.array ([[0, 1, 2, 3, 5, 6], [0, 2, 3, 4, 5, 10]]  , dtype=float)
#
#
#slope1 = np.empty((T, 1), dtype=np.object)
#slope1[0,0] = np.array ([[4, 3, 2, 1],[55, 54, 1, 0.1]] ,dtype=float)
#slope1[1,0] = np.array ([[5, 4, 3.5, 3, 0], [4, 3.8, 3, 2, 1]] ,dtype=float)
#slope1[2,0] = np.array ([[5, 4, 3.5, 3, 2, 0], [4, 3.8, 3, 2, 1, 0.8]] ,dtype=float)

#Rsum = np.zeros((N,T))

for s in range(S):
    R = np.asarray(dataR(N, T))
    #Rsum = Rsum + R
    V, h, grad, finalwealth = strategy(bp, slopes, w, R, N, T, beta, gamma)
    slopes, bp = update(bp, slopes, grad, h, s, k, T, N)

print(bp)
print(slopes)
#print(Rsum/S)
