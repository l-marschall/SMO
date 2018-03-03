# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 22:11:39 2018

@author: kellykkl
"""
import os
currentFile = 'singe_period_optimizer'
dir_path = os.path.dirname(os.path.realpath(currentFile))
os.chdir(dir_path)
from gurobipy import GRB, GurobiError, Model, quicksum
import numpy as np
import copy
from numpy import array


def getcoord(bp, slopes):

    # from: bp = [[a1,...]_0,...,[]_N]_t
    # get coordinates of vertices defining value functions
    # x = [[x1,x2...]_0,...,[x1,x2...]_N]_t
    # y =

    x = copy.deepcopy(bp)
    # add one breakpoint very far away corr to last slope
    for i in range(len(x)):
        x[i].append(10000)

    y = []
    # first breakpoint is always 0
    for i in range(len(slopes)):
        y.append([0])
        yval = 0
        for j in range(len(slopes[i])):
            yval = yval + (x[i][j+1]-x[i][j])*slopes[i][j]
            y[i].append(yval)

    return (x, y)


def optimize(hp, Rt, bp, slopes, theta):
    """
    :param R:       Returns at time t (Gross)
    :param hp:      Post-decision variable (pre-return) at time t-1
    :param bp:      Breakpoints at time t
    :param slopes:  Slopes at time t
    :return:        Post-decision variable at time t + DeltaV
    """

    grad = []  # gradient deltaV_(t-1)

    h = Rt * hp  # element wise multiplication
    x, y = getcoord(bp, slopes)

    # print(x)
    # print(y)

    N = len(bp)-1  # no of holdings, excluding cash

    m = Model()
    m.setParam('OutputFlag', False)

    """Add Variables"""
    # add x_i, y_i as variables (all x first, then all y)
    # 2N variables
    xv = array([m.addVar() for _ in range(N)])                   # Buys   at time t
    yv = array([m.addVar() for _ in range(N)])                   # Sales  at time t
    # also add hpv for convenience (we'll have equality const relating to xv,yv)
    hpv = array([m.addVar(lb=0) for _ in range(N+1)])  # h_plus at time t
    m.update()

    """Add Objective Function"""
    outputCashFlow = (1 + theta) * quicksum(xv) - (1 - theta) * quicksum(yv)
    m.setPWLObj(hpv[0], x[0], y[0])
    for i in range(1, N+1):
        m.setPWLObj(hpv[i], x[i], y[i])

    """Add Constraints"""
    eqCstrs = [m.addConstr(hpv[i] - h[i] == xv[i-1] - yv[i-1]) for i in range(1, N+1)]
    eqCstrs.append(m.addConstr(hpv[0] - h[0] == -1*outputCashFlow))
    holdingCstrs = [m.addConstr(-xv[i-1] + yv[i-1] <= h[i]) for i in range(1, N+1)]
    budgetCstr = m.addConstr(outputCashFlow <= h[0])

    m.ModelSense = -1  # maximize
    m.update()

    try:
        m.optimize()
    except GurobiError as e:
        pass
        print("failed")

    # print(m.Status)

    # optimal variables
    # print([(v.varName, v.X) for v in m.getVars()])

    # optimal h vector
    hopt = []
    for i in range(N+1):
        hopt.append(hpv[i].X)

    # get optimal function value
    Vold = m.ObjVal

    # solve N+1 times, incrementing hp component wise

    for i in range(N+1):

        hp1 = np.copy(hp)
        hp1[i] = hp[i]+1
        h = Rt * hp1  # element wise multiplication
        x, y = getcoord(bp, slopes)

        N = len(bp)-1  # no of holdings, excluding cash

        m = Model()
        m.setParam('OutputFlag', False)

        """Add Variables"""
        # add x_i, y_i as variables (all x first, then all y)
        # 2N variables
        xv = array([m.addVar() for _ in range(N)])                   # Buys   at time t
        yv = array([m.addVar() for _ in range(N)])                   # Sales  at time t
        # also add hpv for convenience (we'll have equality const relating to xv,yv)
        hpv = array([m.addVar(lb=0) for _ in range(N+1)])  # h_plus at time t
        m.update()

        """Add Objective Function"""
        outputCashFlow = (1+theta) * quicksum(xv) - (1-theta) * quicksum(yv)
        m.setPWLObj(hpv[0], x[0], y[0])
        for i in range(1, N+1):
            m.setPWLObj(hpv[i], x[i], y[i])

        """Add Constraints"""
        eqCstrs = [m.addConstr(hpv[i] - h[i] == xv[i-1] - yv[i-1]) for i in range(1, N+1)]
        eqCstrs.append(m.addConstr(hpv[0] - h[0] == -1*outputCashFlow))
        holdingCstrs = [m.addConstr(-xv[i-1] + yv[i-1] <= h[i]) for i in range(1, N+1)]
        budgetCstr = m.addConstr(outputCashFlow <= h[0])

        m.ModelSense = -1  # maximize
        m.update()

        try:
            m.optimize()
        except GurobiError as e:
            pass
            print("failed")

        # get optimal function value
        Vnew = m.ObjVal
        grad.append(Vnew-Vold)

    return (np.asarray(hopt), np.asarray(grad))


def CVaR(h, w, beta):
    # w: initial wealth
    # h: vector of holdings
    h = sorted(h)
    h = h[1:]
    for i in range(len(h)):
        h[i] = h[i] - w
    S = len(h)
    l = int(np.ceil(S * (1-beta)))
    summ = 0
    for i in range(l):
        summ = summ + h[i]
    return -(summ / (S * (1-beta)) + h[l-1] * (1 - (l-1) / (S * (1 - beta))))


# for last period we will have a different value function (no longer completely separable)
# only have one V_T, not N+1 V_i,T's
def V_lastp(hp, RT, gamma, beta, w):
    """
    :param R:       Returns at time T (Gross)
    :param hp:      Post-decision variable (pre-return) at time T-1
    :param w:       Initial wealth at t=0
    :return:        V at given hp, Gradient
    """
    grad = []
    h = RT * hp
    finalwealth = np.sum(h)
    Vold = gamma*np.sum(h) - (1-gamma)*CVaR(h, w, beta)
    N = hp.size-1

    for i in range(N+1):
        hp1 = np.copy(hp)
        hp1[i] = hp[i]+1
        h = RT * hp1  # element wise multiplication

        Vnew = gamma*np.sum(h) - (1-gamma)*CVaR(h, w, beta)
        grad.append(Vnew-Vold)

    return (Vold, np.asarray(grad), finalwealth)
