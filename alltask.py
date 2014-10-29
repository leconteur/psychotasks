# -*- coding: utf-8 -*-
from psychopy import visual
import experiment_logger as el
import nback
import mentalrotation
import experiment

def configureWindow():
    return visual.Window(winType='pyglet', screen=1)

def configureLogger(filename):
    return el.Logger(filename, check_filename=False)

def runEasyNBack(window, logger, n_slides):
    letters = 'bcdfghjklmnpqrstvwxz'
    showtime = 1.5
    pausetime = 0.5
    positive_rate = 0.3
    instruction_text = ("Si la lettre apparaissant a l'ecran est la meme que la lettre "
                        "precedente, appuyez sur la touche 'M'. Si la lettre apparaissant a "
                        "l'ecran est differente que la lettre precedente, appuyez sur la touche "
                        "'Z'. Dans les deux cas, appuyez le plus rapidement possible.")
    instruction_text = instruction_text.decode("utf-8").encode("ascii", "replace")
    instructions = experiment.Instructions(instruction_text, 5)
    exp = experiment.Experiment()
    slides = nback.configure_nback(n_slides, positive_rate, 1, letters, showtime, pausetime,
                                   window)
    exp.configure(instructions, slides, logger, window)
    exp.run()


def runHardNBack(window, logger, n_slides):
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
    instructions = experiment.Instructions(instruction_text, 5)
    exp = experiment.Experiment()
    slides = nback.configure_nback(n_slides, positive_rate, 2, letters, showtime, pausetime,
                                   window)
    exp.configure(instructions, slides, logger, window)
    exp.run()

def runEasyMentalRotation(window, logger, n_slides):
    exp = experiment.Experiment()
    instruction_text = ("Si les deux images sont une rotation de la meme forme, appuyez sur la "
                        "touche 'M'. S'il s'agit de deux formes differentes, appuyez sur la "
                        "touche 'Z'. Appuyez le plus rapidement possible.")
    instruction_text = instruction_text.decode("utf-8").encode("ascii", "replace")
    instructions = experiment.Instructions(instruction_text, 5, color='black')
    slides = mentalrotation.configure_mr(n_slides, mentalrotation.EASY, 60, 1, window)
    exp.configure(instructions, slides, logger, window)
    exp.run()

def runHardMentalRotation(window, logger, n_slides):
    exp = experiment.Experiment()
    instruction_text = ("Si les deux images sont une rotation de la meme forme, appuyez sur la "
                        "touche 'M'. S'il s'agit de deux formes differentes, appuyez sur la "
                        "touche 'Z'. Appuyez le plus rapidement possible.")
    instruction_text = instruction_text.decode("utf-8").encode("ascii", "replace")
    instructions = experiment.Instructions(instruction_text, 5, color='black')
    slides = mentalrotation.configure_mr(n_slides, mentalrotation.HARD, 60, 1, window)
    exp.configure(instructions, slides, logger, window)
    exp.run()


def runEasyVisualSearch(window, logger):
    pass

def runHardVisualSearch(window, logger):
    pass

if __name__ == "__main__":
    try:
        window = configureWindow()
        logger = configureLogger("testall.log")
        runEasyNBack(window, logger, 10)
        runHardNBack(window, logger, 10)
        runEasyMentalRotation(window, logger, 10)
        runHardMentalRotation(window, logger, 10)
        runEasyVisualSearch(window, logger)
        runHardVisualSearch(window, logger)
    finally:
        window.close()
        logger.save_to_csv()
