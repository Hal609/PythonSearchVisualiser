from panda3d.core import Point3
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import LVector3, LVector4
from panda3d.core import DirectionalLight
from panda3d.core import CullFaceAttrib, AntialiasAttrib
from navigate_maze import get_next_pos
import numpy as np
import random
import math

class VoxelGrid(ShowBase):
    def __init__(self, numpy_grid):
        super().__init__()

        self.num_visited = 0
        self.done = False
        self.cam_done = False
        self.tick = 0.1
        self.ticked = False
        self.grid2d = numpy_grid

        self.cam_pos = Point3(0, 0, 0)
        self.agent_position = Point3(1.5, 0.5, 0)

        self.render.setShaderAuto()  # Enable shaders
        
        # Set up camera
        self.camLens.setNearFar(1, 500)

        # Set up lighting
        self.setup_lighting()

        # Create the voxel grid
        self.create_voxel_grid(*self.grid2d.shape, 1)
        self.create_floor()
        self.create_agent(self.agent_position)

        # Update the scene at a consistent frame rate
        self.taskMgr.add(self.spin_camera, "spin_camera_task")
        self.taskMgr.add(self.move_agent, "move_agent_task")
        self.taskMgr.add(self.tick_frame, "tick_frame_task")

        self.render.setDepthTest(True)
        self.render.setDepthWrite(True)

    def create_agent(self, position):
        self.agent = self.loader.loadModel("models/box")

        self.agent.setScale(0.5)
        self.agent.setPos(position)
        self.agent.setColor(0.99, 0.5, 0.5, 1)

        self.agent.setAttrib(CullFaceAttrib.make(CullFaceAttrib.MCullNone))
        
        self.agent.reparentTo(self.render)

    def tick_frame(self, task):
        if self.tick == round(task.time, 1):
            self.tick = round(task.time + 0.1, 1)
            self.ticked = True
        else:
            self.ticked = False
            self.tick == round(task.time + 0.1, 1)
        return Task.cont
    
    def move_agent(self, task):
        # if self.done: return Task.cont

        if self.ticked and 10*self.tick % 2 == 0:
            x, y, _ = self.position_to_index(self.agent_position)
            next_pos = get_next_pos(self.grid2d, (x, y))
            self.agent_step(next_pos)
            self.done = self.is_done(next_pos)
        return Task.cont
    
    def position_to_index(self, position):
        return (round(position.x + 0.5), round(position.y + 0.5), position.z)
    
    def index_to_position(self, index):
        return Point3(index[0] - 0.5, index[1] - 0.5, 0)
    
    def agent_step(self, next_pos):
        self.add_visited_marker(self.agent_position, next_pos)
        self.agent_position = self.index_to_position(next_pos)
        self.agent.setPos(self.agent_position)

    def is_done(self, next_pos):
        height, width = self.grid2d.shape
        if next_pos == (height - 2, width - 2):
            x, y, z = self.agent_position
            new_x, new_y, _ = self.position_to_index(Point3(x, y+1, z))
            self.agent_step((new_x, new_y))
            return True
        return False

    def add_visited_marker(self, position, next_pos):
        self.num_visited += 1
        self.marker = self.loader.loadModel("models/box")

        self.marker.setSz(0.001)
        self.marker.setPos(position)
        self.marker.setZ(-0.4)
        colour_scale_factor = 1/(1+math.e**(-self.num_visited*0.01))
        self.marker.setColor(colour_scale_factor, 0.5/colour_scale_factor, 0.5*colour_scale_factor+0.5, 1)

        self.marker.setAttrib(CullFaceAttrib.make(CullFaceAttrib.MCullNone))
        
        self.marker.reparentTo(self.render)

    def setup_lighting(self):
        # self.light = self.render.attachNewNode(Spotlight("Spot"))
        self.light = self.render.attachNewNode(DirectionalLight("DirectionalLights"))
        self.light.node().setDirection(LVector3(-1, -0.5, -1))
        self.light.node().setScene(self.render)
        self.light.node().setColor(LVector4(0.7, 0.7, 0.7, 1))
        self.light.node().setShadowCaster(True)
        self.render.setLight(self.light)

        self.light2 = self.render.attachNewNode(DirectionalLight("DirectionalLights"))
        self.light2.node().setDirection(LVector3(1, 1, -1))
        self.light2.node().setScene(self.render)
        self.light2.node().setColor(LVector4(0.5, 0.5, 0.5, 1))
        self.light2.node().setShadowCaster(True)
        self.render.setLight(self.light2)

        # Important! Enable the shader generator.
        self.render.setShaderAuto()

    def create_floor(self):
        voxel = self.loader.loadModel("models/box")

        voxel.setSx(self.grid2d.shape[0] + 1)
        voxel.setSy(-(self.grid2d.shape[0] + 1))
        voxel.setPos(Point3(self.grid2d.shape[0]/2 - 1, self.grid2d.shape[1]/2 - 1, -1))
        colour = (0.647, 0.509, 0.444)
        voxel.setColor(*colour, 1)

        voxel.setAttrib(CullFaceAttrib.make(CullFaceAttrib.MCullNone))
        
        voxel.reparentTo(self.render)

    def create_voxel_grid(self, width, depth, height):
        """Creates a grid of small cubes."""
        for x in range(width):
            for y in range(depth):
                for z in range(height):
                    if self.grid2d[x][y] == 1:
                        self.create_voxel(x, y, 0)

    def create_voxel(self, x, y, z):
        """Creates a single voxel cube at a given position."""
        voxel = self.loader.loadModel("models/box")
        # voxel.setTwoSided(True)
        size = 1.0
        voxel.setPos(Point3(x - size/2, y - size/2, z))
        voxel.setScale(size)  # Smaller size for visibility in a large grid

        colours = [(0.8, 0.84, 0.68), (0.91, 0.93, 0.79), (1.0, 0.98, 0.88), (0.98, 0.93, 0.8)]
        colour = random.choice(colours)
        voxel.setColor(*colour, 1)

        voxel.setAttrib(AntialiasAttrib.make(AntialiasAttrib.M_line))
        voxel.setAttrib(CullFaceAttrib.make(CullFaceAttrib.MCullNone))

        # voxel.setShaderAuto()
        
        voxel.reparentTo(self.render)

    def spin_camera(self, task):
        """Rotate camera around the grid."""
        angleDegrees = task.time * 0.5
        angleRadians = angleDegrees * (3.14159 / 180.0)
        centre = (self.grid2d.shape[0]/2, self.grid2d.shape[1]/2)
        
        if (self.done and self.ticked and self.tick*100 % 100 == 0) or self.cam_done:
            move_speed = 0.5

            distance = (self.grid2d.shape[0] + self.grid2d.shape[1])/2
            cam_target = LVector3(centre[0] + math.cos(angleRadians)*distance, -centre[1] + math.sin(angleRadians)*distance, 45)
            dif = cam_target - self.cam_pos
            dif_x, dif_y, dif_z = dif
            dif_length = (dif_x**2 + dif_y**2 +dif_z**2)**(0.5)
            if dif_length > 1.1:
                self.cam_pos += dif.normalized()*move_speed
            else:
                self.cam_pos = cam_target
            self.cam_done = True
        else:
            distance = 10 + (self.grid2d.shape[0] + self.grid2d.shape[1])
            self.cam_pos = LVector3(centre[0] + math.sin(angleRadians)*distance, -centre[1] + math.cos(angleRadians)*distance, (self.grid2d.shape[0] + self.grid2d.shape[1])/2)

        self.camera.setPos(self.cam_pos)
        self.camera.lookAt(*centre, 0)
        return Task.cont

def run_grid(npgrid):
    app = VoxelGrid(npgrid)
    app.run()
