

if __name__ == "__main__":
    try:
        window = configureWindow()
        logger = configureLogger()
        runEasyNBack(window, logger)
        runHardNBack(window, logger)
        runEasyMentalRotation(window, logger)
        runHardMentalRotation(window, logger)
        runEasyVisualSearch(window, logger)
        runHardVisualSearch(window, logger)
    finally:
        window.close()
        logger.savetocsv()

