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
    data.columns = [col.replace('.', '_') for col in data.columns]

    return data


def load_eyetracker(filename):
    with open(filename) as f:
        jsongen = decodeJson(f)
        tracker_data = filterHeartbeat(jsongen)
        return json_to_pandas(tracker_data)


def load_data(filename, taskname):
    data = pd.read_csv(filename, index_col='timestamp', parse_dates=True)
    data = data.drop('Unnamed: 0', axis=1)
    data = data[data.taskname == taskname]
    data = data.dropna(how='all', axis=1)
    return data


def compute_nback(data):
    absent = data['participant response'] == 'absent'
    present = data['participant response'] == 'present'
    target = data.target
    correct = (absent & target.ne(True)) | (present & target)
    rt = data['reaction time']
    return pd.DataFrame({'correct':correct, 'reaction time':rt, 'workload':data.workload,
                         'taskname':data.taskname})


def compute_mr(data):
    response = data['participant response'] == 'same'
    correct = response == data.target
    rt = data['reaction time']
    workload = data.workload
    return pd.DataFrame({'correct':correct, 'reaction time':rt, 'workload':workload,
                         'taskname':data.taskname})


def compute_vs(data):
    rt = data['reaction time']
    workload = data.workload
    return pd.DataFrame({'correct':True, 'reaction time':rt, 'workload':workload,
                         'taskname':data.taskname})


def load_bioharness(filename):
    columns = ['Time', 'HR', 'BR', 'Posture', 'Activity', 'PeakAccel','BRAmplitude', 'BRNoise',
               'BRConfidence', 'ECGAmplitude', 'ECGNoise', 'HRConfidence', 'HRV',
               'SystemConfidence', 'VerticalMin', 'VerticalPeak', 'LateralMin', 'LateralPeak',
               'SagittalMin', 'SagittalPeak', 'DeviceTemp', 'StatusInfo', 'CoreTemp']
    na_values = {'HR':{0:np.nan}, 'BR':{6553.5:np.nan}, 'BRAmplitude':{0:np.nan},
                 'BRNoise':{65535:np.nan}, 'BRConfidence':{255:np.nan}, 'ECGAmplitude':{0:np.nan},
                 'ECGNoise':{0:np.nan}, 'HRV':{65535:np.nan}, 'CoreTemp':{6553.5:np.nan}}
    data = pd.read_csv(filename, usecols=columns, index_col='Time', parse_dates=True)
    data.replace(na_values, inplace=True)
    return data

if __name__ == "__main__":
    data_et = load_eyetracker('results_olivier/loget.txt')
    data_et.replace(0, np.nan, inplace=True)
    data_nback = load_data('results_olivier/testall.log', 'nback')
    nback_perf = compute_nback(data_nback)
    data_mr = load_data('results_olivier/testall.log', 'mental rotation')
    mr_perf = compute_mr(data_mr)
    data_vs = load_data('results_olivier/testall.log', 'visual search')
    vs_perf = compute_vs(data_vs)
    data = pd.concat([nback_perf, mr_perf, vs_perf])
    data.workload = pd.Categorical(data.workload, categories=['low', 'high'])
    data_bh = load_bioharness('results_olivier/bioharness.csv')
    data = data.resample('S', how='last').join([data_et.resample('S'), data_bh.resample('S')], how='outer')
    data.columns = [col.replace(' ', '_') for col in data.columns]
