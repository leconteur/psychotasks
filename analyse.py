import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from scipy.stats import ttest_ind

pd.options.display.mpl_style = 'default'

if __name__ == "__main__":
    data = pd.read_csv('testall.log')
    data.index = data['timestamp']

    data = data.loc[:, ['taskname', 'workload', 'reaction time']]
    data.dropna(inplace=True)
    #print(data.groupby(['taskname', 'workload']).describe())
    groups = data.groupby(['taskname', 'workload'])
    tasks = ['nback', 'visual search', 'mental rotation']
    for task in tasks:
        easy = groups.get_group((task, 'low'))['reaction time'].values
        hard = groups.get_group((task, 'high'))['reaction time'].values
        t, prob = ttest_ind(easy, hard, equal_var=False)
        print("For the task {} the t value is {} and the prob value is {}".format(task, t, prob))
