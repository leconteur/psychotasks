from __future__ import print_function
from psychopy import visual, event
from experiment import ExitException, AbstractSlide, Instructions, Experiment
import random
import experiment_logger as el


def configure_nback(n_trials, positives, n_back, choices, showtime, pausetime, window):
    """Configure a nback experiment. Returns the chosen value for each trial and
    the target value."""
    configs = {'n_back':n_back, 'showtime':showtime, 'pausetime':pausetime,
               'positives':positives}
    slides = []
    for i in range(n_trials):
        if i < 3:  # There is no target in the first 3 sample
            choice = random.choice(choices)
            target = False
        else:
            choice = slides[i-n_back].value
            if random.random() < positives:
                target = True
            else:
                while choice == slides[i-n_back].value:
                    choice = random.choice(choices)
                target = False
        slide = NBackSlide(choice, target, showtime, pausetime, configs, window)
        slides.append(slide)
    return slides


class NBackSlide(AbstractSlide):
    PRESENT = 'present'
    ABSENT = 'absent'
    OMIT = 'omit'
    BOTH_ANSWERS = 'both answers'

    def __init__(self, value, target, showtime, pausetime, configurations, window):
        self.textstim = visual.TextStim(window, value)
        self.value = value
        self.target = target
        super(NBackSlide, self).__init__(showtime, pausetime, configurations, window)

    def draw(self):
        self.textstim.draw(self.window)

    def getAnswer(self, previous_answer):
        if previous_answer is None:
            previous_answer = (False, False)
        pressed_keys = event.getKeys()
        if 'q' in pressed_keys:
            raise ExitException('The participant wish to exit the application.')
        target_present = 'm' in pressed_keys or previous_answer[0]
        target_absent = 'z' in pressed_keys or previous_answer[1]
        return target_present, target_absent

    def getAnswerValue(self, answers):
        if answers[0] and answers[1]:
            ans = self.BOTH_ANSWERS
        elif answers[0]:
            ans = self.PRESENT
        elif answers[1]:
            ans = self.ABSENT
        else:
            ans = self.OMIT
        return {'participant response':ans}


if __name__ == "__main__":
    print("Testing experiment")
    instructions = Instructions("Bonjour", 4)
    experiment = Experiment()
    window = experiment.getWindow()
    letters = 'bcdfgljllmnplrstvwxz'
    slides = configure_nback(10, 0.5, 1, letters, 1, 0.5, window)
    logger = el.Logger('test.log', check_filename=False)
    experiment.configure(instructions, slides, logger)
    try:
        experiment.run()
    finally:
        window.close()
