import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS
import math
from vector import Vector3

class ControlMgr:
    def __init__(self, engine):
        self.engine = engine

    def init(self):
        self.keyboard = self.engine.inputMgr.keyboard
        self.stopped = False

    def tick(self, dt):
        if self.stopped == True:
            return
            
        self.keyboard.capture()
        
        self.player1 = self.engine.entityMgr.entList[0]
        self.player2 = self.engine.entityMgr.entList[1]

        self.mainMenu = self.engine.inputMgr.inputListener.mainMenu


        if not self.mainMenu:
            if not self.keyboard.isKeyDown(OIS.KC_UP) and not self.player1.boosting:
                pass
            if(self.engine.inputMgr.joystick_count > 0):
                if self.keyboard.isKeyDown(OIS.KC_UP) or self.engine.inputMgr.joysticks[0].get_axis(5) > 0:
                    nextAccel = self.player1.speed + self.player1.acceleration
                    if nextAccel < self.player1.maxSpeed:
                        self.player1.desiredSpeed += self.player1.acceleration
                
                if self.keyboard.isKeyDown(OIS.KC_DOWN) or self.engine.inputMgr.joysticks[0].get_axis(2) > 0:
                    nextDecel = self.player1.speed - self.player1.acceleration
                    if self.player1.desiredSpeed > 0:
                        self.player1.speed -= self.player1.acceleration
                    if nextDecel > (-1*self.player1.maxSpeed/2):
                        self.player1.desiredSpeed -= self.player1.acceleration
                            
                if self.keyboard.isKeyDown(OIS.KC_LEFT) or self.engine.inputMgr.joysticks[0].get_axis(0) < -.6:
                    if self.player1.desiredHeading < 0:
                        self.player1.desiredHeading = 357
                        self.player1.yaw = 357
                        self.player1.currentYaw = 357
                    if self.player1.speed > 0 or self.player1.speed < -1:
                        self.player1.desiredHeading -= self.player1.turningRate
                        self.player1.yaw -= self.player1.turningRate
                            
                if self.keyboard.isKeyDown(OIS.KC_RIGHT) or self.engine.inputMgr.joysticks[0].get_axis(0) > 0.6:
                    if self.player1.desiredHeading >= 360:
                        self.player1.desiredHeading = 0
                        self.player1.yaw = 0
                        self.player1.currentYaw = 0
                    if self.player1.speed > 0 or self.player1.speed < -1:
                        self.player1.desiredHeading += self.player1.turningRate
                        self.player1.yaw += self.player1.turningRate
            else:
                if self.keyboard.isKeyDown(OIS.KC_UP):
                    nextAccel = self.player1.speed + self.player1.acceleration
                    if nextAccel < self.player1.maxSpeed:
                        self.player1.desiredSpeed += self.player1.acceleration          
                if self.keyboard.isKeyDown(OIS.KC_DOWN):
                    nextDecel = self.player1.speed - self.player1.acceleration
                    if self.player1.desiredSpeed > 0:
                        self.player1.speed -= self.player1.acceleration
                    if nextDecel > (-1*self.player1.maxSpeed/2):
                        self.player1.desiredSpeed -= self.player1.acceleration
                            
                if self.keyboard.isKeyDown(OIS.KC_LEFT):
                    if self.player1.desiredHeading < 0:
                        self.player1.desiredHeading = 357
                        self.player1.yaw = 357
                        self.player1.currentYaw = 357
                    if self.player1.speed > 0 or self.player1.speed < -1:
                        self.player1.desiredHeading -= self.player1.turningRate
                        self.player1.yaw -= self.player1.turningRate
                            
                if self.keyboard.isKeyDown(OIS.KC_RIGHT):
                    if self.player1.desiredHeading >= 360:
                        self.player1.desiredHeading = 0
                        self.player1.yaw = 0
                        self.player1.currentYaw = 0
                    if self.player1.speed > 0 or self.player1.speed < -1:
                        self.player1.desiredHeading += self.player1.turningRate
                        self.player1.yaw += self.player1.turningRate

            if(self.engine.inputMgr.joystick_count > 0):
                if (self.keyboard.isKeyDown(OIS.KC_RCONTROL) or self.engine.inputMgr.joysticks[0].get_button(0)) and self.player1.weaponUp == True:
                    weapon = self.player1.heldWeapon
                    weapon.aspects[1].node.detachObject(weapon.aspects[1].pEnt) #detach from current node (player)
                    weapon.aspects[1].node = self.engine.gfxMgr.sceneManager.getRootSceneNode().createChildSceneNode(weapon.uiname + 'weaponnode' + str(weapon.eid), self.player1.pos  + ogre.Vector3(0,20,4))
                    weapon.aspects[1].node.attachObject(weapon.aspects[1].pEnt)
                    weapon.aspects[1].node.scale(ogre.Vector3(10,10,10))
                    
                    weapon.speed = self.player1.speed
                    weapon.heading = self.player1.heading
                    weapon.pos = self.player1.pos
                    desiredHeading = self.player1.heading
                    desiredSpeed = self.player1.heldWeapon.maxSpeed
                    yaw = self.player1.yaw
                    weapon.desiredHeading = desiredHeading
                    weapon.desiredSpeed = desiredSpeed
                    weapon.yaw = yaw
                    if weapon.currentYaw < weapon.yaw:
                        weapon.aspects[1].node.yaw(-1*math.radians(weapon.yaw - weapon.currentYaw))
                        weapon.currentYaw += weapon.yaw
                    elif weapon.currentYaw > weapon.yaw:
                        weapon.aspects[1].node.yaw(math.radians(weapon.currentYaw - weapon.yaw))
                    
                    self.engine.entityMgr.weaponList.append(weapon)
                    weapon.firedFrom = self.player1.uiname
                    self.player1.weaponUp = False
                    weapon.held = False
            else:
                if self.keyboard.isKeyDown(OIS.KC_RCONTROL) and self.player1.weaponUp == True:
                    weapon = self.player1.heldWeapon
                    weapon.aspects[1].node.detachObject(weapon.aspects[1].pEnt) #detach from current node (player)
                    weapon.aspects[1].node = self.engine.gfxMgr.sceneManager.getRootSceneNode().createChildSceneNode(weapon.uiname + 'weaponnode' + str(weapon.eid), self.player1.pos  + ogre.Vector3(0,20,4))
                    weapon.aspects[1].node.attachObject(weapon.aspects[1].pEnt)
                    weapon.aspects[1].node.scale(ogre.Vector3(10,10,10))
                    
                    weapon.speed = self.player1.speed
                    weapon.heading = self.player1.heading
                    weapon.pos = self.player1.pos
                    desiredHeading = self.player1.heading
                    desiredSpeed = self.player1.heldWeapon.maxSpeed
                    yaw = self.player1.yaw
                    weapon.desiredHeading = desiredHeading
                    weapon.desiredSpeed = desiredSpeed
                    weapon.yaw = yaw
                    if weapon.currentYaw < weapon.yaw:
                        weapon.aspects[1].node.yaw(-1*math.radians(weapon.yaw - weapon.currentYaw))
                        weapon.currentYaw += weapon.yaw
                    elif weapon.currentYaw > weapon.yaw:
                        weapon.aspects[1].node.yaw(math.radians(weapon.currentYaw - weapon.yaw))
                    
                    self.engine.entityMgr.weaponList.append(weapon)
                    weapon.firedFrom = self.player1.uiname
                    self.player1.weaponUp = False
                    weapon.held = False

            if(self.engine.inputMgr.joystick_count > 1):
                if (self.keyboard.isKeyDown(OIS.KC_NUMPADENTER) or self.engine.inputMgr.joysticks[1].get_button(0)) and self.player2.weaponUp == True :
                    weapon = self.player2.heldWeapon
                    weapon.aspects[1].node.detachObject(weapon.aspects[1].pEnt) #detach from current node (player)
                    weapon.aspects[1].node = self.engine.gfxMgr.sceneManager.getRootSceneNode().createChildSceneNode(weapon.uiname + 'weaponnode' + str(weapon.eid), self.player2.pos  + ogre.Vector3(0,20,4))
                    weapon.aspects[1].node.attachObject(weapon.aspects[1].pEnt)
                    weapon.aspects[1].node.scale(ogre.Vector3(10,10,10))
                    
                    weapon.speed = self.player2.speed
                    weapon.heading = self.player2.heading
                    weapon.pos = self.player2.pos
                    desiredHeading = self.player2.heading
                    desiredSpeed = self.player2.heldWeapon.maxSpeed
                    yaw = self.player2.yaw
                    weapon.desiredHeading = desiredHeading
                    weapon.desiredSpeed = desiredSpeed
                    weapon.yaw = yaw
                    self.engine.entityMgr.weaponList.append(weapon)
                    weapon.firedFrom = self.player2.uiname
                    self.player2.weaponUp = False
                    weapon.held = False
            else:
                if self.keyboard.isKeyDown(OIS.KC_NUMPADENTER) and self.player2.weaponUp == True :
                    weapon = self.player2.heldWeapon
                    weapon.aspects[1].node.detachObject(weapon.aspects[1].pEnt) #detach from current node (player)
                    weapon.aspects[1].node = self.engine.gfxMgr.sceneManager.getRootSceneNode().createChildSceneNode(weapon.uiname + 'weaponnode' + str(weapon.eid), self.player2.pos  + ogre.Vector3(0,20,4))
                    weapon.aspects[1].node.attachObject(weapon.aspects[1].pEnt)
                    weapon.aspects[1].node.scale(ogre.Vector3(10,10,10))
                    
                    weapon.speed = self.player2.speed
                    weapon.heading = self.player2.heading
                    weapon.pos = self.player2.pos
                    desiredHeading = self.player2.heading
                    desiredSpeed = self.player2.heldWeapon.maxSpeed
                    yaw = self.player2.yaw
                    weapon.desiredHeading = desiredHeading
                    weapon.desiredSpeed = desiredSpeed
                    weapon.yaw = yaw
                    self.engine.entityMgr.weaponList.append(weapon)
                    weapon.firedFrom = self.player2.uiname
                    self.player2.weaponUp = False
                    weapon.held = False               

        if not self.mainMenu:
            if not self.keyboard.isKeyDown(OIS.KC_NUMPAD8) and not self.player2.boosting:
                pass

            if(self.engine.inputMgr.joystick_count > 1):
                if self.keyboard.isKeyDown(OIS.KC_NUMPAD8) or self.engine.inputMgr.joysticks[1].get_axis(5) > 0.2:
                    nextAccel = self.player2.speed + self.player2.acceleration
                    if nextAccel < self.player2.maxSpeed:
                        self.player2.desiredSpeed += self.player2.acceleration
                
                if self.keyboard.isKeyDown(OIS.KC_NUMPAD5) or self.engine.inputMgr.joysticks[1].get_axis(2) > 0.2:
                    nextDecel = self.player2.speed - self.player2.acceleration
                    if nextDecel > (-1*self.player2.maxSpeed/2):
                        self.player2.desiredSpeed -= self.player2.acceleration
                            
                if self.keyboard.isKeyDown(OIS.KC_NUMPAD4) or self.engine.inputMgr.joysticks[1].get_axis(0) < -.6:
                    if self.player2.desiredHeading < 0:
                        self.player2.desiredHeading = 357
                        self.player2.yaw = 357
                        self.player2.currentYaw = 357
                    if self.player2.speed > 0 or self.player2.speed < -1:
                        self.player2.desiredHeading -= self.player2.turningRate
                        self.player2.yaw -= self.player2.turningRate
                        
                if self.keyboard.isKeyDown(OIS.KC_NUMPAD6) or self.engine.inputMgr.joysticks[1].get_axis(0) > 0.6:
                    if self.player2.desiredHeading >= 360:
                        self.player2.desiredHeading = 0
                        self.player2.yaw = 0
                        self.player2.currentYaw = 0
                    if self.player2.speed > 0 or self.player2.speed < -1:
                        self.player2.desiredHeading += self.player2.turningRate
                        self.player2.yaw += self.player2.turningRate
            else:
                if self.keyboard.isKeyDown(OIS.KC_NUMPAD8):
                    nextAccel = self.player2.speed + self.player2.acceleration
                    if nextAccel < self.player2.maxSpeed:
                        self.player2.desiredSpeed += self.player2.acceleration
                
                if self.keyboard.isKeyDown(OIS.KC_NUMPAD5):
                    nextDecel = self.player2.speed - self.player2.acceleration
                    if nextDecel > (-1*self.player2.maxSpeed/2):
                        self.player2.desiredSpeed -= self.player2.acceleration
                            
                if self.keyboard.isKeyDown(OIS.KC_NUMPAD4):
                    if self.player2.desiredHeading < 0:
                        self.player2.desiredHeading = 357
                        self.player2.yaw = 357
                        self.player2.currentYaw = 357
                    if self.player2.speed > 0 or self.player2.speed < -1:
                        self.player2.desiredHeading -= self.player2.turningRate
                        self.player2.yaw -= self.player2.turningRate
                        
                if self.keyboard.isKeyDown(OIS.KC_NUMPAD6):
                    if self.player2.desiredHeading >= 360:
                        self.player2.desiredHeading = 0
                        self.player2.yaw = 0
                        self.player2.currentYaw = 0
                    if self.player2.speed > 0 or self.player2.speed < -1:
                        self.player2.desiredHeading += self.player2.turningRate
                        self.player2.yaw += self.player2.turningRate


        if self.keyboard.isKeyDown(OIS.KC_SPACE):
            for ent in self.engine.entityMgr.entList:
                ent.speed = 0
                ent.desiredSpeed = 0
        

    def stop(self):
        self.stopped = True
        

    















