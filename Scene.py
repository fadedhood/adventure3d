from direct.showbase.ShowBase import ShowBase
from panda3d.core import GeoMipTerrain, KeyboardButton, Texture, TextureStage, loadPrcFileData, WindowProperties
from direct.task import Task

loadPrcFileData('', 'load-file-type p3assimp')

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.terrain_texture = self.loader.loadTexture("Terrain\\DiffuseMaps\\forest_leaves_02_diffuse_1k.jpg")
        self.terrain_texture.setWrapU(Texture.WMRepeat)
        self.terrain_texture.setWrapV(Texture.WMRepeat)
        ts = TextureStage('ts')

        self.terrain = GeoMipTerrain("terrain")
        self.terrain.setHeightfield("Terrain\\DisperseMaps\\forest_leaves_02_disp_1k.png")
        self.terrain.setBlockSize(32)
        self.terrain.setFactor(10)
        self.terrain.setFocalPoint(self.camera)
        self.terrain.generate()

        # Attach the terrain to the render node
        self.terrain_node = self.terrain.getRoot()
        self.terrain_node.reparentTo(self.render)
        self.terrain_node.setSz(100)  # Adjust the Z-scale to exaggerate the height

        # Apply the texture to the terrain
        self.terrain_node.setTexture(ts, self.terrain_texture)

        scale_factor = 10.0  # Adjust this value to control the repetition rate
        self.terrain_node.setTexScale(ts, scale_factor, scale_factor)

        # Optionally, add some lighting to the scene
        self.setupLights()
        self.initCamera()
        self.hideCursor()

        self.accept("escape", self.showCursor)
        self.accept("mouse1", self.hideCursor)

    def setupLights(self):
        from panda3d.core import DirectionalLight, AmbientLight, Vec4

        # Create a directional light
        dlight = DirectionalLight('dlight')
        dlight.setDirection((-1, -1, -1))
        dlight_np = self.render.attachNewNode(dlight)
        self.render.setLight(dlight_np)

        # Create an ambient light
        alight = AmbientLight('alight')
        alight.setColor(Vec4(0.5, 0.5, 0.5, 1))
        alight_np = self.render.attachNewNode(alight)
        self.render.setLight(alight_np)

    def initCamera(self):
        # Set initial camera position
        self.camera.setPos(0, -100, 200)
        self.camera.lookAt(0, 0, 0)

        # Camera control parameters
        self.cameraSpeed = 200  # Movement speed

        # Mouse sensitivity
        self.mouseSensitivity = 0.2

        # Disable default mouse-based camera control
        self.disableMouse()

    def updateCamera(self, task):
        # Update camera position based on user input
        dt = self.clock.getDt()
        if self.mouseWatcherNode.is_button_down(KeyboardButton.asciiKey('w')):
            self.camera.setY(self.camera, self.cameraSpeed * dt)
        if self.mouseWatcherNode.is_button_down(KeyboardButton.asciiKey('s')):
            self.camera.setY(self.camera, -self.cameraSpeed * dt)
        if self.mouseWatcherNode.is_button_down(KeyboardButton.asciiKey('a')):
            self.camera.setX(self.camera, -self.cameraSpeed * dt)
        if self.mouseWatcherNode.is_button_down(KeyboardButton.asciiKey('d')):
            self.camera.setX(self.camera, self.cameraSpeed * dt)

        if self.mouseWatcherNode.has_mouse():
            # Mouse control for camera orientation
            md = self.win.get_pointer(0)
            x = md.get_x()
            y = md.get_y()

            self.camera.setH(self.camera.getH() - (x - self.win.get_x_size() // 2) * self.mouseSensitivity)
                
            newP = self.camera.getP() - (y - self.win.get_y_size() // 2) * self.mouseSensitivity
            # Clamp the pitch value to be between -80 and 80 degrees
            if newP < -80:
                newP = -80
            elif newP > 80:
                newP = 80
            self.camera.setP(newP)

            # Update the pointer to the center of the window
            self.win.move_pointer(0, self.win.get_x_size() // 2, self.win.get_y_size() // 2)

        # Return Task.cont to keep the task running
        return Task.cont
    
    def hideCursor(self):
        # Hide the mouse cursor
        properties = WindowProperties()
        properties.setCursorHidden(True)
        self.win.requestProperties(properties)
        self.taskMgr.add(self.updateCamera, "updateCamera")

    def showCursor(self):
         # Show the mouse cursor
        properties = WindowProperties()
        properties.setCursorHidden(False)
        self.win.requestProperties(properties)
        self.taskMgr.remove("updateCamera")

app = MyApp()
app.run()
