from __future__ import print_function
from psychopy import event, visual
from experiment import AbstractSlide
from shapes import Triangle, Square, Circle
import random

shapes = [Triangle, Square, Circle]
colors = ['red', 'green', 'blue', 'black']


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

if __name__ == "__main__":
    from experiment import Instructions, Experiment
    import experiment_logger as el
    try:
        window = visual.Window(winType='pyglet')
        logger = el.Logger('test_vs.log', check_filename=False)
        easy_instructions = Instructions("Bonjour", 1)
        easy_experiment = Experiment()
        share_color = False
        share_shape = False
        easy_slides = configure_vs(10, 10, 0.5, 'black', Triangle, share_color,
                                   share_shape, 'easy', window)
        easy_experiment.configure(easy_instructions, easy_slides, logger, window)
        easy_experiment.run()


        shapes = [Triangle, Square, Circle]
        colors = ['red', 'black']



        hard_instructions = Instructions("Bonjour", 1)
        hard_experiment = Experiment()
        share_color = True
        share_shape = True
        hard_slides = configure_vs(10, 80, 0.5, 'black', Triangle, share_color,
                                   share_shape, 'hard', window)
        hard_experiment.configure(hard_instructions, hard_slides, logger, window)
        hard_experiment.run()
    finally:
        window.close()
        logger.save_to_csv()
