# Team 9 RISK
import pygame
import constants as c

# Contains methods for UI display
class GUI():
    
    # Defines text box for UI
    def textArea(self, text, font, color=(0, 0, 0)):
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()

    # Sets sprite overlay colors
    def setSurfaceColor(self, sprite, color, alpha):
        for x in range(0, sprite.bounds.width):
            for y in range(0, sprite.bounds.height):
                if sprite.layout.get_at((sprite.bounds.x + x, sprite.bounds.y + y)) != (0, 0, 0):
                    sprite.layout.set_at((sprite.bounds.x + x, sprite.bounds.y + y), color)
                    sprite.layout.set_alpha(alpha)

    # Update troop visual count
    def troopDisplay(self, textList, sprites, Map):
        smallText = pygame.font.Font(None, 25)
        for sprite in sprites:
            territories = Map.territories[sprite.id - 1]
            textSurface, textBox = self.textArea(str(territories.num_troops), smallText)
            textBox.center = sprite.bounds.center
            textList.append([textSurface, textBox])

    # Player victory screen if a player completes goals
    def display_win(self, topLevel, players):
        largeText = pygame.font.Font(None, 75)
        margin = 50
        textPosition = (200, 200)
        for p in players:
            if p.obj.getGoalStatus() == True:
                winnerPlayer = p
                textSurface, textBox = self.textArea(winnerPlayer.name + " wins!", largeText, winnerPlayer.color)
                textBox.topleft = textPosition
                textPosition = (textPosition[0], textPosition[1] + margin)
                topLevel.append([textSurface, textBox])

    # Adds text to top layer for help screen
    def display_help(self, topLevel):
        largeText = pygame.font.Font(None, 50)
        margin = 50
        textPosition = (200, 200)

        textSurface, textBox = self.textArea("'h' key: Help", largeText, c.white)
        textBox.topleft = textPosition
        topLevel.append([textSurface, textBox])
        textPosition = (textPosition[0], textPosition[1] + margin)

        textSurface, textBox = self.textArea("Left/Right Mouse-click : Select/Deselect Territory", largeText, c.white)
        textBox.topleft = textPosition
        topLevel.append([textSurface, textBox])
        textPosition = (textPosition[0], textPosition[1] + margin)

        textSurface, textBox = self.textArea("Scroll Wheel Up/Down : Increase/Decrease Troop Selection", largeText, c.white)
        textBox.topleft = textPosition
        topLevel.append([textSurface, textBox])
        textPosition = (textPosition[0], textPosition[1] + margin)

        textSurface, textBox = self.textArea("'n' key: Next phase", largeText, c.white)
        textBox.topleft = textPosition
        topLevel.append([textSurface, textBox])
        textPosition = (textPosition[0], textPosition[1] + margin)

        textSurface, textBox = self.textArea("'esc' key: quit", largeText, c.white)
        textBox.topleft = textPosition
        topLevel.append([textSurface, textBox])
        textPosition = (textPosition[0], textPosition[1] + margin)

    # Updates dice visuals and shows respective losses as a column
    def display_hud(self, troopCount, interfaceText, turn, textPosition):
        smallText = pygame.font.Font(None, 25)
        margin = 20
        col = [100, 400, 700, 1000]
        row = textPosition[1]

        # FIRTS COLUMN TEXT        ... position carries over to next
        textSurface, textBox = self.textArea("Round : " + str(turn.num), smallText)
        textBox.topleft = (textPosition[0], textPosition[1])
        interfaceText.append([textSurface, textBox])

        textSurface, textBox = self.textArea("Phase : " + turn.list_phase[turn.phase], smallText)
        textPosition = (textPosition[0], textPosition[1] + margin + margin)
        textBox.topleft = textPosition
        interfaceText.append([textSurface, textBox])

        textSurface, textBox = self.textArea("Player : ", smallText)
        textPosition = (textPosition[0], textPosition[1] + margin + margin)
        textBox.topleft = textPosition
        interfaceText.append([textSurface, textBox])

        # name value
        textSurface, textBox = self.textArea(turn.players[turn.turnCount - 1].name, smallText,
                                        turn.players[turn.turnCount - 1].color)
        textBox.topleft = (textPosition[0] + 70, textPosition[1])
        interfaceText.append([textSurface, textBox])

        # MIDDLE COLUMN TEXT
        textSurface, textBox = self.textArea("Number of Selected Troops : " + str(troopCount), smallText)
        textPosition = (textPosition[0] + 200, textPosition[1])
        textBox.topleft = textPosition
        interfaceText.append([textSurface, textBox])

        textSurface, textBox = self.textArea(
            "Available number of troops to deploy : " + str(turn.players[turn.turnCount - 1].num_troops), smallText)
        textPosition = (textPosition[0], textPosition[1] - margin - margin)
        textBox.topleft = textPosition
        interfaceText.append([textSurface, textBox])

        textSurface, textBox = self.textArea("Troops per turn : " + str(turn.players[turn.turnCount - 1].troopsPerTurn), smallText)
        textPosition = (textPosition[0], textPosition[1] - margin - margin)
        textBox.topleft = textPosition
        interfaceText.append([textSurface, textBox])

    # Updates dice visuals and shows respective losses as a column
    def diceRolls(self, gameInstance, troopLosses, numDies, xPos, yPos):
        tempDiceLayer = []

        # Gets correct die sprite and resizes
        for i, j in enumerate(numDies):
            dieSprite = pygame.image.load(c.dicePath + str(j) + ".png").convert_alpha()
            resizeSprite = pygame.transform.scale(dieSprite, (c.diceSize, c.diceSize))
            tempDiceLayer.append(
                [resizeSprite, gameInstance.pygameWindow.blit(resizeSprite, (i * c.diceSize * 1.1 + xPos, yPos))])

        # Gets tombstome sprite to represent losses in a row
        for deaths in range(0, troopLosses):
            tombstoneSprite = pygame.image.load(c.imagePath + c.deadImage).convert_alpha()
            resizeSprite = pygame.transform.scale(tombstoneSprite, (c.diceSize, c.diceSize))
            tempDiceLayer.append([resizeSprite, gameInstance.pygameWindow.blit(resizeSprite, (
                xPos - (deaths + 1) * c.diceSize * 1.1, yPos))])

        gameInstance.interfaceDice.extend(tempDiceLayer)
