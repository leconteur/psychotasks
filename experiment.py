"""This module contains the class to help build a standard experiment."""
from __future__ import print_function
from psychopy import visual, core, event
import time
import datetime


class ExitException(Exception):
    pass

class AbstractSlide(object):
    def __init__(self, showtime, pausetime, configurations, window):
        self.window = window
        self.framerate = 1.0/60.0
        self.max_frame = showtime/self.framerate
        self.pausetime = pausetime
        self.configurations = configurations

    def show(self):
        timestamp = datetime.datetime.fromtimestamp(time.time())
        event.clearEvents()
        i_frame = 0
        total_time = False
        answers = None
        while not self.stoploop(i_frame):
            self.draw()
            self.window.flip()
            answers = self.getAnswer(answers)
            if any(answers) and total_time is False:
                total_time = i_frame * self.framerate
            i_frame += 1
        if total_time is False:
            total_time = None
        self.window.flip(clearBuffer=True)
        core.wait(self.pausetime)
        sound = self.play_sound(answers)
        ans = self.getAnswerValue(answers)
        ans.update({'reaction time':total_time, 'timestamp':timestamp, 'sound_played':sound})
        ans.update(self.configurations)
        return ans

    def stoploop(self, frame):
        return frame > self.max_frame

    def play_sound(self, answers):
        print("BEEEEEEEEEP")
        return False

class Instructions(object):
    """Instructions for the current experiment. It will be shown a certain
    amount of time before the start of an exeperiment."""
    def __init__(self, text, time=1, color='white'):
        self.text = text
        self.time = time
        self.color = color

    def show(self, win):
        """Show the instruction on the window win."""
        textstim = visual.TextStim(win, text=self.text, color=self.color)
        textstim.setAutoDraw(True)
        win.flip()
        event.waitKeys(keyList=['return'])
        textstim.setAutoDraw(False)
        win.flip(clearBuffer=True)
        core.wait(self.time)



class Experiment(object):
    """An experiment is a single condition."""
    def __init__(self):
        self.instructions = None
        self.slides = None
        self.logger = None
        self.wait_time = None
        self.experiment_id = None
        self.win = None
        self.sentinels = None

    def configure(self, instructions, slides, logger, sentinels, window):
        self.instructions = instructions
        self.slides = slides
        self.logger = logger
        self.win = window
        self.sentinels = sentinels if sentinels is not None else []

    def run(self):
        """Run the preconfigured experiment."""
        self.instructions.show(self.win)
        for slide in self.slides:
            ret_val = slide.show()
            self.logger.log_trial(ret_val)
            for s in self.sentinels:
                if not s.checkValid():
                    raise Exception("The {} is disconnected.".format(s.getDeviceName()))
