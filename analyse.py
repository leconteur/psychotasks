import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from scipy.stats import ttest_ind

pd.options.display.mpl_style = 'default'

if __name__ == "__main__":
    data_nback = pd.read_csv('test.log')
    data_nback['workload'] = np.where(data_nback['n_back'] == 1, 'low', 'high')
    data_nback['task'] = 'nback'
    data_nback.index = data_nback['timestamp']
    data_vs = pd.read_csv('test_vs.log')
    data_vs['workload'] = data_vs['difficulty']
    data_vs['task'] = 'visual search'
    data_vs.index = data_vs.timestamp
    data_mr = pd.read_csv('test_mr.log')
    data_mr['workload'] = np.where(data_mr['difficulty'] == 'easy', 'low', 'high')
    data_mr['task'] = 'mental rotation'
    data_mr.index = data_mr.timestamp
    data = pd.concat([data_nback, data_vs, data_mr])
    data = data.loc[:, ['workload', 'reaction time', 'task']]

    data.groupby('task').boxplot(by='workload')
    # plt.ylim((0, 8))
    plt.show()
