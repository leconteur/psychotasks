import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from pandas.io.json import json_normalize
import json
from scipy.stats import ttest_ind, zscore, wilcoxon, mannwhitneyu


pd.options.display.mpl_style = 'default'


def decodeJson(generator):
    for line in generator:
        yield json.loads(line)


def filterHeartbeat(generator):
    for json in generator:
        if json['category'] == 'tracker':
            yield json['values']['frame']


def json_to_pandas(generator):
    data = list(generator)
    data = json_normalize(data)
    data = data.set_index('timestamp')
    data.index = data.index.to_datetime()
    columns_labels = [tuple(c.split('.')) for c in data.columns]
    data.columns = pd.MultiIndex.from_tuples(columns_labels)

    return data


def load_eyetracker(filename):
    with open(filename) as f:
        jsongen = decodeJson(f)
        tracker_data = filterHeartbeat(jsongen)
        return json_to_pandas(tracker_data)

if __name__ == "__main__":
    #data = load_eyetracker('results_olivier/loget.txt')
    data = pd.read_csv('testall.log')
    data.index = data['timestamp']

    data = data.loc[:, ['taskname', 'workload', 'reaction time']]
    data.dropna(inplace=True)
    data['z time'] = data.groupby('taskname').transform(zscore)
    groups = data.groupby(['taskname', 'workload'])
    data.boxplot('z time', by=['taskname', 'workload'])
    plt.show()
    tasks = ['nback', 'visual search', 'mental rotation']
    for task in tasks:
        easy = groups.get_group((task, 'low'))['reaction time']
        hard = groups.get_group((task, 'high'))['reaction time']
        #t, prob = ttest_ind(easy.values, hard.values, equal_var=False)
        l = min(len(easy.values), len(hard.values))
        easyvalues, hardvalues = easy.values[0:l], hard.values[0:l]
        #t, pvalue = wilcoxon(easyvalues, hardvalues)
        t, pvalue = mannwhitneyu(easyvalues, hardvalues)
        print("For the task {} the t value is {} and the prob value is {}".format(task, t, pvalue))
        easy = groups.get_group((task, 'low'))
        hard = groups.get_group((task, 'high'))
