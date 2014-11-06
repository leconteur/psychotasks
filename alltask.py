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
    return visual.Window(winType='pyglet', screen=scr, fullscr=True)

def configureLogger(filename, check_filename):
    return el.Logger(filename, check_filename=False)

def runEasyNBack(window, logger, sentinels, n_slides):
    letters = 'bcdfghjklmnpqrstvwxz'
    showtime = 1.5
    pausetime = 0.5
    positive_rate = 0.3
    instruction_text = ("Si la lettre apparaissant a l'ecran est la meme que la lettre "
                        "precedente, appuyez sur la touche 'M'. Si la lettre apparaissant a "
                        "l'ecran est differente que la lettre precedente, appuyez sur la touche "
                        "'Z'. Dans les deux cas, appuyez le plus rapidement possible.")
    instruction_text = instruction_text.decode("utf-8").encode("ascii", "replace")
    instructions = experiment.Instructions(instruction_text)
    exp = experiment.Experiment()
    slides = nback.configure_nback(n_slides, positive_rate, 1, letters, showtime, pausetime,
                                   window)
    exp.configure(instructions, slides, logger, sentinels, window)
    exp.run()


def runHardNBack(window, logger, sentinels, n_slides):
    letters = 'bcdfghjklmnpqrstvwxz'
    showtime = 1.5
    pausetime = 0.5
    positive_rate = 0.3
    instruction_text = ("Si la lettre apparaissant a l'ecran est la meme que la lettre "
                        "etant apparu sur l'avant derniere diapositive, appuyez sur la touche 'M'."
                        "Si la lettre apparaissant a l'ecran est differente que la lettre "
                        "etant apparu sur l'avant derniere diapositive, appuyez sur la touche "
                        "'Z'. Dans les deux cas, appuyez le plus rapidement possible.")
    instruction_text = instruction_text.decode("utf-8").encode("ascii", "replace")
    instructions = experiment.Instructions(instruction_text)
    exp = experiment.Experiment()
    slides = nback.configure_nback(n_slides, positive_rate, 2, letters, showtime, pausetime,
                                   window)
    exp.configure(instructions, slides, logger, sentinels, window)
    exp.run()

def runEasyMentalRotation(window, logger, sentinels, n_slides):
    exp = experiment.Experiment()
    instruction_text = ("Si les deux images sont une rotation de la meme forme, appuyez sur la "
                        "touche 'M'. S'il s'agit de deux formes differentes, appuyez sur la "
                        "touche 'Z'. Appuyez le plus rapidement possible.")
    instruction_text = instruction_text.decode("utf-8").encode("ascii", "replace")
    instructions = experiment.Instructions(instruction_text, color='black')
    slides = mentalrotation.configure_mr(n_slides, mentalrotation.EASY, 60, 1, window)
    exp.configure(instructions, slides, logger, sentinels, window)
    exp.run()

def runHardMentalRotation(window, logger, sentinels, n_slides):
    exp = experiment.Experiment()
    instruction_text = ("Si les deux images sont une rotation de la meme forme, appuyez sur la "
                        "touche 'M'. S'il s'agit de deux formes differentes, appuyez sur la "
                        "touche 'Z'. Appuyez le plus rapidement possible.")
    instruction_text = instruction_text.decode("utf-8").encode("ascii", "replace")
    instructions = experiment.Instructions(instruction_text, color='black')
    slides = mentalrotation.configure_mr(n_slides, mentalrotation.HARD, 60, 1, window)
    exp.configure(instructions, slides, logger, sentinels, window)
    exp.run()
    window.color = 'gray'
    window.flip()
    window.flip()


def runEasyVisualSearch(window, logger, sentinels, n_slides):
    exp = experiment.Experiment()
    instruction_text = ("Cliquez sur la lettre 'A' le plus rapidement possible.")
    instructions = experiment.Instructions(instruction_text)
    slideFactory = vs.VisualSearchSlideFactory(window)
    slideFactory.configure(n_distractors=40, pausetime=1, target_type='letter',
                           target_letter='A', workload='low')
    slides = slideFactory.createSlides(n_slides)
    exp.configure(instructions, slides, logger, sentinels, window)
    exp.run()

def runHardVisualSearch(window, logger, sentinels, n_slides):
    exp = experiment.Experiment()
    instruction_text = ("Cliquez sur la voyelle, blanche et non inclinnee le plus rapidement "
                        "possible.")
    instructions = experiment.Instructions(instruction_text)
    slideFactory = vs.VisualSearchSlideFactory(window)
    slideFactory.configure(n_distractors=40, pausetime=1.0, target_type='vowel',
                               distractor_colors=1, rotation=15, workload='high')
    slides = slideFactory.createSlides(n_slides)
    exp.configure(instructions, slides, logger, sentinels, window)
    exp.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run one of the task.')
    parser.add_argument('taskname', choices=['nback', 'visual_search', 'mental_rotation'], help="The task that will be run.")
    parser.add_argument('workload', choices=['low', 'high', 'practice'],
                         help="The workload level for the experimental condition.")
    parser.add_argument('participantNumber', help="The participant number.")
    parser.add_argument('--scr', type=int, default=1,
                         help="The screen (0 or 1) on which the experiment will run.")
    parser.add_argument('--noeyetracker', action="store_true",
                         help="Use this option if you do not wish to check if the eyetracker is functionnal.")
    args = parser.parse_args()
    logfile = "results/" + args.participantNumber + "/"
    logfile += args.taskname + "_" + args.workload + ".log"
    checkfilename = args.workload != 'practice'
    logger = configureLogger(logfile, checkfilename)
    window = configureWindow(args.scr)
    if args.noeyetracker is False:
        sentinels = [eyetribesentinel.EyetribeSentinel()]
    else:
        sentinels = []
    try:
        if args.taskname == 'nback':
            if args.workload == 'practice':
                runEasyNBack(window, logger, sentinels, 10)
            elif args.workload == 'low':
                runEasyNBack(window, logger, sentinels, 60)
            elif args.workload == 'high':
                runHardNBack(window, logger, sentinels, 60)
        elif args.taskname == 'visual_search':
            if args.workload == 'practice':
                runEasyVisualSearch(window, logger, sentinels, 10)
            elif args.workload == 'low':
                runEasyVisualSearch(window, logger, sentinels, 60)
            elif args.workload == 'high':
                runHardVisualSearch(window, logger, sentinels, 60)
        elif args.taskname == 'mental_rotation':
            if args.workload == 'practice':
                runEasyMentalRotation(window, logger, sentinels, 5)
            elif args.workload == 'low':
                runEasyMentalRotation(window, logger, sentinels, 60)
            elif args.workload == 'high':
                runHardMentalRotation(window, logger, sentinels, 60)
    finally:
        window.close()
        logger.save_to_csv()
        for s in sentinels:
            s.close()
