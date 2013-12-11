from __future__ import division

# PyQT4 imports
from PyQt4 import QtGui, QtCore, QtOpenGL
from PyQt4.QtOpenGL import QGLWidget

from random import choice, randint
# PyOpenGL imports
import OpenGL.GL as gl
import OpenGL.arrays.vbo as glvbo

import OpenGL.GLU as glu

from collections import defaultdict


FORWARDS, BACKWARDS, LEFT, RIGHT = range(4)

colours = [(0, 0, 252), (0, 234, 0)]

deep_size = 50


class World(object):

    def __init__(self, player):
        self.player = player
        self.objects = []
        
        self.by_x = defaultdict(list)
        self.by_y = defaultdict(list)
        self.by_z = defaultdict(list)



    def add_objects(self, objects):
        self.objects.extend(objects)

        for object_ in objects:
            self.by_x[object_.x].append(object_)
            self.by_y[object_.y].append(object_)
            self.by_z[object_.z].append(object_)

    def objects_by_selection(self, xs, ys, zs):
        out = []
        for x in xrange(xs[0], xs[-1]):
            cubes = self.by_x[x]
            out.extend([cube for cube in cubes 
                if ys[0] < cube.y < ys[1] 
                and zs[0] < cube.z < zs[1]])
        return out


    def tick(self):
        self.player.tick()


class GLPlotWidget(QGLWidget):
    # default window size

    def __init__(self, width, height, world, *args):
        QGLWidget.__init__(self, *args)
        self.width = width
        self.height = height
        self.world = world

    def draw_ice(self, x, y, z=0):
        gl.glBegin(gl.GL_TRIANGLE_STRIP)
        width = 1
        height = 1

        gl.glColor3f(0, 0, 0.5)
        gl.glVertex3f(x, y, z)
        gl.glVertex3f(x + width, y, z)
        gl.glVertex3f(x, y + height, z)
        
        gl.glVertex3f(x + width, y + height, z)
        gl.glVertex3f(x, y + height, z)
        gl.glColor3f(0, 0.2, 0.7)
        gl.glVertex3f(x + width, y, z)

        gl.glEnd()

    def move(self, x=None, y=None, z=None):
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()


        facing = self.world.player.facing

        #(20 if facing == RIGHT else (-20 if facing == LEFT else 0)

        glu.gluLookAt(self.world.player.x, self.world.player.y, self.world.player.z,
            self.world.player.x + (20 if facing == RIGHT else (-20 if facing == LEFT else 0)), 
            self.world.player.y, 
            self.world.player.z + (20 if facing == FORWARDS else (-20 if facing == BACKWARDS else 0)),
            0, 1, 0)

    def draw_skybox(self):
        gl.glBegin(gl.GL_TRIANGLE_STRIP)
        width = 100
        height = 100
        depth = 0

        x = self.world.player.x
        y = self.world.player.y - 3

        z = self.world.player.z + (deep_size / 2)

        gl.glColor3f(0.2, 0.4, 0.5)
        gl.glVertex3f(x - width, y, z)
        gl.glVertex3f(x + width, y, z)
        gl.glColor3f(0.6, 0.6, 0.2)
        gl.glVertex3f(x - width, y + height, z)

        gl.glEnd()

    def draw_cube(self, cube):
        gl.glBegin(gl.GL_QUADS)                    # Start Drawing The Pyramid

        width = 1
        height = 1
        depth = 1

        x = cube.x
        y = cube.y 
        z = cube.z

        
        gl.glNormal3d(0, 0, 1)
        gl.glVertex3f(x + width, y + height, z)        # Top Right Of The Quad (Top)
        gl.glVertex3f(x, y + height, z)        # Top Left Of The Quad (Top)
        gl.glVertex3f(x, y + height, z + depth)        # Bottom Left Of The Quad (Top)
        gl.glVertex3f(x + width, y + height, z + depth)        # Bottom Right Of The Quad (Top)

        gl.glVertex3f(x + width, y, z + depth)        # Top Right Of The Quad (Bottom)
        gl.glVertex3f(x, y, z + depth)        # Top Left Of The Quad (Bottom)
        gl.glVertex3f(x, y, z)        # Bottom Left Of The Quad (Bottom)
        gl.glVertex3f(x + width, y, z)        # Bottom Right Of The Quad (Bottom)

        gl.glVertex3f(x + width, y + height, z + depth)        # Top Right Of The Quad (Front)
        gl.glVertex3f(x, y + height, z + depth)        # Top Left Of The Quad (Front)
        gl.glVertex3f(x, y, z + depth)        # Bottom Left Of The Quad (Front)
        gl.glVertex3f(x + width, y, z + depth)        # Bottom Right Of The Quad (Front)

        gl.glVertex3f(x + width, y, z)        # Bottom Left Of The Quad (Back)
        gl.glVertex3f(x, y, z)        # Bottom Right Of The Quad (Back)
        gl.glVertex3f(x, y + height, z)        # Top Right Of The Quad (Back)
        gl.glVertex3f(x + width, y + height, z)        # Top Left Of The Quad (Back)

        gl.glVertex3f(x, y + height, z + depth)        # Top Right Of The Quad (Left)
        gl.glVertex3f(x, y + height, z)        # Top Left Of The Quad (Left)
        gl.glVertex3f(x, y, z)        # Bottom Left Of The Quad (Left)
        gl.glVertex3f(x, y, z + depth)        # Bottom Right Of The Quad (Left)

        gl.glVertex3f(x + width, y + height, z)        # Top Right Of The Quad (Right)
        gl.glVertex3f(x + width, y + height, z + depth)        # Top Left Of The Quad (Right)
        gl.glVertex3f(x + width, y, z + depth)        # Bottom Left Of The Quad (Right)
        gl.glVertex3f(x + width, y, z)        # Bottom Right Of The Quad (Right)
        gl.glEnd()                # Done Drawing The Quad
        
    def draw_player(self):
        gl.glBegin(gl.GL_TRIANGLES)
        
        x = 0
        y = 0
        z = 0 
        
        width = 3
        height = 3

        gl.glColor3f(1, 0, 0)
        gl.glVertex3f(x, y, z)

        gl.glColor3f(0.6, 0.2, 0)
        gl.glVertex3f(x + (width / 2), y + height, z)

        gl.glColor3f(0.8, 0.1, 0.2)
        gl.glVertex3f(x + width, y, z)

        gl.glEnd()

    def initializeGL(self):
        """Initialize OpenGL, VBOs, upload data on the GPU, etc.
        """
        # background color
        gl.glClearColor(0, 0, 0, 0)
        gl.glViewport(0, 0, self.width, self.height)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_FOG)
        gl.glFogf(gl.GL_FOG_START, 0.5)
        gl.glFogf(gl.GL_FOG_END, 0.7)
        gl.glFogf(gl.GL_FOG_DENSITY, 0.1)
        gl.glFogf(gl.GL_FOG_COLOR, 0, 0, 0, -0.5)
        gl.glDisable(gl.GL_FOG)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()

    def paintGL(self):
        """Paint the scene.
        """

        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)

        self.draw_skybox()
        self.draw_player()
        player_x = int(self.world.player.x)
        player_y = int(self.world.player.y)
        player_z = int(self.world.player.z)


        render_distances = [10, 6, 15]
        
        for cube in self.world.objects_by_selection(
            [player_x - render_distances[0], player_x + render_distances[0]],
            [player_y - render_distances[1], player_y + render_distances[1]],
            [player_z, player_z + render_distances[2]]):

            gl.glColor3f(*cube.color)
            self.draw_cube(cube)
                

    def resizeGL(self, width, height):
        """Called upon window resizing: reinitialize the viewport.
        """
        # update the window size    
        self.width, self.height = width, height
        # paint within the whole window
        gl.glViewport(0, 0, width, height)
        # set orthographic projection (2D only)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()

        gl.glOrtho(-deep_size, deep_size, -deep_size, deep_size, -deep_size, deep_size)

        gl.glLoadIdentity()
        glu.gluPerspective(90, width / height, 0.1, 50)

        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        #gl.glTranslate(-0.5, -0.4, -3.0)
        
        #gl.glRotatef(180, 0, 0, 1)
        self.move()


class WorldObject(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

        self.movement = {'x': 0, 
            'y' : 0, 
            'z' : 0}

    def move(self):
        self.x += self.movement['x']
        self.y += self.movement['y']
        self.z += self.movement['z']

    def reset(self):
        for k in self.movement:
            self.movement[k] = 0

class Cube(WorldObject):
    def __init__(self, *args):
        WorldObject.__init__(self, *args)
        self.color = (randint(0, 100) / 100, randint(0, 100) / 100, randint(0, 100) / 100)



class Player(WorldObject):
    def __init__(self, x, y, z):
        WorldObject.__init__(self, x, y, z)

        self._peak = 3
        step = self._peak / 5
        self._wave = []

        c = 0

        while c < self._peak:
            self._wave.append(c)
            c += step

        while c > 0:
            self._wave.append(c)
            c -= step

        self._jump_index = 0
        self._start_y = self.y
        self._is_jumping = False

        self.facing = FORWARDS

    def rotate_right(self):
        if self.facing == FORWARDS:
            self.facing = RIGHT
        elif self.facing == RIGHT:
            self.facing = BACKWARDS
        elif self.facing == BACKWARDS:
            self.facing = LEFT
        else:
            self.facing = FORWARDS

    def rotate_left(self):
        if self.facing == FORWARDS:
            self.facing = LEFT
        elif self.facing == LEFT:
            self.facing = BACKWARDS
        elif self.facing == BACKWARDS:
            self.facing = RIGHT
        else:
            self.facing = FORWARDS

    def tick(self):
        self.move()

        if self._is_jumping:
            self.jump()

    def start_jump(self):
        if self._is_jumping:
            return
        self._is_jumping = True
        self._jump_index = 0

    def jump(self):
        self.y = self._start_y + self._wave[self._jump_index]
        self._jump_index += 1

        if self._jump_index >= len(self._wave):
            self._is_jumping = False
            self._jump_index = 0


if __name__ == '__main__':
    # import numpy for generating random data points
    import sys


    # define a QT window with an OpenGL widget inside it
    class TestWindow(QtGui.QMainWindow):
        def __init__(self):
            super(TestWindow, self).__init__()
            # initialize the GL widget
            player = Player(0, 0, 0)
            self.world = World(player)

            numbers = range(-20, 20)

            def generate_world():
                for z in numbers:
                    self.world.add_objects([Cube(x, -3, z) for x in numbers])
                    self.world.add_objects([Cube(x, -2, z) for x in numbers if x == z or x < z])

            generate_world()
            
            self.keys = set()

            self.widget = GLPlotWidget(600, 400, self.world)

            self.widget.setGeometry(0, 0, self.widget.width, self.widget.height)
            self.setCentralWidget(self.widget)
            self.show()

            self.paint_timer = QtCore.QTimer()
            QtCore.QObject.connect(self.paint_timer, QtCore.SIGNAL("timeout()"), self.widget.updateGL)

            self.checker = QtCore.QTimer()
            QtCore.QObject.connect(self.checker, QtCore.SIGNAL("timeout()"), self.check)

            def control():
                self.world.tick()
                self.widget.move()

            self.ticker = QtCore.QTimer()
            QtCore.QObject.connect(self.ticker, QtCore.SIGNAL("timeout()"), control)


            QtCore.QMetaObject.connectSlotsByName(self)
            
            self.paint_timer.start(30)
            self.checker.start(30)
            self.ticker.start(30)


            self.resize(800, 600)

        def keyPressEvent(self, event):
            self.keys.add(event.key())
            self.check()

        def keyReleaseEvent(self, event):
            try:
                self.keys.remove(event.key())
            except:
                print 'enable to remove ', event.key()
                pass

        def check(self):
            self.world.player.reset()
            mover = self.world.player.movement

            for key in self.keys:  

                if key == QtCore.Qt.Key_A:
                    mover['x'] = 1
                    #self.widget.move(x=False)
                elif key == QtCore.Qt.Key_D:
                    mover['x'] = -1
                    #self.widget.move(x=True)
                elif key == QtCore.Qt.Key_W:
                    mover['z'] = 1
                    #self.widget.move(z=True)
                elif key == QtCore.Qt.Key_S:
                    mover['z'] = -1
                    #self.widget.move(z=False)
                elif key == QtCore.Qt.Key_Space:
                    self.world.player.start_jump()
                elif key == QtCore.Qt.Key_E:
                    self.world.player.facing = BACKWARDS
                elif key == QtCore.Qt.Key_Q:
                    self.world.player.facing = FORWARDS

             
    # create the QT App and window
    app = QtGui.QApplication(sys.argv)
    window = TestWindow()
    window.show()
    app.exec_()