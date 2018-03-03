import numpy as np
import pandas as pd
import os
currentFile = 'GeneratorRealData'
dir_path = os.path.dirname(os.path.realpath(currentFile))
os.chdir(dir_path)


def dataR(N, T, interest_rate, file_csv='finaldf.csv'):
    data = pd.read_csv(file_csv, index_col=0)
    data = data.iloc[:, 1:]  # remove timestamp from data set

    idx = 0
    data.insert(loc=idx, column="Riskless asset", value=interest_rate)
    nstocks = data.shape[1]  # number of stocks is equal to number of columns:

    if N <= nstocks:
        data = data.iloc[0:, 0:N]
        # compute the growth rate of the exchange rates:
        data.iloc[0:, 1:] = 1 + data.iloc[0:, 1:].diff(periods=1, axis=0) / data.iloc[0:, 1:]
        data = data[1:]
        nrows = data.shape[0]
        data_training = data[0: (nrows - T)]
        data_test = data[(nrows - T):]

        return(data_training, data_test)

    else:
        print('More stocks selected than available in data frame', '!')
