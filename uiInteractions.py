# Team 9 RISK

import pygame
from pygame import *
import constants as c
from sprites import Sprites

# Format territory sprites and add to surface
def formatTerr(self, worldTerritories, territorySprites, highlightedTerritories, gui):
    for i, j in enumerate(worldTerritories):
        surface = pygame.image.load(j).convert()
        resize = c.windowLength / surface.get_width()

        surface = pygame.transform.scale(surface, (
            int(resize * surface.get_width()), int(resize * surface.get_height())))

        territorySprite = Sprites(surface, j)
        initialSpriteLayer = Sprites(surface.copy(), j)

        gui.setSurfaceColor(initialSpriteLayer, (1, 1, 1), 150)
        territorySprites.append(territorySprite)
        highlightedTerritories.append(initialSpriteLayer)

    # Creates final layer of all connected sprites
    self.colorTerritories(territorySprites, gui)
    for i, j in enumerate(territorySprites):
        if i == 0:
            finalLayout = j.layout.copy()
        else:
            finalLayout.blit(j.layout, (0, 0))

    # Update visual troop numbers
    gui.troopDisplay(self.textList, territorySprites, self.map)
    return finalLayout

# Checks user mouse and key interactions
def eventHandler(self, gameEnd, helpFlag, selectFlag, spriteSelected, ID):
    if "AI" in ID:
        pass

    # Checks every mouse and key action in window
    for event in pygame.event.get():
        if event.type == QUIT:
            print("Ending game!")
            gameEnd = True

        # Handling key presses
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:  # Exit program on key press
                print("Ending game!")
                gameEnd = True

            elif event.key == K_n:  # Proceed to next round
                try:
                    self.turn.next()
                except ValueError as e:
                    print(e.args)

                self.tempTerritoryList = []  # Resets selected territory for next player
                selectFlag = False
                spriteSelected = 0

            elif event.key == K_h:  # Help screen
                helpFlag = not helpFlag

        # Handling mouse-clicks/scrolls
        elif event.type == MOUSEBUTTONDOWN:
            try:
                if event.button == 3:  # Right mouse-click to unselect (selected) territory
                    self.tempTerritoryList = []
                    selectFlag = False
                    spriteSelected = 0

                elif event.button == 4:  # Scroll mousewheel down to increase selected troops
                    self.troopCount += 1

                elif event.button == 5:  # Scroll mousewheel down to decrease selected troops
                    if self.troopCount > 0:
                        self.troopCount -= 1

            except AttributeError as e:
                print(e)
                print("You should select a country first ...")
            except ValueError as e:
                print(e.args)
    return gameEnd, helpFlag, selectFlag, spriteSelected

# Sends layers to surface of pygame
def sendSurface(self, finalLayout):
    for surface in self.surfaces:
        self.pygameWindow.blit(surface[0], surface[1])

    for dice in self.interfaceDice:
        self.pygameWindow.blit(dice[0], dice[1])

    self.pygameWindow.blit(finalLayout, (0, 0))

    for tempTerritoryList in self.tempTerritoryList:
        self.pygameWindow.blit(tempTerritoryList, (0, 0))

    for text in self.textList:
        self.pygameWindow.blit(text[0], text[1])

    for t in self.interfaceText:
        self.pygameWindow.blit(t[0], t[1])

    for final in self.topLevel:
        self.pygameWindow.blit(final[0], final[1])

    if self.functions != []:
        for f in self.functions:
            f()

# Method for handling the upper most surface layer
def topLay(self, helpFlag, gui):
    if self.turn.players[self.turn.turnCount - 1].obj.getGoalStatus() == True:
        self.topLevel = []

        topLayer = pygame.Surface(self.pygameWindow.get_size())
        topLayer = topLayer.convert()
        topLayer.fill(c.black)
        topLayer.set_alpha(180)

        self.topLevel.append([topLayer, (0, 0)])
        gui.display_win(self.topLevel, self.players)

    # Uses same top layer to contain help screen
    else:
        if helpFlag:
            self.topLevel = []

            topLayer = pygame.Surface(self.pygameWindow.get_size())
            topLayer = topLayer.convert()
            topLayer.fill(c.black)
            topLayer.set_alpha(180)

            self.topLevel.append([topLayer, (0, 0)])
            gui.display_help(self.topLevel)
        else:
            self.topLevel = []

# Provides interactive visual changes upon click/presses
def updateVisualGetClick(self, temptroopValID, selectedTerritory, spriteLayer):

    if temptroopValID != selectedTerritory:
        self.pygameWindow.blit(spriteLayer.layout, (0, 0))
        pygame.display.update(spriteLayer.layout.get_rect())

    # On click, check phase and territory function validity
    click = pygame.mouse.get_pressed()
    return click

# Helper for planning phase
def placing(self, click, temptroopValID):
    if click[0] == 1:
        playerTerritory = next((p for p in self.map.territories if p.id == temptroopValID),
                               None)
        if playerTerritory.id_player == self.turn.turnCount:
            self.turn.placeTroops(playerTerritory, self.troopCount)
            pygame.time.wait(100)
        else:
            print("This territory does not belong to the player!")

# Helper for troop movement phase
def moving(self, click, selectFlag, temptroopValID, spriteLayer, startTerritory):
    spriteSelect = 0
    
    if click[0] == 1 and not selectFlag:  # On left click select territory
        startTerritory = next((p for p in self.map.territories if p.id == temptroopValID), None)
        self.selectedTerritory = startTerritory
        
        # One troop must always occupy controlled territories
        if startTerritory.id_player == self.turn.turnCount and startTerritory.num_troops > 1:
            self.troopCount = startTerritory.num_troops - 1
            self.tempTerritoryList.append(spriteLayer.layout)
            selectFlag = True
            spriteSelect = temptroopValID

    elif click[0] == 1:  # On right click unselect territory
        endTerritory = next((p for p in self.map.territories if p.id == temptroopValID), None)
        path = self.map.checkValidPath(self.turn.players[self.turn.turnCount - 1].territories,
                                       startTerritory, endTerritory)
        selectFlag = False
        spriteSelect = 0
        self.tempTerritoryList = []

        if path and endTerritory.id != startTerritory.id:
            self.turn.troopMovement(startTerritory, endTerritory, self.troopCount)
            self.turn.next()

    return selectFlag, spriteSelect

# Helper for attack phase
def attacking(self, click, selectFlag, temptroopValID, spriteLayer, attackFlag, gui, territorySprites, finalLayout,
              startTerritory, targetTerritory):
    if click[0] == 1 and not selectFlag:
        startTerritory = next((p for p in self.map.territories if p.id == temptroopValID), None)
        self.selectedTerritory = startTerritory

        # Always one troop minimun on territories owned
        if startTerritory.id_player == self.turn.turnCount and startTerritory.num_troops > 1:
            self.troopCount = startTerritory.num_troops - 1
            self.tempTerritoryList.append(spriteLayer.layout)
            selectFlag = True
            spriteSelected = temptroopValID

    elif click[0] == 1:  # Selecting territory to attack
        endTerritory = next((p for p in self.map.territories if p.id == temptroopValID), None)
        if attackFlag and endTerritory == targetTerritory and startTerritory.num_troops > 1:
            self.turn.troopMovement(startTerritory, endTerritory, self.troopCount)
            selectFlag = False
            self.tempTerritoryList = []
            attackFlag = False

        elif attackFlag:
            selectFlag = False
            self.tempTerritoryList = []
            attackFlag = False
            
        # Attack neighboring target with home troops
        elif endTerritory.id_player != self.turn.turnCount and endTerritory.id in startTerritory.neighbors:  # Attack with home troops

            # Get dice roll results and pause
            try:
                self.interfaceDice = []
                attackResult, diceResults = self.turn.attack(startTerritory, endTerritory,
                                                             self.troopCount)
                for i, res in enumerate(diceResults):
                    gui.diceRolls(self, res[0], res[2], 600, territorySprites[
                        0].layout.get_height() + 10 + i * c.diceSize * 1.1)
                    gui.diceRolls(self, res[1], res[3], 800, territorySprites[
                        0].layout.get_height() + 10 + i * c.diceSize * 1.1)
                pygame.time.wait(100)
                
            except ValueError as e:
                print(e.args)
                attackResult = False
                selectFlag = False
                self.tempTerritoryList = []
                
            # On successful attack, update visuals and ownership
            if attackResult:
                sprite = next((s for s in territorySprites if s.id == temptroopValID), None)
                gui.setSurfaceColor(sprite, self.turn.players[self.turn.turnCount - 1].color, 255)
                finalLayout.blit(sprite.layout, (0, 0))
                attackFlag = True
                targetTerritory = endTerritory
                self.troopCount = startTerritory.num_troops - 1
            else:
                selectFlag = False
                self.tempTerritoryList = []
                
    return attackFlag, selectFlag, startTerritory, targetTerritory



