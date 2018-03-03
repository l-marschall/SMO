import numpy as np
import pandas as pd
import os
currentFile = 'GeneratorRealData'
dir_path = os.path.dirname(os.path.realpath(currentFile))
os.chdir(dir_path)


def dataR(N, interest_rate, file_csv='finaldf.csv'):
    data = pd.read_csv(file_csv, index_col=0)
    idx = 1

    nstocks = data.shape[1] - 1  # number of stocks is equal to number of columns minus timestamp!
    if N <= nstocks:
        # I changed the riskless asset to return only 2%:
        data.insert(loc=idx, column="Riskless asset", value=interest_rate)

        # compute the growth rate of the exchange rates:
        data.iloc[0:, 2:] = 1 + data.iloc[0:, 2:].diff(periods=1, axis=0) / data.iloc[0:, 2:]
        data = data[1:]

        return(data)

    else:
        print('More stocks selected than available in data frame!')


def dataR(numberofstocks, timeperiods, data=data):
    R = data.iloc[:, 1:(numberofstocks+1)].sample(n=timeperiods)  # replace=False is default.
    return(R)


def Rmean(N, T, data=data):
    meanR = np.asarray(np.mean(data, axis=0))
    return(meanR)
