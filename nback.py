from __future__ import print_function
from psychopy import visual, event
from experiment import ExitException, AbstractSlide, Instructions, Experiment
import random
import experiment_logger as el


def configure_nback(n_trials, positives, n_back, choices, showtime, pausetime, window):
    """Configure a nback experiment. Returns the chosen value for each trial and
    the target value."""

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
        workload = 'low' if n_back <= 1 else 'high'
        configs = {'n_back':n_back, 'showtime':showtime, 'pausetime':pausetime,
                   'positives':positives, 'target':target, 'taskname':'nback',
                   'workload':workload}
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
        if not pressed_keys:
            return previous_answer
        if 'q' in pressed_keys:
            raise ExitException('The participant wish to exit the application.')
        print(pressed_keys)
        present_keys = ['m', 'n', 'j', 'k', 'l', 'comma', 'period', 'b', 'h']
        absent_keys = ['a', 's', 'x', u'\xab', 'c', 'd']
        target_present = previous_answer[0] or any(key in pressed_keys for key in present_keys)
        target_absent = previous_answer[1] or any(key in pressed_keys for key in absent_keys)
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
    letters = 'bcdfgljllmnplrstvwxz'
    showtime = 1
    pausetime = 0.5
    nslides = 10
    positive_rate = 0.3
    window = visual.Window(winType='pyglet')
    logger = el.Logger('test.log', check_filename=False)

    easy_instructions = Instructions("1-back", 4)
    easy_experiment = Experiment()
    easy_slides = configure_nback(nslides, positive_rate, 1, letters, showtime, pausetime, window)
    easy_experiment.configure(easy_instructions, easy_slides, logger, window)

    hard_instructions = Instructions("2-back", 4)
    hard_experiment = Experiment()
    hard_slides = configure_nback(nslides, positive_rate, 2, letters, showtime, pausetime, window)
    hard_experiment.configure(hard_instructions, hard_slides, logger, window)
    try:
        easy_experiment.run()
        hard_experiment.run()
    finally:
        window.close()
        logger.save_to_csv()
