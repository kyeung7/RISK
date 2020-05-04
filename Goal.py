# Team 9 RISK
# Sets bonus conditions for game
class Goal():
    def __init__(self, Map, turns):
        self.turns=  turns
        self.types = ["Capture continents", "Capture territories", "Destroy"]
        self.map = Map
        self.randrange = [[0, 1, 2, 3, 4, 5], [], [x for x in range(1, turns.numPlayers + 1)]]
