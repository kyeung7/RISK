# Team 9 RISK

import random
from Card import Card
from player import Player
from Goal import Goal
from Objective import Objective

# Contains methods for setting turns. Turn depends on current players
class PlayerTurn():
    def __init__(self, numPlayers, mapInstance):
        self.endGame = False
        self.num = 0
        self.numPlayers = numPlayers
        self.turnList = list(range(1, numPlayers + 1))
        random.shuffle(self.turnList)
        self.numTerritories = mapInstance.numTerritories
        self.players = []

        for k in range(0, numPlayers):
            self.players.append(Player(k + 1, mapInstance, self))

        # Assigns player goals
        self.goal = Goal(mapInstance, self)
        for k in range(0, numPlayers):
            self.players[k].obj = Objective(self.goal, self.players[k])
        self.id_turnList = 0
        self.map = mapInstance
        self.list_phase = ["Placement", "Attack", "Movement"]
        self.phase = 0
        self._player_ = self.turnList[self.id_turnList]

    # Helpers for allocating starting troupes
    def playerName(self):
        return self.players[self.turnCount -1].name

    # Turn actions on attac
    def next(self):
        if self.players[self.turnCount - 1].num_troops > 0:
            raise ValueError("Need to deploy", self.players[self.turnCount - 1].num_troops)

        if self.num == 0:  # Placement phase
            self.id_turnList = (self.id_turnList + 1) % len(self.turnList)
            if self.id_turnList == 0:
                self.num += 1
                self.phase = (self.phase + 1) % len(self.list_phase)

        elif self.num == 1:  # Attack phase
            self.phase = (self.phase + 1) % len(self.list_phase)
            if self.phase == 0:
                self.phase += 1
                self.id_turnList = (self.id_turnList + 1) % len(self.turnList)

                # Update territory info if captured
                self.players[self.turnCount - 1].attack_success = False
                if self.id_turnList == 0:
                    self.num += 1
                    self.phase = 0

                    # Updates reinforcement troops for start of player turn
                    self.players[self.turnCount - 1].num_troops += self.players[self.turnCount - 1].troopsPerTurn
        else:
            self.phase = (self.phase + 1) % len(self.list_phase)
            if self.phase == 0:
                self.id_turnList = (self.id_turnList + 1) % len(self.turnList)

                # Update territory captured boolean
                self.players[self.turnCount - 1].attack_success = False

                # Updates reinforcement troops for start of player turn
                self.players[self.turnCount - 1].num_troops += self.players[self.turnCount - 1].troopsPerTurn
                if self.id_turnList == 0:
                    self.num += 1

        print("Turn Number :", self.num, "order", self.turnList, "player turn", self.turnList[self.id_turnList])
        print(self.list_phase[self.phase])

    # Next player turn actions
    def next_player(self):
        if self.num == 0:  # Initial placement phase
            self.id_turnList = (self.id_turnList + 1) % len(self.turnList)
            if self.id_turnList == 0:
                self.num += 1
                self.phase = (self.phase + 1) % len(self.list_phase)

        elif self.num == 1:  # Skip placement
            self.phase = 1
            self.id_turnList = (self.id_turnList + 1) % len(self.turnList)
            self.players[self.turnCount - 1].attack_success = False
            if self.id_turnList == 0:
                self.num += 1
                self.phase = 0
                self.players[self.turnCount - 1].num_troops += self.players[self.turnCount - 1].troopsPerTurn

        else:
            # Move to next player turn
            self.id_turnList = (self.id_turnList + 1) % len(self.turnList)
            self.phase = 0
            self.players[self.turnCount - 1].attack_success = False
            self.players[self.turnCount - 1].num_troops += self.players[self.turnCount - 1].troopsPerTurn
            if self.id_turnList == 0:
                self.num += 1

    # Method allocates starting troops for each player
    def initialTroops(self):
        if self.numPlayers == 2:
            num_troops = 50
        elif self.numPlayers == 3:
            num_troops = 40
        elif self.numPlayers == 4:
            num_troops = 30
        elif self.numPlayers == 5:
            num_troops = 20
        elif self.numPlayers == 6:
            num_troops = 15
        else:
            print("Troop allocation error! Please restart game!")
            num_troops = 0
        for p in self.players:
            p.num_troops = num_troops

    # Distributes territories as evenly as possible among players
    def distributeTerritories(self, territories):
        listTerritoryID = []
        for k in territories:
            listTerritoryID.append(k.id)
            
        random.shuffle(listTerritoryID)
        n = self.numTerritories // self.numPlayers
        for idx, i in enumerate(range(0, len(listTerritoryID), n)):
            if idx < self.numPlayers:
                self.players[idx].territories = listTerritoryID[i:i + n]
            else:
                for pays_restant in listTerritoryID[i:i + n]:  # After distribution, remaing countrys randomly assigned
                    self.players[random.randint(0, self.numPlayers - 1)].territories.append(pays_restant)

        for p in self.players:
            for territories in p.territories:
                self.map.territories[territories - 1].id_player = p.id
                self.map.territories[territories - 1].num_troops = 1  # Min 1 troop per territory
                p.num_troops -= 1
                
        return listTerritoryID

    # Get dice roll results
    def rollDice(self, attack, defense):
        d_a = []
        d_b = []
        losses = [0, 0, d_a, d_b]  # Attacker deaths, defender deaths

        for k in range(0, attack):
            d_a.append(random.randint(1, 6))
        d_a.sort(reverse=True)

        for k in range(0, defense):
            d_b.append(random.randint(1, 6))
        d_b.sort(reverse=True)

        for k in range(0, min(attack, defense)):
            if d_b[k] < d_a[k]:  # On attacker win
                losses[1] = losses[1] + 1
            else:
                losses[0] = losses[0] + 1
        return losses

    # Used with dice to calculate successful attacks
    def attack(self, attacker, defender, attackingTroops):
        diceResults = []

        while (True):
            if attackingTroops > 2:
                dice_atck = 3
            elif attackingTroops > 1:
                dice_atck = 2
            elif attackingTroops > 0:
                dice_atck = 1
            else:
                raise ValueError("not enough troops:", attackingTroops)
            if defender.num_troops > 1:
                dice_def = 2
            elif defender.num_troops > 0:
                dice_def = 1

            res = self.rollDice(dice_atck, dice_def)
            print(res)

            diceResults.append(res)
            attacker.num_troops -= res[0]
            attackingTroops -= res[0]
            defender.num_troops -= res[1]

            if attackingTroops == 0:  # Attack failed
                return False, diceResults

            elif defender.num_troops == 0:  # Territory captured

                # Update list of territories for players
                self.players[attacker.id_player - 1].territories.append(defender.id)
                self.players[defender.id_player - 1].territories.remove(defender.id)

                # Update captured territor id
                defender.id_player = attacker.id_player

                # Moves surviving troops to new territory, remove from old
                self.troopMovement(attacker, defender, dice_atck)

                # Attacker gets a card if it is the first captured territory this turn
                if self.players[attacker.id_player - 1].attack_success == False:
                    self.players[attacker.id_player - 1].attack_success = True

                    # If player has 5+ cards, card is discarded
                    if len(self.players[attacker.id_player - 1].cards) > 4:
                        self.players[attacker.id_player - 1].del_card(0)

                    self.players[attacker.id_player - 1].cards.append(Card())
                return True, diceResults

    # Remove troops from old territory, add survivors to new
    def troopMovement(self, origin, destination, num_troops):
        if num_troops < origin.num_troops:
            origin.num_troops -= num_troops
            destination.num_troops += num_troops
        else:
            print("trying to move too many troops")

    # Troop assigner during placement
    def placeTroops(self, territories, num_troops):
        player = next((p for p in self.players if p.id == territories.id_player), None)
        if (player.num_troops - num_troops <= 0):
            territories.num_troops += player.num_troops
            player.num_troops -= player.num_troops
            self.next()
        else:
            player.num_troops -= num_troops
            territories.num_troops += num_troops

    # getter for turn
    @property
    def turnCount(self):
        return self.turnList[self.id_turnList]

    # Checks if path is valid
    def chemin_exist(self, playerTerritories, territoryA, territoryB):
        validNeighbors = []
        if territoryA.id in playerTerritories:
            validNeighbors.append(territoryA.id)
            self.pathDepth(territoryA, playerTerritories, validNeighbors)
            if territoryB.id in validNeighbors:
                print("A path exists")
                return True
            else:
                print("no valid path")
                return False
        else:
            print("Player cannot select this territory")
            return False

    def pathDepth(self, territories, playerTerritories, validNeighbors):
        for p_id in territories.neighbors:
            if p_id in playerTerritories and p_id not in validNeighbors:
                validNeighbors.append(p_id)
                self.pathDepth(territories[p_id - 1], playerTerritories, validNeighbors)
