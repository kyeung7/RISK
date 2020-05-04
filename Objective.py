# Team 9 RISK
import random
import copy

# Contains goal condition checks, players complete objectives to win
class Objective():
    def __init__(self,goal,player):
        self.goal = goal
        self.type = self.goal.types[random.randint(0,len(self.goal.types)-1)]
        self.player = player
        self._description = ""
        self.gen_obj()
        
    # Used for goal setup
    def gen_obj(self):
        if self.type == "Captured continent":
            self.continents = []
            self.other_cont = False
            self.nbtroupes = 1
            r_choice = random.choice(self.goal.randrange[0])
            self.goal.randrange[0].remove(r_choice) #Prevent mission dupe
            
            if r_choice == 0:
                self.continents.append(self.goal.map.continents[4])
                self.continents.append(self.goal.map.continents[5])
                self.other_cont = True
                
            elif r_choice == 1:
                self.continents.append(self.goal.map.continents[4])
                self.continents.append(self.goal.map.continents[2])
                self.other_cont = True
                
            elif r_choice == 2:
                self.continents.append(self.goal.map.continents[1])
                self.continents.append(self.goal.map.continents[0])
                
            elif r_choice == 3:
                self.continents.append(self.goal.map.continents[1])
                self.continents.append(self.goal.map.continents[5])
                
            elif r_choice == 4:
                self.continents.append(self.goal.map.continents[3])
                self.continents.append(self.goal.map.continents[2])
                
            elif r_choice == 5:
                self.continents.append(self.goal.map.continents[3])
                self.continents.append(self.goal.map.continents[0])
                
        if self.type == "Capture territories":
            r_choice = random.randint(0, 1)
            if r_choice == 0:
                self.nbpays = 18
                self.nbtroupes = 2
            if r_choice == 1:
                self.nbpays = 24
                self.nbtroupes = 1
                
        if self.type == "Kill all enemies":
            randrange_excl = copy.copy(self.goal.randrange[2])
            try:
                randrange_excl.remove(self.player.id) #Excluding self
            except ValueError:
                pass #If player already lost
            if len(randrange_excl) == 0:
                print("You lost!")
            try:
                randid = random.choice(randrange_excl)
                self.goal.randrange[2].remove(randid) #Prevent mission dupe
                self.target=self.goal.turns.players[randid - 1] 
            except IndexError: #Restricted attackable players
                self.type = self.goal.types[random.randint(0,1)] #Pick different mission
                self.gen_obj()
                
    # Used for goal formatting
    @property
    def description(self):
        if self.type=='capture continents':
            tmp_str='Capture'
            for i in range(0,len(self.continents)):
                tmp_str+=' '+str(self.continents[i].name)
            if self.other_cont:
                tmp_str+=' and another cont'
            return tmp_str
        elif self.type=='capture territories':
            tmp_str = 'Capture '+str(self.nbpays)+' territories' 
            if self.nbtroupes>1:
                tmp_str+=' with '+str(self.nbtroupes)+' troops'
            return tmp_str
        elif self.type=='kill all enemies':
            if self.target.name=='':
                return 'Destory '+str(self.target.id)
            else:
                return 'Destory '+str(self.target.name)

    # Returns goal completion status for game victory
    def getGoalStatus(self):
        if self.type=='capture territories':
            return self.captureTerritory(self.nbpays,self.nbtroupes)
        if self.type=='capture continents':
            return self.captureContinent(self.continents,self.nbtroupes)
        if self.type=='kill all enemies':
            return self.destoryPlayer(self.target)        

    # Used for checking if territory has been captured
    def captureTerritory(self,nb_pays,nb_troupes):
        numOccupyingTroops=0
        for p in self.goal.map.territories:
            if p.nb_troupes>nb_troupes-1 and p.id_player==self.player.id:
                numOccupyingTroops+=1
        if numOccupyingTroops>nb_pays-1:
            self.goal.turns.game_finish=True
            return True
        else:
            return False

    # Checks of all territories in a continent has been captured
    def captureContinent(self,continents,nb_troupes):
        numOccupyingTroops=0
        for c in continents:
            occupiedFlag=True
            for p in c.territories:
                if p.nb_troupes < nb_troupes or p.id_player != self.player.id:
                    occupiedFlag = False
            if occupiedFlag==True:
                numOccupyingTroops+=1
                
        if self.other_cont: # Checks if player have another continent
            additionnal_cont = 0
            other_conts = [x for x in self.goal.map.continents if x not in continents]
            for c in other_conts:
                occupiedFlag = True
                for p in c.territories:
                    if p.nb_troupes < nb_troupes or p.id_player != self.player.id:
                        occupiedFlag = False
                if occupiedFlag == True:
                    additionnal_cont += 1
                    
        if numOccupyingTroops == len(continents):
            if self.other_cont and additionnal_cont>0:
                self.goal.turns.game_finish=True
                return True
            elif not self.other_cont:
                self.goal.turns.game_finish=True
                return True
            else:
                return False
        else:
            return False

    def destoryPlayer(self,player):
        if not player.isalive:
            self.goal.turns.game_finish=True
            return True
        else:
            return False
