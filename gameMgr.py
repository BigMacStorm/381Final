from vector import Vector3


class GameMgr:
    def __init__(self, engine):
        self.engine = engine
        print "starting Game mgr"
        pass

    def init(self):
        self.loadLevel()


    def loadLevel(self):
        self.game1()
        

    def game1(self):
        x = 0
        for entType in self.engine.entityMgr.entTypes:
            ent = self.engine.entityMgr.createEnt(entType, pos = Vector3(0, 0, x))
            x += 400

        self.engine.entityMgr.createLvl1()


    def tick(self, dt):
        pass

    def stop(self):
        pass
        

