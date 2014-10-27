from __future__ import print_function
from psychopy import event, visual
from experiment import AbstractSlide
from shapes import Triangle, Square, Circle
from numpy.linalg import norm
import numpy as np
import random
import string

shapes = [Triangle, Square, Circle]
colors = ['red', 'green', 'blue', 'black']


class Letter(visual.TextStim):
    def contains(self, other):
        return norm(self.pos - other.getPos()) < 0.07

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
            if norm(dist.pos - pos) < 0.05:
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

def configure_vs(n_slides, n_distractors, pausetime, target_color, target_type,
                 target_share_color, target_share_shape, experiment_id, window):
    slides = []
    for _ in range(n_slides):
        slideshapes = []
        slideshapes.append(target_type(window, target_color, getRandomPos()))
        while len(slideshapes) <= n_distractors:
            shape, color = getRandomShape(target_type, target_color)
            if color_invalid(target_color, color, target_share_color):
                continue
            if shape_invalid(target_type, shape, target_share_shape):
                continue
            distractor = shape(window, color, getRandomPos())
            if not contains(slideshapes, distractor):
                slideshapes.append(distractor)
        configs = {'n_distractors':n_distractors, 'pausetime':pausetime,
                   'target_color':target_color, 'target_type':target_type.name,
                   'target share color':target_share_color, 'target_share_type':target_share_shape,
                   'experiment id': experiment_id}
        slides.append(VisualSearchSlide(slideshapes[0], slideshapes[1:], pausetime,
                                        configs, window))

    return slides


def color_invalid(target_color, color, target_share_color):
    return target_color == color and target_share_color is False


def shape_invalid(target_type, shape, target_share_shape):
    return target_type == shape and target_share_shape is False


def getRandomShape(target_shape, target_color):
    color, shape = target_color, target_shape
    while color == target_color and shape == target_shape:
        color = random.choice(colors)
        shape = random.choice(shapes)
    return shape, color


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
        window = visual.Window(winType='pyglet', fullscr=True, waitBlanking=True)
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


def main_shapes():
    from experiment import Instructions, Experiment
    import experiment_logger as el
    try:
        window = visual.Window(winType='pyglet')
        logger = el.Logger('test_vs.log', check_filename=False)
        easy_instructions = Instructions("Bonjour", 1)
        easy_experiment = Experiment()
        share_color = False
        share_shape = False
        easy_slides = configure_vs(30, 10, 0.5, 'black', Triangle, share_color,
                                   share_shape, 'easy', window)
        easy_experiment.configure(easy_instructions, easy_slides, logger, window)
        easy_experiment.run()

        shapes = [Triangle, Square, Circle]
        colors = ['red', 'black']

        hard_instructions = Instructions("Bonjour", 1)
        hard_experiment = Experiment()
        share_color = True
        share_shape = True
        hard_slides = configure_vs(30, 80, 0.5, 'black', Triangle, share_color,
                                   share_shape, 'hard', window)
        hard_experiment.configure(hard_instructions, hard_slides, logger, window)
        hard_experiment.run()
    finally:
        window.close()
        logger.save_to_csv()

if __name__ == "__main__":
    # main_shapes()
    main_letters()
