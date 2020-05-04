# Team 9 RISK

from continent import Continent

# Contains territory initialization and neighboring paths
class Map():

    def __init__(self):
        self.territories = []
        self.continents = []
        self.numTerritories = 0

        # Lets create a list for all the continents
        # information from https://en.wikipedia.org/wiki/Risk_(game)
        self.continents.append(
            Continent(["Congo", "East Africa", "Egypt", "Madagascar", "North Africa", "South Africa"], 3, "Africa",
                      self))

        self.continents.append(Continent(
            ["Alaska", "Alberta", "Central America", "Eastern United States", "Greenland", "Northwest Territory",
             "Ontario", "Quebec", "Western United States"], 5, "North America", self))

        self.continents.append(Continent(["Venezuela", "Brazil", "Peru", "Argentina"], 2, "South America", self))

        self.continents.append(Continent(
            ["Afghanistan", "China", "India", "Irkutsk", "Japan", "Kamchatka", "Middle East", "Mongolia",
             "Siam", "Siberia", "Ural", "Yakutsk"], 7, "Asia", self))

        self.continents.append(Continent(
            ["Great Britain", "Iceland", "Northern Europe", "Scandinavia", "Southern Europe", "Ukraine",
             "Western Europe"], 5, "Europe", self))

        self.continents.append(
            Continent(["Eastern Australia", "Indonesia", "Papa New Guinea", "Western Australia"], 2, "Australia",
                      self))

        # we need to hard code all the neighbors so looking at the map and wiki page the following is created.
        # Territory numbers
        # 1: Congo                          16: Argentina       31: Yakutsk
        # 2: East Africa                    17: Brazil          32: Great Britain
        # 3: Egypt                          18: Peru            33: Iceland
        # 4: Madagascar                     19: Venezuela       34: Northern Europe
        # 5: North Africa                   20: Afghanistan     35: Scandinavia
        # 6: South Africa                   21: China           36: Southern Europe
        # 7: Alaska                         22: India           37: Ukraine (Eastern Europe, Russia)
        # 8: Alberta                        23: Irkutsk         38: Western Europe
        # 9: Central America                24: Japan           39: Eastern Australia
        # 10: Eastern United States         25: Kamchatka       40: Indonesia
        # 11: Greenland                     26: Middle East     41: New Guinea
        # 12: Northwest Territory           27: Mongolia        42: Western Australia
        # 13: Ontario (Central Canada)      28: Siam
        # 14: Quebec (Eastern Canada)       29: Siberia
        # 15: Western United States         30: Ural

        # Africa
        self.continents[0].territories[0].neighbors = [2, 5, 6] # Congo
        self.continents[0].territories[1].neighbors = [1, 3, 4, 5, 26] #East Africa
        self.continents[0].territories[2].neighbors = [2, 5, 36, 26] # Egypt
        self.continents[0].territories[3].neighbors = [2, 6] # Madagascar
        self.continents[0].territories[4].neighbors = [1, 2, 3, 17, 36, 38] # North Africa
        self.continents[0].territories[5].neighbors = [1, 2, 4] # South Africa

        # North america
        self.continents[1].territories[0].neighbors = [8, 12, 25] # Alaska
        self.continents[1].territories[1].neighbors = [7, 12, 13, 15] # Alberta
        self.continents[1].territories[2].neighbors = [15, 10, 19]  # Central America
        self.continents[1].territories[3].neighbors = [9, 15, 13, 14]  # Eastern United States
        self.continents[1].territories[4].neighbors = [12, 13, 14, 33] # Greenland
        self.continents[1].territories[5].neighbors = [7, 8, 13, 11] # Northwest Territory
        self.continents[1].territories[6].neighbors = [8, 15, 10, 14, 11, 12] # Ontario
        self.continents[1].territories[7].neighbors = [10, 13, 11] # Quebec
        self.continents[1].territories[8].neighbors = [9, 10, 8, 13] # Western United States

        # South America
        self.continents[2].territories[0].neighbors = [17, 18] # Venezuela
        self.continents[2].territories[1].neighbors = [16, 18, 19, 5] # Brazil
        self.continents[2].territories[2].neighbors = [16, 17, 19] # Peru
        self.continents[2].territories[3].neighbors = [18, 17, 9]  # Argentine

        # Asia
        self.continents[3].territories[0].neighbors = [21, 22, 26, 30, 37]  # Afghanistan
        self.continents[3].territories[1].neighbors = [20, 22, 28, 27, 29, 30] # China
        self.continents[3].territories[2].neighbors = [20, 21, 26, 28] # India
        self.continents[3].territories[3].neighbors = [29, 27, 25, 31] # Irkutsk
        self.continents[3].territories[4].neighbors = [27, 25] # Japan
        self.continents[3].territories[5].neighbors = [31, 23, 27, 24, 7] # Kamchatka
        self.continents[3].territories[6].neighbors = [20, 22, 37, 2, 3] # Middle East
        self.continents[3].territories[7].neighbors = [24, 21, 29, 25, 23] # Mongolia
        self.continents[3].territories[8].neighbors = [21, 22, 40] # Siam
        self.continents[3].territories[9].neighbors = [30, 21, 23, 31, 27] # Siberia
        self.continents[3].territories[10].neighbors = [20, 21, 29, 37]  # Ural
        self.continents[3].territories[11].neighbors = [29, 23, 25] # Yakitsk

        # Europe
        self.continents[4].territories[0].neighbors = [33, 35, 34, 38] # Great Britain
        self.continents[4].territories[1].neighbors = [32, 35, 11] # Iceland
        self.continents[4].territories[2].neighbors = [32, 35, 37, 36, 38] # Northern Europe
        self.continents[4].territories[3].neighbors = [37, 32, 33, 34] # Scandinavia
        self.continents[4].territories[4].neighbors = [38, 34, 37, 3, 26, 5] # Southern Europe
        self.continents[4].territories[5].neighbors = [35, 34, 36, 20, 26, 30] # Ukraine
        self.continents[4].territories[6].neighbors = [32, 34, 36, 5] # Western Europe

        # Australia
        self.continents[5].territories[0].neighbors = [42, 41] # Eastern Australia
        self.continents[5].territories[1].neighbors = [42, 41, 28] # Indonesia
        self.continents[5].territories[2].neighbors = [42, 40, 39] # New Guinea
        self.continents[5].territories[3].neighbors = [39, 41, 40] # Western Australia

    # Determines if territories are neighbors
    def checkValidPath(self, playerTerritories, startTerritory, endTerritory):
        validTerritories = []
        if startTerritory.id in playerTerritories:
            validTerritories.append(startTerritory.id)
            self.pathCalculation(startTerritory, playerTerritories, validTerritories)
            if endTerritory.id in validTerritories:
                print("A path exists")
                return True
            else:
                print("There does not exist a path")
                return False
        else:
            print("Player cannot choose this country")
            return False

    # Helper for check path
    def pathCalculation(self, territories, playerTerritories, validTerritories):
        for pathIndexer in territories.neighbors:
            if pathIndexer in playerTerritories and pathIndexer not in validTerritories:
                validTerritories.append(pathIndexer)
                self.pathCalculation(self.territories[pathIndexer - 1], playerTerritories, validTerritories)
