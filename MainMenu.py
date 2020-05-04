# Team 9 RISK

import os
import pygame

from pygame.locals import *
from setupGame import SetupGame
from runGame import RunGame
import constants as c

# Initializes game menu layers and provides start point for user
class Menu():

    # initialize the menu with buttons
    def __init__(self, MENUSTAT, screen, clock, background1):
        self.playButton = pygame.image.load(c.imagePath + c.playButton)
        self.helpButton = pygame.image.load(c.imagePath + c.helpButton)
        self.exitButton = pygame.image.load(c.imagePath + c.exitButton)
        self.MENUSTAT = MENUSTAT
        self.screen = screen
        self.clock = clock
        self.background1 = background1
        self.fpsClock = pygame.time.Clock()


    # Returns information for text handling
    def textArea(self, text, font, color=(0, 0, 0)):
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()

    # Resizes and sends button images to display
    def formatButtons(self, menu, animateMenuX):
        formattedPlayButton = pygame.transform.scale(self.playButton, (100, 50))  # size change
        formattedHelpButton = pygame.transform.scale(self.helpButton, (100, 50))  # size change
        formattedExitButton = pygame.transform.scale(self.exitButton, (100, 50))  # size change

        self.screen.blit(menu, (animateMenuX, 0))  # add to layer starting left top corner position
        self.screen.blit(formattedPlayButton,
                         (c.windowLength - int(c.windowLength / 2) - 250, c.windowWidth - int(c.windowWidth / 5)))
        self.screen.blit(formattedHelpButton,
                         (c.windowLength - int(c.windowLength / 2), c.windowWidth - int(c.windowWidth / 5)))  # middle
        self.screen.blit(formattedExitButton,
                         (c.windowLength - int(c.windowLength / 2) + 250, c.windowWidth - int(c.windowWidth / 5)))

        return formattedPlayButton, formattedHelpButton, formattedExitButton

    # Positions buttons accordingly depending on window dimensions
    def placeButtons(self, currentMouseX, currentMouseY, formattedPlayButton, formattedHelpButton, formattedExitButton):

        # if lowerbound < mousepos < higher bound and for y.. do button
        # difference is button size formatted
        if ((c.windowLength - int(c.windowLength / 2) - 250) < currentMouseX < (
                c.windowLength - int(c.windowLength / 2) - 150)) and (
                (c.windowWidth - int(c.windowWidth / 5)) < currentMouseY < (
                c.windowWidth - int(c.windowWidth / 5) + 50)):
            self.screen.blit(formattedPlayButton,
                             (c.windowLength - int(c.windowLength / 2) - 250, c.windowWidth - int(c.windowWidth / 5)),
                             special_flags=pygame.BLEND_RGBA_MULT)
        elif ((c.windowLength - int(c.windowLength / 2)) < currentMouseX < (
                c.windowLength - int(c.windowLength / 2) + 100)) and (
                (c.windowWidth - int(c.windowWidth / 5)) < currentMouseY < (
                c.windowWidth - int(c.windowWidth / 5) + 50)):
            self.screen.blit(formattedHelpButton,
                             (c.windowLength - int(c.windowLength / 2), c.windowWidth - int(c.windowWidth / 5)),
                             special_flags=pygame.BLEND_RGBA_MULT)  # middle
        elif ((c.windowLength - int(c.windowLength / 2) + 250) < currentMouseX < (
                c.windowLength - int(c.windowLength / 2) + 350)) and (
                (c.windowWidth - int(c.windowWidth / 5)) < currentMouseY < (
                c.windowWidth - int(c.windowWidth / 5) + 50)):
            self.screen.blit(formattedExitButton,
                             (c.windowLength - int(c.windowLength / 2) + 250, c.windowWidth - int(c.windowWidth / 5)),
                             special_flags=pygame.BLEND_RGBA_MULT)

    # Screen for when user presses settings option
    def settings(self, SETTINGSTAT):
        # flag true for options
        pygame.init()
        while SETTINGSTAT == True:
            mouse = pygame.mouse.get_pos()
            currentMouseX = mouse[0]
            currentMouseY = mouse[1]

            # Button visual and function
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:

                    # On right click on help (OPTIONS should rename latre)
                    if (event.button == 1) and ((c.windowLength - int(c.windowLength / 2)) < currentMouseX < (
                            c.windowLength - int(c.windowLength / 2) + 100)) and (
                            (c.windowWidth - int(c.windowWidth / 5)) < currentMouseY < (
                            c.windowWidth - int(c.windowWidth / 5) + 50)):
                        print("returning to menu")
                        SETTINGSTAT = False

            # Load settings screen
            settingsScreen = pygame.image.load(c.imagePath + c.settingsImage)
            formattedSettingsScreen = pygame.transform.scale(settingsScreen, (c.windowLength, c.windowWidth))
            formattedExitButton = pygame.transform.scale(self.helpButton, (100, 50))  # size change

            self.screen.blit(formattedSettingsScreen, (0, 0))

            # Create text and add to screen on visuals
            margin = 100
            tempText = pygame.font.Font(None, 50)
            textPosition = (int(c.windowLength / 5), margin)
            textSurface, textBox = self.textArea("In Risk you must conquer all the territories to win.", tempText, c.white)
            textBox.topleft = textPosition
            self.screen.blit(textSurface, textBox)

            textPosition = (int(c.windowLength / 5), margin + 100)
            textSurface, textBox = self.textArea("Players will be given set troops and starting territories.", tempText,
                                            c.white)
            textBox.topleft = textPosition
            self.screen.blit(textSurface, textBox)

            textPosition = (int(c.windowLength / 5), margin + 200)
            textSurface, textBox = self.textArea("Use the 'h' key ingame for control help ... Good Luck.", tempText, c.white)
            textBox.topleft = textPosition
            self.screen.blit(textSurface, textBox)

            if ((c.windowLength - int(c.windowLength / 2)) < currentMouseX < (
                    c.windowLength - int(c.windowLength / 2) + 100)) and (
                    (c.windowWidth - int(c.windowWidth / 5)) < currentMouseY < (
                    c.windowWidth - int(c.windowWidth / 5) + 50)):
                self.screen.blit(formattedExitButton,
                            (c.windowLength - int(c.windowLength / 2), c.windowWidth - int(c.windowWidth / 5)),
                            special_flags=pygame.BLEND_RGBA_MULT)  # middle
            else:
                self.screen.blit(formattedExitButton, (
                c.windowLength - int(c.windowLength / 2), c.windowWidth - int(c.windowWidth / 5)))  # middle

            pygame.display.update()
            self.fpsClock.tick(30) # Used to limit window frames to prevent lagging

    # Checks user interactions with mouse and keyboard
    def eventGetter(self, currentMouseX, currentMouseY, numPlayers, numAI):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN: # On right click on play button start game
                if (event.button == 1) and ((c.windowLength - int(c.windowLength / 2) - 250) < currentMouseX < (
                        c.windowLength - int(c.windowLength / 2) - 150)) and (
                        (c.windowWidth - int(c.windowWidth / 5)) < currentMouseY < (
                        c.windowWidth - int(c.windowWidth / 5) + 50)):
                    print("Starting game ...")
                    menu = False
                    running = True

                    # Prep load screen while game inits
                    loadScreen = pygame.image.load(c.imagePath + c.loadingImage)
                    formattedLoadScreen = pygame.transform.scale(loadScreen, (c.windowLength, c.windowWidth))
                    self.screen.blit(formattedLoadScreen, (0, 0))
                    pygame.display.update()  # update visuals
                    
                    # Initialize game setup
                    sGame = SetupGame(running, self.screen, self.background1, self.clock)
                    sGame.startGame(numPlayers, running, self.screen, self.background1, self.clock, numAI)

                # On right click on help/options button
                elif (event.button == 1) and ((c.windowLength - int(c.windowLength / 2)) < currentMouseX < (
                        c.windowLength - int(c.windowLength / 2) + 100)) and (
                        (c.windowWidth - int(c.windowWidth / 5)) < currentMouseY < (
                        c.windowWidth - int(c.windowWidth / 5) + 50)):
                    print("opening options ...")
                    self.settings(True)

                # On right click on exit button
                elif (event.button == 1) and ((c.windowLength - int(c.windowLength / 2) + 250) < currentMouseX < (
                        c.windowLength - int(c.windowLength / 2) + 350)) and (
                        (c.windowWidth - int(c.windowWidth / 5)) < currentMouseY < (
                        c.windowWidth - int(c.windowWidth / 5) + 50)):
                    print("Shutting down ...")
                    os._exit(0)  # clean exit
                    
    # Initialize menu flags and sensors
    def startMenu(self, numPlayers, numAI):
        animateMenuX = 0
        print(self.MENUSTAT)
        while self.MENUSTAT == True:
            mouse = pygame.mouse.get_pos()

            # Check mouse pos and highlight button when mouse hovers above
            currentMouseX = mouse[0]
            currentMouseY = mouse[1]

            self.screen.fill((0, 0, 0))
            self.clock.tick(30)

            menu = pygame.transform.scale(self.background1, (int(c.windowLength * 1.3), c.windowWidth))  # zoom in on bg

            formattedPlayButton, formattedHelpButton, formattedExitButton = self.formatButtons(menu, animateMenuX)

            self.placeButtons(currentMouseX, currentMouseY, formattedPlayButton, formattedHelpButton, formattedExitButton)

            self.eventGetter(currentMouseX, currentMouseY, numPlayers, numAI)

            pygame.display.update()  # update visuals
            self.fpsClock.tick(30)

            # Used for menu animation
            animateMenuX -= 0.5
            if animateMenuX <= -400:
                animateMenuX = 0
