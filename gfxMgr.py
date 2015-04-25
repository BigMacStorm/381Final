#Andrew Menard and Brian Gaunt
#CS 381
#Graphics Manager

"""
    USE TUTORIAL #6
"""

import ogre.renderer.OGRE as ogre
import math

class GfxMgr:
    
    def __init__(self, engine):
        self.engine = engine
    
    def init(self):
        self.createRoot()
        self.defineResources()
        self.setupRenderSystem()
        self.createRenderWindow()
        self.initializeResourceGroups()
        self.setupScene()

    def createRoot(self):
        self.root = ogre.Root()

    def defineResources(self):
        cf = ogre.ConfigFile()
        cf.load("resources.cfg")

        #start looping through the parsed config file
        seci = cf.getSectionIterator()
        while seci.hasMoreElements():
            #aquire the section to get all contents out
            secName = seci.peekNextKey() #section name (which is the group of the resources)
            settings = seci.getNext()
            #
            for item in settings:
                typeName = item.key #type of resource (zip, folder, etc)
                archName = item.value #filename of the resource itself
                ogre.ResourceGroupManager.getSingleton().addResourceLocation(archName, typeName, secName)
                #add all three things to the ResourceGroupManager

    def setupRenderSystem(self):
        if not self.root.restoreConfig() and not self.root.showConfigDialog():
            raise Exception("User canceled the config dialog! -> Application.setupRenderSystem()")

    def createRenderWindow(self):
        self.root.initialise(True, "Render Window")

    def initializeResourceGroups(self):
        ogre.TextureManager.getSingleton().setDefaultNumMipmaps(5)
        ogre.ResourceGroupManager.getSingleton().initialiseAllResourceGroups()

    def setupScene(self):
        
        '''SETUP SCENEMANAGER'''
        self.sceneManager = self.root.createSceneManager(ogre.ST_GENERIC, "Default SceneManager")
        self.sceneManager.setAmbientLight(ogre.ColourValue(1, 1, 1))
        
        '''SETUP ENVIRONMENT'''
        plane = ogre.Plane ((0, 1, 0), 0)
        meshManager = ogre.MeshManager.getSingleton ()
        meshManager.createPlane ('Ground', 'General', plane,
                                     100000, 100000, 20, 20, True, 
                                     1, 5, 5, (0, 0, 1))
        ent = self.sceneManager.createEntity('GroundEntity', 'Ground')
        self.sceneManager.getRootSceneNode().createChildSceneNode ().attachObject (ent)
        ent.setMaterialName ('Ocean2_Cg')
        ent.castShadows = False
        self.sceneManager.setSkyBox (True, "Examples/SpaceSkyBox", 5000, False)
        #sceneManager.setSkyDome (True, "Examples/CloudySky", 5, 8)

        '''SETUP CAMERAS AND VIEWPORTS'''
        self.camera_Main = self.sceneManager.createCamera("camera_Main")
        #want to set up developer camera so we just have a freeroaming camera
        #with a full screen view port.
        #also will be used for menus that are full screen

        self.camera_P1 = self.sceneManager.createCamera("Camera_P1")
        self.camera_P2 = self.sceneManager.createCamera("Camera_P2")

        viewPort_Main = self.root.getAutoCreatedWindow().addViewport(self.camera_Main, 0, 0, 0, 1, 1)
        viewPort_P1 = self.root.getAutoCreatedWindow().addViewport(self.camera_P1, 1, 0, 0, 0.5, 1)
        viewPort_P2 = self.root.getAutoCreatedWindow().addViewport(self.camera_P2, 2, 0.5, 0, 0.5, 1)
        
        node_Main_camera = self.sceneManager.getRootSceneNode().createChildSceneNode('CamNode_Main',
                                                                    (-1250, 200, 200))

        node_P1_camera = self.sceneManager.getRootSceneNode().createChildSceneNode('CamNode_P1_1',
                                                                   (-1000, 200, 200))
        node_P1_camera.yaw(math.radians(-90))
        node1 = node_P1_camera.createChildSceneNode('PitchNode_P1_1')
        node_P1_camera = self.sceneManager.getRootSceneNode().createChildSceneNode('CamNode_P1_2',
                                                                   (-1500, 200, 200))
        node_P1_camera.yaw(math.radians(-90))
        node2 = node_P1_camera.createChildSceneNode('PitchNode_P1_2')
        
        node1.attachObject(self.camera_P1)
        
        node_P2_camera = self.sceneManager.getRootSceneNode().createChildSceneNode('CamNode_P2_1', (-1000, 200, 200))
        node_P2_camera.yaw(math.radians(-90))
        node1 = node_P2_camera.createChildSceneNode('PitchNode_P2_1')
        node_P2_camera = self.sceneManager.getRootSceneNode().createChildSceneNode('CamNode_P2_2', (-500, 200, 200))
        node_P2_camera.yaw(math.radians(-90))
        node2 = node_P2_camera.createChildSceneNode('PitchNode_P2_2')

        node1.attachObject(self.camera_P2)



    def tick(self, dt):
        self.engine.keepRunning = self.root.renderOneFrame(dt) #boolean type must return
    
    def stop(self):
        pass
