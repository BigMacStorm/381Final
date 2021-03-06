#Entity Manager        
from vector import Vector3    
import ent     
import random
  
class EntityMgr:        
    def __init__(self, engine):        
        print "starting entity manager"        
        self.engine = engine        
                
    def init(self):        
        self.entList = []    
        self.lvl1List = []
        self.lvl1ChkPts = []
        self.weaponList = []
        self.numEnts = 0
        self.numObs = 0
        self.numItem_Boost = 0
        self.numItem_Weapon = 0    

        self.entTypes = [ent.Sleek, ent.Destroyer]        

    def createEnt(self, entType, pos = Vector3(0,0,0)):        
        ent = entType(self.engine, self.numEnts, pos = pos)        
        ent.init()        
        self.entList.append(ent)        
        self.numEnts = self.numEnts + 1        
        return ent
                
    def createObs(self, pos = Vector3(0,0,0)):        
        obs = ent.Obstacle(self.engine, self.numObs, pos = pos)        
        obs.init()
        obs.uiname += str(self.numObs)
        self.lvl1List.append(obs)        
        self.numObs = self.numObs + 1        
        return obs

    def createItem_Boost(self, pos = Vector3(0,0,0)):        
        item = ent.Item_Boost(self.engine, self.numItem_Boost, pos = pos)        
        item.init()
        item.uiname += str(self.numItem_Boost)
        self.lvl1List.append(item)        
        self.numItem_Boost = self.numItem_Boost + 1        
        return item

    def destroyCurrentLevel(self):
        del lvl1List[:]
        del lvl1ChkPts[:]
    
    def createItem_Weapon(self, pos = Vector3(0,0,0)):
        item = ent.Item_Weapon(self.engine, self.numItem_Weapon, pos = pos)
        item.init()
        item.uiname += str(self.numItem_Weapon)
        self.lvl1List.append(item)
        self.numItem_Weapon += 1
        return item
        
    def createLvl1(self):
        #create back of start lane
        vector = Vector3(-250,0,0)
        for i in xrange(0,3):
            self.createObs(vector)
            vector -= Vector3(0,0,100)
        vector = Vector3(-250,0,100)
        for i in xrange(0,6):
            self.createObs(vector)
            vector += Vector3(0,0,100)
        #create first leg, both sides
        for i in xrange(0,100):
            vector = Vector3((i * 100)-250,0,0)
            self.lvl1ChkPts.append(vector)
            self.createObs(vector + Vector3(0,0,650))
            self.createObs(vector + Vector3(0,0, -250))
        #make turn's right edge
        for i in xrange(0,13):
            vector = Vector3(100 + self.lvl1ChkPts[-1].x, 0, 0)
            self.createObs(vector + Vector3(0,0,650))
            if i < 7:
                self.lvl1ChkPts.append(vector)
                
        #make turn's top edge
        nextX = self.lvl1ChkPts[-1].x
        turnPoint = self.lvl1ChkPts[-1]
        for i in xrange(0,35):
            vector = Vector3(nextX, 0, turnPoint.z - (100*i))
            self.createObs(vector + Vector3(200,0,650))
            if i < 20:
                self.lvl1ChkPts.append(vector)
            
        #make turn's bottom edge
        nextX = turnPoint.x
        for i in xrange(0,14):
            vector = Vector3(nextX, 0, turnPoint.z - (100*i))
            self.createObs(vector + Vector3(-650, 0, -250))
            
        #make return right edge
        turnPoint = self.lvl1ChkPts[-1]
        for i in xrange(0,124):
            vector = Vector3(turnPoint.x - (100*i), 0, turnPoint.z)
            self.lvl1ChkPts.append(vector)
            self.createObs(vector + Vector3(100,0,-850))
            if i < 116:
                self.createObs(vector + Vector3(-650,0,250))
        
        self.placeRandomItemsOnCheckpoint()

            
    def tick(self, dt):        
        for ent in self.entList:        
            ent.tick(dt)        
        for ent in self.weaponList:
            ent.tick(dt)
                
    def stop(self):        
        pass
        
    def placeRandomItemsOnCheckpoint(self):
        for i in xrange(0,50):
            choice = random.choice(self.lvl1ChkPts)
            boost = random.randint(0,50)
            weapon = random.randint(0,100)
            if boost < 30:
                if weapon < 50:    
                    self.createItem_Boost(choice + Vector3(random.randint(-300,300),0,random.randint(-300,300)))
                else:
                    self.createItem_Weapon(choice + Vector3(random.randint(-300,300),10,random.randint(-300,300)))
            else:
                self.createObs(choice + Vector3(random.randint(-300,300), 0, random.randint(-300,300)))
        
        
        
        
        
        
        
        
        
        
