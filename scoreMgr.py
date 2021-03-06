#Entity Manager
import os.path        
import datetime
from vector import Vector3
import ent     
import random
  
class ScoreMgr:        

    def __init__(self, engine):
        print "starting score manager"
        self.engine = engine
    
    def init(self):
        self.scoreList = []
        self.p1Time = "0"
        self.p2Time = "0"
        self.scoreNum = 0
        currentscore = []
        curPiece = 1
        if os.path.isfile('HighScores'):
            with open('HighScores', 'r') as scoreFile:
                for piece in self.readByTokens(scoreFile):
                    if curPiece < 4:
                        #get piece 1, 2, then 3
                        currentscore.append(piece)
                        curPiece += 1
                    elif curPiece == 4:
                        #get fourth piece, add to list, reset curPiece
                        currentscore.append(piece)
                        self.scoreList.append(currentscore)
                        currentscore = []
                        curPiece = 1
                    else:
                        curPiece = 1
        else:
            #highscores does not exist
            pass
        

    def tick(self, dt):
        pass
        
    def addCurrentTime(self, player):
        date = datetime.datetime.now().strftime("%m/%d/%Y")
        realtime = datetime.datetime.now().strftime("%I:%M%p")
        if player == "Player1" and self.engine.selectionMgr.p1End:
            self.p1Time = self.engine.overlayMgr.overlayList[1].curTime
        elif player == "Player2" and self.engine.selectionMgr.p2End:
            self.p2Time = self.engine.overlayMgr.overlayList[1].curTime
        currentscore = []
        currentscore.append(player)
        currentscore.append(date)
        currentscore.append(realtime)
        currentscore.append(str(self.engine.overlayMgr.overlayList[1].curTime))
        self.scoreList.append(currentscore)
        self.scoreNum += 1
        self.scoreList.sort(key=lambda x: float(x[3]))

    def stop(self):
        file = open('HighScores', 'w')
        counter = 0
        for score in self.scoreList:
            if counter < 10:
                file.write(score[0] + ' ' + score[1] + ' ' + score[2] + ' ' + score[3] + ' ' + '\n')
            counter += 1
        file.close()
        
    def printScoreList(self):
        for score in self.scoreList:
            print score[0] + ' ' + score[1] + ' ' + score[2] + ' ' + score[3]
            
    def readByTokens(self, fileobj):
        for line in fileobj:
            for token in line.split():
                yield token
        
        
        
        
        
