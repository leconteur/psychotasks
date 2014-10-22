from __future__ import print_function
from experiment import Instructions, Experiment, AbstractSlide, ExitException
import experiment_logger as el
from psychopy import visual, event
import random

EASY = 0
HARD = 1

def configure_mr(difficulty, showtime, pausetime, window):
    target = [random.randint(0, 1) == 1 for _ in range(10)]
    slides = []
    for t in target:
        diff = 'easy' if difficulty == EASY else 'hard'
        configs = {'showtime':showtime, 'pausetime':pausetime, 'difficulty':diff}
        slides.append(MentalRotationSlide(t, difficulty, showtime, pausetime, configs, window))
    return slides

class MentalRotationSlide(AbstractSlide):
    image_folder = "/home/olivier/Downloads/MRT library 882008/white_back/checkered/jpg/{xz}/"
    filename = image_folder + "{image_number}_{xz}_{degree}_{ab}.jpg"
    SAME = 'same'
    DIFFERENT = 'different'
    OMIT = 'omit'
    BOTH_ANSWERS = 'both answers'
    EASYRANGE = (5, 41, 5)
    HARDRANGE = (100, 171, 5)

    def __init__(self, target, difficulty, showtime, pausetime, configurations, window):
        self.difficulty = difficulty
        self.target = target
        super(MentalRotationSlide, self).__init__(showtime, pausetime, configurations, window)
        leftfile, rightfile = self.configureSlide()
        self.leftimage = visual.ImageStim(self.window, leftfile, units='norm')
        self.leftimage.setSize(1, units='norm')
        self.leftimage.setPos((-0.5, 0))
        self.rightimage = visual.ImageStim(self.window, rightfile, units='norm')
        self.rightimage.setSize(1, units='norm')
        self.rightimage.setPos((0.5, 0))
        self.response = False

    def configureSlide(self):
        lefta = random.choice([True, False])
        righta = lefta if self.target else not lefta
        leftchoice = 'a' if lefta else 'b'
        rightchoice = 'a' if righta else 'b'
        xz = random.choice(['x', 'z'])
        imagenumber = random.randint(1, 16)
        leftdegree = random.randrange(0, 360, 5)
        diff = self.getRotation()
        rightdegree = (leftdegree + diff) % 360
        leftfile = self.filename.format(image_number=imagenumber, xz=xz, ab=leftchoice,
                                        degree=leftdegree)
        rightfile = self.filename.format(image_number=imagenumber, xz=xz, ab=rightchoice,
                                         degree=rightdegree)
        self.configurations.update({'target':self.target, 'left image':leftchoice,
                                    'right image':rightchoice, 'xz':xz, 'image number':imagenumber,
                                    'left rotation':leftdegree, 'right rotation':rightdegree,
                                    'rotation difference':diff})
        return leftfile, rightfile

    def getRotation(self):
        if self.difficulty == EASY:
            rotation = self.EASYRANGE
        else:
            rotation = self.HARDRANGE
        return random.randrange(*rotation) * random.choice([-1, 1])



    def stoploop(self, frame):
        return self.response

    def draw(self):
        self.leftimage.draw(self.window)
        self.rightimage.draw(self.window)

    def getAnswer(self, previous_answer):
        if previous_answer is None:
            previous_answer = (False, False)
        pressed_keys = event.getKeys()
        if 'q' in pressed_keys:
            raise ExitException('The participant wish to exit the application.')
        target_present = 'm' in pressed_keys or previous_answer[0]
        target_absent = 'z' in pressed_keys or previous_answer[1]
        if target_present or target_absent:
            self.response = True
        return target_present, target_absent

    def getAnswerValue(self, answers):
        if answers[0] and answers[1]:
            ans = self.BOTH_ANSWERS
        elif answers[0]:
            ans = self.SAME
        elif answers[1]:
            ans = self.DIFFERENT
        else:
            ans = self.OMIT
        return {'participant response':ans}


if __name__ == "__main__":
    window = visual.Window(winType='pyglet')
    logger = el.Logger('test_mr.log', check_filename=False)

    easy_experiment = Experiment()
    easy_instructions = Instructions("Easy", 4)
    easy_slides = configure_mr(EASY, 8, 1, window)
    easy_experiment.configure(easy_instructions, easy_slides, logger, window)
    hard_experiment = Experiment()
    hard_instructions = Instructions("Hard", 4)
    hard_slides = configure_mr(HARD, 8, 1, window)
    hard_experiment.configure(hard_instructions, hard_slides, logger, window)
    try:
        easy_experiment.run()
        hard_experiment.run()
    finally:
        window.close()
        logger.save_to_csv()
