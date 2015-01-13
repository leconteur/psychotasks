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
        self.sound_played = False
        self.timestamp = 0
        self.i_frame = 0
        self.final_frame = 0
        self.answered = False

    def show(self):
        self.timestamp = datetime.datetime.fromtimestamp(time.time())
        event.clearEvents()
        answers = None
        while not self.stoploop():
            self.draw()
            self.window.flip()
            answers = self.getAnswer(answers)
            if any(answers) and not self.answered:
                self.answered = True
                self.final_frame = self.i_frame
            sound = self.play_sound(answers)
            self.i_frame += 1
        self.window.flip(clearBuffer=True)
        core.wait(self.pausetime)
        return self.getOutput(answers)

    def getOutput(self, answers):
        ans = self.getAnswerValue(answers)
        ans.update({'reaction time':self.total_time(), 'timestamp':self.timestamp,
                    'sound_played':self.sound_played})
        ans.update(self.configurations)
        return ans

    def stoploop(self):
        return self.i_frame > self.max_frame

    def play_sound(self, answers):
        return False

    def current_time(self):
        return self.i_frame * self.framerate

    def total_time(self):
        if not self.answered:
            return None
        return self.final_frame * self.framerate

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
