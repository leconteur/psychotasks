from __future__ import print_function
from psychopy import event
from experiment import AbstractSlide
from shapes import *
import random

shapes = [Triangle, Square, Circle]
colors = ['red', 'green', 'blue', 'black']


def configure_vs(n_slides, n_distractors, pausetime, target_color, target_type,
                 target_share_color, target_share_shape, window):
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
        slides.append(VisualSearchSlide(slideshapes[0], slideshapes[1:], pausetime, {}, window))

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

if __name__ == "__main__":
    from experiment import Instructions, Experiment
    import experiment_logger as el
    try:
        instructions = Instructions("Bonjour", 1)
        experiment = Experiment()
        window = experiment.getWindow()
        share_color = True
        share_shape = True
        slides = configure_vs(10, 30, 0.5, 'black', Triangle, share_color, share_shape, window)
        logger = el.Logger('test_mr.log', check_filename=False)
        experiment.configure(instructions, slides, logger)
        experiment.run()
    finally:
        window.close()
