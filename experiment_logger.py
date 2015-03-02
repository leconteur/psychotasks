"""This module implements common logging functions. It uses pandas to
write the data to the disk."""
from __future__ import print_function
import pandas as pd
import os


class Logger():
    """The logger uses pandas to write the data on the disk."""
    def __init__(self, filename, check_filename=True):
        self.filename = filename
        self.check_filename = check_filename
        if self.check_fileconflict():
            raise IOError('Filename already taken')
        self.data = pd.DataFrame()

    def log_trial(self, data):
        """Data is a dictionary containing the data for the current run."""
        line = pd.DataFrame(data, index=[0])
        self.data = pd.concat([self.data, line], ignore_index=True)

    def save_to_csv(self):
        """Save the data to the csv 'filename'"""
        if self.check_fileconflict():
            raise IOError('Filename already taken')
        d = os.path.dirname(self.filename)
        if not os.path.exists(d):
            os.makedirs(d)
        mode = 'a' if os.path.exists(self.filename) else 'w'
        head = False if os.path.exists(self.filename) else True
        self.data.to_csv(self.filename, encoding='utf-8',
                         header=head, mode=mode)

    def check_fileconflict(self):
        """Returns a boolean indicating if the filename is already present."""
        return os.path.exists(self.filename) and self.check_filename

    def saveExperimentInfo(self, participant_info, experiment_info, runtime):
        print(participant_info, experiment_info, runtime)

if __name__ == "__main__":
    import random
    logger = Logger("test.csv")
    fake_trials = []
    for _ in range(10):
        target = random.randint(0, 2) == 1
        difficulty = random.randint(0, 4)
        answer = random.randint(0, 2) == 1
        reaction_time = random.uniform(0, 2)

        fake_trials.append({'target':target, 'difficulty':difficulty,
                            'answer':answer, 'reaction time': reaction_time})
    for trial in fake_trials:
        logger.log_trial(trial)
    logger.log_trial({'target':False, 'other':True})
    logger.save_to_csv()
