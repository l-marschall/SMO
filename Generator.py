import os
currentFile = 'Generator'
dir_path = os.path.dirname(os.path.realpath(currentFile))
os.chdir(dir_path)
import numpy as np


def GenerateR(N, T, distribution='student-t', df=10, mu=0, sigma=0.3):
    if distribution == 'student-t':
        print("Student-t distribution used")
        R = np.random.standard_t(df, N*T)
        R = np.array([[R]])
        R = R.reshape(T, N)
    if distribution == 'normal':
        print("Gaussian distribution used")
        R = np.random.normal(mu, sigma, N*T)
        R = np.array([[R]])
        R = R.reshape(T, N)

    R = np.asmatrix(R)
    R[:, 0] = 1.00005  # gives me the first row. Now making it a constant

    return(R)
