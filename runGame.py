# Team 9 RISK

import glob
import uiInteractions
import random
import time
import pygame

from pygame import *
from interacting import Interacting
from RiskGUI import GUI

import constants as c

# Initializes game as usual howver incorporates basic AI as a player
class RunGame():
    def __init__(self, window, turn):
        self.pygameWindow = window

        # Updates current objects
        self.map = turn.map
        self.players = turn.players
        self.turn = turn

        self.numTroops = 25  # Sets number of troops
        self.selectedTerritory = None

        self.interfaceDice = []  # Contains dice results
        self.functions = []  # Contains function calls
        self.interfaceText = []  # Contains text layers for HUD
        self.surfaces = []  # Contains surface layers
        self.tempTerritoryList = []  # Contains territory layers
        self.textList = []  # Contains text overlays
        self.topLevel = []  # Used to hold help and win screen

    # Helpers for troop management
    @property
    def troopCount(self):
        if self.turn.phase == 0:
            return min(self.numTroops, self.players[
                self.turn.turnCount - 1].num_troops)  # Cannot deploy more then total - 1 troops from territory
        else:
            return self.numTroops

    @troopCount.setter
    def troopCount(self, troopVal):
        if self.turn.phase == 0:  # Checks troop placement during different phases
            if troopVal < 1:
                self.numTroops = 1
                print("Too few troops")
            elif troopVal > self.players[self.turn.turnCount - 1].num_troops:
                self.numTroops = self.players[self.turn.turnCount - 1].num_troops
                print("Too many troops")
        else:
            if troopVal < 0:
                self.numTroops = 0
                print("Too few troops")
            elif troopVal > self.selectedTerritory.num_troops - 1:
                self.numTroops = self.selectedTerritory.num_troops - 1  # Minimum of 1 troop per territory
                print("Too many troops")

        self.numTroops = troopVal

    # Sets a color layer on territory sprites based on player color
    def colorTerritories(self, sprites, gui):
        for p in self.players:
            for territories in p.territories:
                sprite = next((s for s in sprites if s.id == territories), None)
                gui.setSurfaceColor(sprite, p.color, 255)

    # Method initialzes map surface
    def run(self):
        self.surfaces = []
        background = pygame.image.load(c.imagePath + c.backgroundImage).convert()

        # Auto resize to fit background
        resize = c.windowLength / background.get_width()
        w = int(resize * background.get_width())
        h = int(resize * background.get_height())
        background = pygame.transform.scale(background, (w, h))

        # Auto resize to fit base map
        worldMap = pygame.image.load(c.imagePath + c.mapImages).convert_alpha()
        resize = c.windowLength / worldMap.get_width()
        w = int(resize * worldMap.get_width())
        h = int(resize * worldMap.get_height())
        worldMap = pygame.transform.scale(worldMap, (w, h))

        # Player HUD
        barre = pygame.image.load(c.imagePath + c.bareImage).convert_alpha()
        barre = pygame.transform.scale(barre, (c.windowLength, c.windowWidth - h))

        self.functions = []
        self.surfaces.extend([[background, (0, 0)], [barre, (0, h)], [worldMap, (0, 0)]])

    # ==================================================================================================================
    # Method utilizes overlay methods to update pygameWindow
    def display(self, function = None):

        # Loads png sprites for highlighting selected territories
        worldTerritories = glob.glob(c.mapPath + "*.png")
        territorySprites = []
        highlightedTerritories = []

        spriteSelected = -1

        # Adds an AI player to do moves, new constants serve as player data for the CPU
        selectFlag = False
        attackFlag = False
        helpFlag = False
        gameEnd = False
        startTerritory = None
        targetTerritory = None

        AI = self.players
        count = 0
        idxP = 0
        idxAi = 0
        AIPLAYER = []
        Players = []
        ID = []
        
        for i in AI:
            f = i.name
            if "AI" not in f:
                Players.append(f)
                print(str(Players[idxP]) + " is the " + str(count) + " index in list")
                idxP += 1
                ID.append(idxP)
            else:
                AIPLAYER.append(f)
                print(str(AIPLAYER[idxAi]) + " is the " + str(count) + " index in list")
                idxAi += 1
                ID.append(idxAi)
            count += 1

        # Initializes player UI
        gui = GUI()
        finalLayout = uiInteractions.formatTerr(self, worldTerritories, territorySprites, highlightedTerritories, gui)

        # Event handler for mouse and button interactions
        while (not gameEnd):
            pName = self.turn.players[self.turn.turnCount - 1].name
            gameEnd, helpFlag, selectFlag, spriteSelected = \
                uiInteractions.eventHandler(self, gameEnd, helpFlag, selectFlag, spriteSelected, pName)

            uiInteractions.sendSurface(self, finalLayout)

            uiInteractions.topLay(self, helpFlag, gui)


            # Highlight territories as cursor moves over them
            mouse = pygame.mouse.get_pos()
            try:
                tempColorValue = self.surfaces[2][0].get_at((mouse[0], mouse[1]))
            except IndexError as e:
                print(e)
                pass

            # Setups user GUI layout and enables player functions
            try:
                if tempColorValue != (0, 0, 0, 0) and tempColorValue != (0, 0, 0, 255):
                    temptroopValID = tempColorValue[0] - 100
                    spriteLayer = next((territorySprite for territorySprite in highlightedTerritories if
                                        territorySprite.id == temptroopValID), None)

                    click = uiInteractions.updateVisualGetClick(self, temptroopValID, spriteSelected, spriteLayer)

                    # Placing reinforcements on owned territories
                    if self.turn.list_phase[self.turn.phase] == "Placement":
                        if "AI" in pName:
                            avail = []
                            for p in self.map.territories: # Gets all territories
                                if p.id_player == self.turn.turnCount:
                                    avail.append(p)

                            # Randomly pick a country the AI owns...
                            randCountry = random.randrange(0,len(avail)-1)
                            troopsMax = self.turn.players[self.turn.turnCount - 1].num_troops
                            randTroops = random.randrange(1,troopsMax +1)
                            self.turn.placeTroops(avail[randCountry], randTroops)

                        uiInteractions.placing(self, click, temptroopValID)

                    # Attacking neighboring territories with n-1 troops
                    elif self.turn.list_phase[self.turn.phase] == "Attack":
                        if "AI" in pName:
                            totavail = []
                            availWTroops = []
                            for p in self.map.territories:  # Gets all territories
                                if p.id_player == self.turn.turnCount:
                                    totavail.append(p)

                            for i in range(len(totavail)):
                                if totavail[i].num_troops > 1:
                                    availWTroops.append(totavail[i])
                            maxT = 0
                            idxV = 0
                            idxN = []
                            for i in availWTroops:
                                numtroops = i.num_troops
                                idxN.append((numtroops, i))
                                if numtroops > maxT:
                                    maxT = numtroops
                                    idxV = i
                            if len(availWTroops) < 1:
                                for i in totavail:
                                    numtroops = i.num_troops
                                    idxN.append((numtroops, i))
                                    if numtroops > maxT:
                                        maxT = numtroops
                                        idxV = i


                            # Now that we have max troops we want to attack a neighbor, since this AI is dumb just randomly pick one
                            totTargets = []
                            for p in self.map.territories:
                                if p.id_player != self.turn.turnCount:
                                    totTargets.append(p)

                            attackable = []
                            for i in totTargets:
                                if i.id in idxV.neighbors:
                                    attackable.append(i)

                            # Randomly chooses a valid target and attacks with all troops
                            randTarget = random.randrange(0, len(attackable))
                            tgts = []
                            if maxT == idxV.num_troops:
                                for i in idxV.neighbors:
                                    tgts.append(i)
                                if idxV.id_player == self.turn.turnCount and idxV.id in attackable[randTarget].neighbors:
                                    try:
                                        self.interfaceDice = []
                                        attackResult, diceResults = self.turn.attack(idxV, totTargets[randTarget],
                                                                                     idxV.num_troops-1)
                                        for i, res in enumerate(diceResults):
                                            gui.diceRolls(self, res[0], res[2], 600, territorySprites[
                                                0].layout.get_height() + 10 + i * c.diceSize * 1.1)
                                            gui.diceRolls(self, res[1], res[3], 800, territorySprites[
                                                0].layout.get_height() + 10 + i * c.diceSize * 1.1)
                                        pygame.time.wait(100)
                                    except ValueError as e:
                                        print(e.args)
                                        attackResult = False
                                        self.tempTerritoryList = []

                                    if attackResult:  # On successful attack, update visuals
                                        sprite = next((s for s in territorySprites if s.id == temptroopValID), None)
                                        gui.setSurfaceColor(sprite, self.turn.players[self.turn.turnCount - 1].color,
                                                            255)
                                        finalLayout.blit(sprite.layout, (0, 0))
                                        targetTerritory = totTargets[randTarget]
                                        self.numTroops = idxV.num_troops - 1

                                    else:
                                        self.tempTerritoryList = []
                            elif idxV.num_troops > 1:
                                print("Using army with less troops")
                            else:
                                print("No available attacks")

                        # Updates flags after event check
                        attackFlag, selectFlag, startTerritory, targetTerritory = uiInteractions.attacking(self, click, selectFlag, temptroopValID, spriteLayer, attackFlag, gui, territorySprites, finalLayout, startTerritory, targetTerritory)



                    # Moving troops between territories
                    elif self.turn.list_phase[self.turn.phase] == "Movement":
                        if click[0] == 1 and not selectFlag:  # On left click select territory
                            startTerritory = next((p for p in self.map.territories if p.id == temptroopValID), None)
                            self.selectedTerritory = startTerritory
                            if startTerritory.id_player == self.turn.turnCount and startTerritory.num_troops > 1:
                                self.troopCount = startTerritory.num_troops - 1
                                self.tempTerritoryList.append(spriteLayer.layout)
                                selectFlag = True
                                spriteSelected = temptroopValID

                        elif click[0] == 1:  # On right click unselect territory
                            endTerritory = next((p for p in self.map.territories if p.id == temptroopValID), None)
                            path = self.map.checkValidPath(self.turn.players[self.turn.turnCount - 1].territories,
                                                           startTerritory, endTerritory)
                            selectFlag = False
                            spriteSelected = 0
                            self.tempTerritoryList = []

                            if path and endTerritory.id != startTerritory.id:
                                self.turn.troopMovement(startTerritory, endTerritory, self.troopCount)
                                self.turn.next()


                    # Update troop text overlay visuals
                    self.textList = []
                    gui.troopDisplay(self.textList, territorySprites, self.map)

            except ValueError as e:
                pass

            # Update HUD text visuals
            self.interfaceText = []
            gui.display_hud(self.troopCount, self.interfaceText, self.turn,
                        (75, territorySprites[0].layout.get_height() + 10))
            pygame.display.flip()
# ==================================================================================================================
# Returns information for text handling
