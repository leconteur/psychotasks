# -*- coding: utf-8 -*-
from psychopy import visual
import experiment_logger as el
import nback
import mentalrotation
import experiment
import visual_search as vs
import argparse
import eyetribesentinel


def configureWindow(scr):
    return visual.Window(screen=scr, fullscr=True)


def configureLogger(filename, check_filename):
    return el.Logger(filename, check_filename=False)


def runEasyNBack(window, logger, sentinels, n_slides, sound_prob):
    letters = 'bcdfghjklmnpqrstvwxz'
    showtime = 2.0
    pausetime = 0.5
    positive_rate = 0.3
    instruction_text = ("Si la lettre apparaissant a l'ecran est la meme que la lettre "
                        "precedente, appuyez sur la touche 'M'. \n\n"
                        "Sinon, appuyez sur la touche 'Z'.\n\n"
                        "Dans les deux cas, appuyez le plus rapidement possible.\n\n"
                        "Appuyez sur 'entree' pour commencer.")
    instruction_text = instruction_text.decode("utf-8").encode("ascii", "replace")
    instructions = experiment.Instructions(instruction_text)
    exp = experiment.Experiment()
    slides = nback.configure_nback(n_slides, positive_rate, 1, letters, showtime, pausetime,
                                   sound_prob, window)
    exp.configure(instructions, slides, logger, sentinels, window)
    exp.run()


def runHardNBack(window, logger, sentinels, n_slides, sound_prob):
    letters = 'bcdfghjklmnpqrstvwxz'
    showtime = 2.0
    pausetime = 0.5
    positive_rate = 0.3
    instruction_text = ("Si la lettre apparaissant a l'ecran est la meme que l'avant derniere "
                        "lettre, appuyez sur la touche 'M'. \n\n"
                        "Sinon, appuyez sur la touche 'Z'.\n\n"
                        "Dans les deux cas, appuyez le plus rapidement possible.\n\n"
                        "Appuyez sur 'entree' pour commencer.")
    instruction_text = instruction_text.decode("utf-8").encode("ascii", "replace")
    instructions = experiment.Instructions(instruction_text)
    exp = experiment.Experiment()
    slides = nback.configure_nback(n_slides, positive_rate, 2, letters, showtime, pausetime,
                                   sound_prob, window)
    exp.configure(instructions, slides, logger, sentinels, window)
    exp.run()


def runEasyMentalRotation(window, logger, sentinels, n_slides):
    exp = experiment.Experiment()
    instruction_text = ("Si les deux images sont une rotation de la meme forme, appuyez sur la "
                        "touche 'M'.\n\nSinon, appuyez sur la "
                        "touche 'Z'.\n\nAppuyez le plus rapidement possible."
                        "\nAppuyez sur 'entree' pour commencer.")
    instruction_text = instruction_text.decode("utf-8").encode("ascii", "replace")
    instructions = experiment.Instructions(instruction_text, color='black')
    slides = mentalrotation.configure_mr(n_slides, mentalrotation.EASY, 60, 1, window)
    exp.configure(instructions, slides, logger, sentinels, window)
    exp.run()


def runHardMentalRotation(window, logger, sentinels, n_slides):
    exp = experiment.Experiment()
    instruction_text = ("Si les deux images sont une rotation de la meme forme, appuyez sur la "
                        "touche 'M'.\n\nSinon, appuyez sur la "
                        "touche 'Z'.\n\nAppuyez le plus rapidement possible."
                        "\nAppuyez sur 'entree' pour commencer.")
    instruction_text = instruction_text.decode("utf-8").encode("ascii", "replace")
    instructions = experiment.Instructions(instruction_text, color='black')
    slides = mentalrotation.configure_mr(n_slides, mentalrotation.HARD, 60, 1, window)
    exp.configure(instructions, slides, logger, sentinels, window)
    exp.run()
    window.color = 'gray'
    window.flip()
    window.flip()


def runEasyVisualSearch(window, logger, sentinels, n_slides, soundprob, soundtime):
    exp = experiment.Experiment()
    instruction_text = ("Cliquez sur la lettre 'A' le plus rapidement possible.\nAppuyez sur "
                        "'entree' pour commencer")
    instructions = experiment.Instructions(instruction_text)
    slideFactory = vs.VisualSearchSlideFactory(window)
    slideFactory.configure(n_distractors=40, pausetime=1, target_type='letter',
                           target_letter='A', workload='low', sound_probability=soundprob,
                           soundtime=soundtime)
    slides = slideFactory.createSlides(n_slides)
    exp.configure(instructions, slides, logger, sentinels, window)
    exp.run()


def runHardVisualSearch(window, logger, sentinels, n_slides, soundprob, soundtime):
    exp = experiment.Experiment()
    instruction_text = ("Cliquez sur la voyelle (A,E,I,O,U,Y) non inclinnee le plus rapidement "
                        "possible.\nAppuyez sur 'entree' pour commencer.")
    instructions = experiment.Instructions(instruction_text)
    slideFactory = vs.VisualSearchSlideFactory(window)
    slideFactory.configure(n_distractors=40, pausetime=1.0, target_type='vowel',
                           distractor_colors=1, rotation=15, workload='high',
                           sound_probability=soundprob, soundtime=soundtime)
    slides = slideFactory.createSlides(n_slides)
    exp.configure(instructions, slides, logger, sentinels, window)
    exp.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run one of the task.')
    parser.add_argument('taskname', choices=['nback', 'visual_search', 'mental_rotation'],
                        help="The task that will be run.")
    parser.add_argument('workload', choices=['low', 'high'],
                        help="The workload level for the experimental condition.")
    parser.add_argument('participantNumber', help="The participant number.")
    parser.add_argument('--practice', action='store_true', help="Only do a subset of the task")
    parser.add_argument('--soundprobwrong', type=float, default=0.0,
                        help=("The probability that a sound will be played if the wrong answer is "
                              "given or that the answer is not provided soon enough. This must be "
                              "a number between 0 and 1."))
    parser.add_argument('--soundprobright', type=float, default=0.0,
                        help=("The probability that a sound will be played if the right answer is "
                              "given. This must be a number between 0 and 1."))
    parser.add_argument('--soundtime', type=float, default=2.0,
                        help=("The time threshold from which a sound can be played in the visual "
                              "search task."))
    parser.add_argument('--scr', type=int, default=1,
                        help="The screen (0 or 1) on which the experiment will run.")
    parser.add_argument('--eyetracker', action="store_true",
                        help=("Use this option if you do not wish to check if the eyetracker "
                              "is functionnal."))
    args = parser.parse_args()
    args.soundprob = (args.soundprobright, args.soundprobwrong)
    logfile = "results/" + args.participantNumber + "/"
    logfile += args.taskname + "_" + args.workload
    if args.practice:
        logfile += "_practice"
    logfile += ".log"
    checkfilename = args.workload != 'practice'
    logger = configureLogger(logfile, checkfilename)
    window = configureWindow(args.scr)
    if args.eyetracker is True:
        sentinels = [eyetribesentinel.EyetribeSentinel()]
    else:
        sentinels = []
    try:
        ntrials = 10 if args.practice else 60
        if args.taskname == 'nback':
            if args.workload == 'low':
                runEasyNBack(window, logger, sentinels, ntrials, args.soundprob)
            elif args.workload == 'high':
                runHardNBack(window, logger, sentinels, ntrials, args.soundprob)
        elif args.taskname == 'visual_search':
            if args.soundprobright != 0.0:
                raise NotImplementedError("The sound probability is only for wrong values")
            if args.workload == 'low':
                runEasyVisualSearch(window, logger, sentinels, ntrials, args.soundprobwrong, args.soundtime)
            elif args.workload == 'high':
                runHardVisualSearch(window, logger, sentinels, ntrials, args.soundprobwrong, args.soundtime)
        elif args.taskname == 'mental_rotation':
            if args.soundprob != (0.0, 0.0):
                raise NotImplementedError('The sound playing is not implemented for this task.')
            if args.workload == 'low':
                runEasyMentalRotation(window, logger, sentinels, ntrials)
            elif args.workload == 'high':
                runHardMentalRotation(window, logger, sentinels, ntrials)
    finally:
        window.close()
        logger.save_to_csv()
        for s in sentinels:
            s.close()
