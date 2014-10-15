"""This module contains the class to help build a standard experiment."""
from __future__ import print_function
from psychopy import visual, core, event


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
        ans = self.getAnswerValue(answers)
        ans.update({'reaction time':total_time})
        ans.update(self.configurations)
        return ans

    def stoploop(self, frame):
        return frame > self.max_frame

class Instructions(object):
    """Instructions for the current experiment. It will be shown a certain
    amount of time before the start of an exeperiment."""
    def __init__(self, text, time):
        self.text = text
        self.time = time

    def show(self, win):
        """Show the instruction on the window win."""
        textstim = visual.TextStim(win, text=self.text)
        textstim.setAutoDraw(True)
        win.flip()
        core.wait(self.time)
        textstim.setAutoDraw(False)
        win.flip(clearBuffer=True)


class Experiment(object):
    """An experiment is a single condition."""
    def __init__(self):
        self.instructions = None
        self.slides = None
        self.logger = None
        self.wait_time = None
        self.win = visual.Window(winType='pyglet')

    def configure(self, instructions, slides, logger):
        self.instructions = instructions
        self.slides = slides
        self.logger = logger

    def run(self):
        """Run the preconfigured experiment."""
        self.instructions.show(self.win)
        for slide in self.slides:
            ret_val = slide.show()
            self.logger.log_trial(ret_val)
        self.logger.save_to_csv()

    def getWindow(self):
        return self.win
