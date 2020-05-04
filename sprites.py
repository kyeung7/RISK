# Team 9 RISK

# Contains information on sprite layer and bounds
class Sprites():
    def __init__(self, surface, name_id):
        self.layout = surface
        self.name_pays = ""
        self.id = int(name_id[-6: -4])
        self.bounds = surface.get_bounding_rect()