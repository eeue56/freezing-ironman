from __future__ import division

# PyQT4 imports
from PyQt4 import QtGui, QtCore, QtOpenGL
from PyQt4.QtOpenGL import QGLWidget

from random import choice
# PyOpenGL imports
import OpenGL.GL as gl
import OpenGL.arrays.vbo as glvbo

import OpenGL.GLU as glu


colours = [(0, 0, 252), (0, 234, 0)]

deep_size = 50

class World(object):

    def __init__(self, player):
        self.player = player
        self.objects = []

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
        glu.gluLookAt(self.world.player.x, self.world.player.y, self.world.player.z - 10,
            self.world.player.x, self.world.player.y, self.world.player.z + 10,
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

    def draw_player(self):
        gl.glBegin(gl.GL_TRIANGLES)

        x = self.world.player.x
        y = self.world.player.y
        z = self.world.player.z
        
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
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()

    def paintGL(self):
        """Paint the scene.
        """

        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)

        self.draw_skybox()
        self.draw_player()

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
        glu.gluPerspective(70, width / height, 0.1, 50)

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

class Player(WorldObject):
    def __init__(self, x, y, z):
        WorldObject.__init__(self, x, y, z)

        self._peak = 5
        self._wave = range(self._peak)
        self._wave = self._wave + self._wave[::-1]
        self._jump_index = 0
        self._start_y = self.y
        self._is_jumping = False

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

        if self._jump_index >= len(self.wave):
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
            
            self.keys = set()

            self.widget = GLPlotWidget(600, 400, self.world)

            self.widget.setGeometry(0, 0, self.widget.width, self.widget.height)
            self.setCentralWidget(self.widget)
            self.show()

            self.paint_timer = QtCore.QTimer()
            QtCore.QObject.connect(self.paint_timer, QtCore.SIGNAL("timeout()"), self.widget.updateGL)

            self.checker = QtCore.QTimer()
            QtCore.QObject.connect(self.checker, QtCore.SIGNAL("timeout()"), self.check)

            self.ticker = QtCore.QTimer()
            QtCore.QObject.connect(self.ticker, QtCore.SIGNAL("timeout()"), self.world.tick)

            QtCore.QMetaObject.connectSlotsByName(self)
            
            self.paint_timer.start(30)
            self.checker.start(25)
            self.ticker.start(25)
            self.resize(800, 600)

        def keyPressEvent(self, event):
            self.keys.add(event.key())

        def keyReleaseEvent(self, event):
            try:
                self.keys.remove(event.key())
            except:
                pass

        def check(self):
            self.world.player.reset()
            mover = self.world.player.movement

            for key in self.keys:  

                if key == QtCore.Qt.Key_A:
                    mover['x'] = -1
                    self.widget.move(x=False)
                elif key == QtCore.Qt.Key_D:
                    mover['x'] = 1
                    self.widget.move(x=True)
                elif key == QtCore.Qt.Key_W:
                    mover['z'] = 1
                    self.widget.move(z=True)
                elif key == QtCore.Qt.Key_S:
                    mover['z'] = -1
                    self.widget.move(z=False)
                elif key == QtCore.Qt.Key_Space:
                    self.world.player.start_jump()

             
    # create the QT App and window
    app = QtGui.QApplication(sys.argv)
    window = TestWindow()
    window.show()
    app.exec_()