# Team 9 RISK
from MainMenu import Menu
import constants as c
import pygame


# Since we were behind we used a wikipedia page with all the map images,
# and https://github.com/Whysmerhill/Risk/tree/a23b17826e84d992bf5434b99724d7aafaae5443 as a reference point.
# Most of the code is handwritten with logic for the playerTurn borrowed from this github.

# To run the game you must manually input the number of players or AI
# We will create a cleaner way for users to edit this if time allows

# We will start with the main menu to start the proj.
def run():
    freshStart = True
    running = True
    MENUSTAT = True
    game = False
    
    screen = pygame.display.set_mode((c.windowLength, c.windowWidth))
    clock = pygame.time.Clock()
    
    pygame.display.set_caption("Risk (GAME WINDOW)")
    background1 = pygame.image.load(c.imagePath + c.menuBackgroundImage)

    # Change number of players here
    numPlayers = 0
    numAI = 2
    
    if numPlayers + numAI >= 2:
        print("OK running")
        newMenu = Menu(MENUSTAT, screen, clock, background1)
        Menu.startMenu(newMenu,numPlayers, numAI)
    else:
        print("Rerun not enough players")

if __name__ == "__main__":
    run()
