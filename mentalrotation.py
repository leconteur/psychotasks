from __future__ import print_function
from experiment import Instructions, Experiment, AbstractSlide, ExitException
import experiment_logger as el
from psychopy import visual, event
import random

EASY = 0
HARD = 1

def configure_mr(nslides, difficulty, showtime, pausetime, window):
    target = [random.randint(0, 1) == 1 for _ in range(nslides)]
    slides = []
    try:
        fr = 1/window.getActualFrameRate()
    except TypeError:
        fr = 1/60.0
    for t in target:
        diff = 'low' if difficulty == EASY else 'high'
        configs = {'showtime':showtime, 'pausetime':pausetime, 'workload':diff}
        slides.append(MentalRotationSlide(t, difficulty, showtime, pausetime, configs, window, fr))
    return slides

class MentalRotationSlide(AbstractSlide):
    image_folder = "../MentalRotationLibrary/white_back/checkered/jpg/{xz}/"
    filename = image_folder + "{image_number}_{xz}_{degree}_{ab}.jpg"
    SAME = 'same'
    DIFFERENT = 'different'
    OMIT = 'omit'
    BOTH_ANSWERS = 'both answers'
    EASYRANGE = (5, 41, 5)
    HARDRANGE = (125, 171, 5)

    def __init__(self, target, difficulty, showtime, pausetime, configurations, window, fr):
        self.difficulty = difficulty
        self.target = target
        super(MentalRotationSlide, self).__init__(showtime, pausetime, configurations, window, fr)
        window.setColor('white')
        window.flip()
        window.flip()
        leftfile, rightfile = self.configureSlide()
        self.leftimage = visual.ImageStim(self.window, leftfile, units='norm')
        self.leftimage.setSize(1, units='norm')
        self.leftimage.setPos((-0.5, 0))
        self.rightimage = visual.ImageStim(self.window, rightfile, units='norm')
        self.rightimage.setSize(1, units='norm')
        self.rightimage.setPos((0.5, 0))
        self.response = False
        self.reminder = visual.TextStim(window, text="Pareil: 'M'\nDifferent: 'Z'",
                                        pos=(-0.85, -0.90), height=0.04, color='black')

    def configureSlide(self):
        lefta = random.choice([True, False])
        righta = lefta if self.target else not lefta
        leftchoice = 'a' if lefta else 'b'
        rightchoice = 'a' if righta else 'b'
        xz = random.choice(['x', 'z'])
        imagenumber = random.randint(1, 16)
        leftdegree = random.randrange(5, 360, 5)
        if leftdegree == 90 or leftdegree == 180 or leftdegree == 270:
            leftdegree += 5
        diff = self.getRotation()
        rightdegree = (leftdegree + diff) % 360
        if rightdegree == 0 or rightdegree == 90 or rightdegree == 180 or rightdegree == 270 or rightdegree == 360:
            rightdegree = (rightdegree + 5) % 360
        leftfile = self.filename.format(image_number=imagenumber, xz=xz, ab=leftchoice,
                                        degree=leftdegree)
        rightfile = self.filename.format(image_number=imagenumber, xz=xz, ab=rightchoice,
                                         degree=rightdegree)
        self.configurations.update({'target':self.target, 'left image':leftchoice,
                                    'right image':rightchoice, 'xz':xz, 'image number':imagenumber,
                                    'left rotation':leftdegree, 'right rotation':rightdegree,
                                    'rotation difference':diff, 'taskname':'mental rotation'})
        return leftfile, rightfile

    def getRotation(self):
        if self.difficulty == EASY:
            rotation = self.EASYRANGE
        else:
            rotation = self.HARDRANGE
        return random.randrange(*rotation) * random.choice([-1, 1])



    def stoploop(self):
        return self.response

    def draw(self):
        self.leftimage.draw(self.window)
        self.rightimage.draw(self.window)
        self.reminder.draw(self.window)

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
    easy_instructions = Instructions("Easy", 4, color='black')
    easy_slides = configure_mr(30, EASY, 8, 1, window)
    easy_experiment.configure(easy_instructions, easy_slides, logger, window)
    hard_experiment = Experiment()
    hard_instructions = Instructions("Hard", 4, color='black')
    hard_slides = configure_mr(30, HARD, 8, 1, window)
    hard_experiment.configure(hard_instructions, hard_slides, logger, window)
    try:
        easy_experiment.run()
        hard_experiment.run()
    finally:
        window.close()
        logger.save_to_csv()
