# -*- coding: utf-8 -*-
from psychopy import visual
import experiment_logger as el
import nback
import mentalrotation
import experiment
import visual_search as vs

def configureWindow():
    return visual.Window(winType='pyglet', screen=1, fullscr=True)

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
    window.color = 'gray'
    window.flip()
    window.flip()


def runEasyVisualSearch(window, logger, n_slides):
    exp = experiment.Experiment()
    instruction_text = ("Cliquez sur la lettre 'A' le plus rapidement possible.")
    instructions = experiment.Instructions(instruction_text, 5)
    slideFactory = vs.VisualSearchSlideFactory(window)
    slideFactory.configure(n_distractors=40, pausetime=1, target_type='letter',
                           target_letter='A', workload='low')
    slides = slideFactory.createSlides(n_slides)
    exp.configure(instructions, slides, logger, window)
    exp.run()

def runHardVisualSearch(window, logger, n_slides):
    exp = experiment.Experiment()
    instruction_text = ("Cliquez sur la voyelle, blanche et non inclinnee le plus rapidement "
                        "possible.")
    instructions = experiment.Instructions(instruction_text, 5)
    slideFactory = vs.VisualSearchSlideFactory(window)
    slideFactory.configure(n_distractors=40, pausetime=1.0, target_type='vowel',
                               distractor_colors=2, rotation=15, workload='high')
    slides = slideFactory.createSlides(n_slides)
    exp.configure(instructions, slides, logger, window)
    exp.run()


if __name__ == "__main__":
    try:
        window = configureWindow()
        logger = configureLogger("testall.log")
        runEasyNBack(window, logger, 60)
        runHardNBack(window, logger, 60)
        runEasyMentalRotation(window, logger, 50)
        runHardMentalRotation(window, logger, 50)
        runEasyVisualSearch(window, logger, 50)
        runHardVisualSearch(window, logger, 50)
    finally:
        window.close()
        logger.save_to_csv()
