import numpy as np
import pandas as pd
import os
currentFile = 'GeneratorRealData'
dir_path = os.path.dirname(os.path.realpath(currentFile))
os.chdir(dir_path)

data = pd.read_csv('finaldf.csv', index_col=0)
idx = 1
# I changed the riskless asset to return only 2%:
data.insert(loc=idx, column="Riskless asset", value=0.5)

# rename the two exchange rates and reverse their order:
data = data.rename(columns={'AUDUSD': 'USDAUD', 'EURUSD': 'USDEUR'})
data.iloc[0:, [3, 7]] = 1 / data.iloc[0:, [3, 7]]

# compute the growth rate of the exchange rates:
data.iloc[0:, 2:] = 1 + data.iloc[0:, 2:].diff(periods=1, axis=0) / data.iloc[0:, 2:]
np.mean(data.iloc[0:, 2:])


def dataR(numberofstocks, timeperiods, data=data):
    R = data.iloc[:, 1:(numberofstocks+1)].sample(n=timeperiods)  # replace=False is default.
    return(R)


# Examples
Realdata = dataR(numberofstocks=11, timeperiods=100)
Realdata
