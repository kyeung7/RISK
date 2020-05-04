# Team 9 RISK
import copy
import random

# Contains troop bonus information
class Card():
    def __init__(self):
        self.types = ["Solider", "Calvalry", "Cannon"]
        bonus = [5, 8, 10, 12]
        
        rand = random.randint(0, 2)
        
        self.type = self.types[rand]
        self.bonus = bonus[rand]
