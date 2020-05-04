# Team 9 RISK

# Holds data for each territory on map
class Territories():
    def __init__(self, name, continent, Map):
        Map.numTerritories = Map.numTerritories + 1
        self.id = Map.numTerritories
        self.name = name
        self.continent = continent
        self.id_player = 0
        self.num_troops = 0
        self.neighbors = []

    # Used for valid path checking
    def neighbors(self, territories):
        for t in territories:
            self.neighbors.append(t)
