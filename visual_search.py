from __future__ import print_function
from psychopy import event, visual
from experiment import AbstractSlide
from shapes import Triangle, Square, Circle
from numpy.linalg import norm
import numpy as np
import random
import string


class Letter(visual.TextStim):
    def contains(self, other):
        return norm(self.pos - other.getPos()) < 0.05


class ConfigurationError(Exception): pass


class VisualSearchSlideFactory(object):
    TARGET_TYPES = ["vowel", "consonnant", "letter"]

    TARGETS = {"vowel":list("AEIOUY"), "consonnant":list("BCDFGHJKLMNPQRSTVWXZ")}
    COLORS = ['white', 'black', 'red', 'green', 'blue']

    def __init__(self, window):
        self.window = window
        self.configurations = {}

    def configure(self, **kwargs):
        self.configurations.update(**kwargs)

    def createSlides(self, n_slides):
        try:
            return [self.createSlide() for _ in range(n_slides)]
        except KeyError as e:
            raise ConfigurationError("The factory was not configured correctly. "
                                     "Please configure the following option: {}".format(e.args[0]))

    def createSlide(self):
        self.createTarget()
        self.createDistractors()
        return VisualSearchSlide(self.target, self.distractors, self.configurations['pausetime'],
                                 self.configurations, self.window)

    def createTarget(self):
        if self.configurations['target_type'] == "letter":
            text = self.configurations['target_letter']
        else:
            text = random.choice(self.TARGETS[self.configurations['target_type']])
        target_color = self.configurations.get('color', 'white')
        pos = getRandomPos()
        self.target = Letter(self.window, text=text, pos=pos, color=target_color)

    def createDistractors(self):
        self.distractors = []
        while len(self.distractors) < self.configurations['n_distractors']:
            self.createDistractor()

    def createDistractor(self):
        pos = getRandomPos()
        for dist in self.distractors + [self.target]:
            if norm(dist.pos - pos) < 0.1:
                return
        text = random.choice(string.ascii_uppercase)
        color = random.choice(self.COLORS[0:self.configurations.get('distractor_colors', 1)])
        rotation = random.choice([-1, 0, 1]) * self.configurations.get('rotation', 0)
        distractor = Letter(self.window, text=text, pos=pos, color=color, ori=rotation)
        if self.equivalentLetter(self.target, distractor):
            return
        self.distractors.append(distractor)

    def equivalentLetter(self, letter_a, letter_b):
        if np.array_equal(letter_a.color, letter_b.color) and letter_a.ori == letter_b.ori:
            if self.configurations['target_type'] == 'letter':
                return letter_a.text == letter_b.text
            else:
                letters = self.TARGETS[self.configurations['target_type']]
                return letter_a.text in letters and letter_b.text in letters
        else:
            return False




def getRandomPos():
    return random.uniform(-0.95, 0.95), random.uniform(-0.95, 0.95)


def contains(shapelist, shape):
    return any(s.overlaps(shape) for s in shapelist)


class VisualSearchSlide(AbstractSlide):
    def __init__(self, target, distractors, pausetime, configurations, window):
        super(VisualSearchSlide, self).__init__(600, pausetime, configurations, window)
        self.mouse = event.Mouse()
        self.target = target
        self.distractors = distractors
        self.response = False

    def draw(self):
        self.target.draw(self.window)
        for distractor in self.distractors:
            distractor.draw(self.window)

    def getAnswer(self, previous_answer):
        self.response = self.mouse.isPressedIn(self.target)
        return (self.response, )

    def stoploop(self, frame):
        return self.response

    def getAnswerValue(self, answer):
        return {'pressed':True}


def main_letters():
    from experiment import Instructions, Experiment
    import experiment_logger as el
    try:
        window = visual.Window(winType='pyglet', fullscr=True, waitBlanking=True, screen=1)
        logger = el.Logger('test_vs.log', check_filename=False)
        easy_instructions = Instructions("Bonjour", 1)
        easy_experiment = Experiment()
        slideFactory = VisualSearchSlideFactory(window)
        slideFactory.configure(n_distractors=40, pausetime=1.0, target_type='vowel',
                               distractor_colors=2, rotation=15, difficulty='high')
        easy_slides = slideFactory.createSlides(30)
        easy_experiment.configure(easy_instructions, easy_slides, logger, window)
        easy_experiment.run()

        hard_instructions = Instructions("Allo", 1)
        hard_experiment = Experiment()
        slideFactory = VisualSearchSlideFactory(window)
        slideFactory.configure(n_distractors=40, pausetime=1.0, target_type='letter',
                                    target_letter='A', difficulty='low')
        hard_slides = slideFactory.createSlides(30)
        hard_experiment.configure(hard_instructions, hard_slides, logger, window)
        hard_experiment.run()
    finally:
        window.close()
        logger.save_to_csv()

if __name__ == "__main__":
    main_letters()
