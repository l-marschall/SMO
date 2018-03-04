"""
This file plots the final results of the execute function.
"""
import os
currentFile = 'plotting'
dir_path = os.path.dirname(os.path.realpath(currentFile))
os.chdir(dir_path)
print(dir_path)
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

company_list = ['Amazon', 'Bank of New York', 'Barclays', 'Coca Cola', 'lowe‘s Companies',
                'Nike', 'Norfolk Southern Railway', 'State Street Corporation', 'Walmart']
xy = pd.read_csv('xy.csv')

V_optimization = pd.read_csv('V_optimization.csv')
V_optimization.columns = ['index', 'V']

slopes = pd.read_csv('slopes.csv')
slopes.columns = ['index', 'slopes']

htest = pd.read_csv('htest.csv')
htest.columns = ['index', 'Bank'] + company_list
htest = htest.melt(id_vars=['index'], var_name='stock')

finalwealth = pd.read_csv('finalwealthar.csv')
finalwealth.columns = ['index', 'finalwealth']

bp = pd.read_csv('bp.csv')
bp.columns = ['index', 'breakpoints']


sns.factorplot(x='index', y='value', hue='stock', data=htest, scale=2)
plt.show()

sns.set(style="darkgrid")
paper_rc = {'lines.linewidth': 1}
sns.set_context("paper", rc=paper_rc)

plt.close()
fig, ax = plt.subplots(dpi=300)
fig.set_size_inches(11.7, 8.27)
sns.factorplot(ax=ax, data=htest, x='index', y='value', hue='stock')
plt.setp(ax.collections, sizes=[0])
ax.set_xlabel('')
plt.savefig("htest.pdf")
plt.show()
