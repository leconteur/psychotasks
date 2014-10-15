from __future__ import print_function
from experiment import Instructions, Experiment, AbstractSlide, ExitException
import experiment_logger as el
from psychopy import visual, event
import random

def configure_mr(showtime, pausetime, window):
    configs = {'showtime':showtime, 'pausetime':pausetime}
    target = [random.randint(0, 1) == 1 for _ in range(10)]
    return [MentalRotationSlide(t, showtime, pausetime, configs, window) for t in target]

class MentalRotationSlide(AbstractSlide):
    image_folder = "/home/olivier/Downloads/MRT library 882008/white_back/checkered/jpg/{xz}/"
    filename = image_folder + "{image_number}_{xz}_{degree}_{ab}.jpg"

    def __init__(self, target, showtime, pausetime, configurations, window):
        super(MentalRotationSlide, self).__init__(showtime, pausetime, configurations, window)
        self.target = target
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
        diff = random.randrange(5, 41, 5) * random.choice([-1, 1])
        rightdegree = (leftdegree + diff) % 360
        leftfile = self.filename.format(image_number=imagenumber, xz=xz, ab=leftchoice,
                                        degree=leftdegree)
        rightfile = self.filename.format(image_number=imagenumber, xz=xz, ab=rightchoice,
                                         degree=rightdegree)
        self.configurations.update({'target present':self.target,'left image':leftchoice,
                                    'right image':rightchoice, 'xz':xz, 'image number':imagenumber,
                                    'left rotation':leftdegree, 'right rotation':rightdegree,
                                    'rotation difference':diff})
        return leftfile, rightfile


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

    def getAnswerValue(self, answer):
        return {'placeholder':2}

if __name__ == "__main__":
    instructions = Instructions("Bonjour", 1)
    experiment = Experiment()
    window = experiment.getWindow()
    letters = 'bcdfgljllmnplrstvwxz'
    slides = configure_mr(8, 1, window)
    logger = el.Logger('test_mr.log', check_filename=False)
    experiment.configure(instructions, slides, logger)
    try:
        experiment.run()
    finally:
        window.close()
