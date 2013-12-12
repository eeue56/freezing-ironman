#!/usr/bin/python2

from __future__ import division

# PyQT4 imports
from PyQt4 import QtGui, QtCore, QtOpenGL
from PyQt4.QtOpenGL import QGLWidget
# PyOpenGL imports
import OpenGL.GL as gl
import OpenGL.arrays.vbo as glvbo

from random import choice, randint
from misc import *
from world import World
from world_objects import *


class GLPlotWidget(QGLWidget):

    def __init__(self, width, height, world, *args):
        QGLWidget.__init__(self, *args)
        self.width = width
        self.height = height
        self.world = world
 
    def initializeGL(self):
        """Initialize OpenGL, VBOs, upload data on the GPU, etc.
        """
        # background color
        gl.glClearColor(0,0,0,0)
        gl.glViewport(0, 0, self.width, self.height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()

    def paintGL(self):
        """Paint the scene.
        """
        # clear the buffer
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        # set yellow color for subsequent drawing rendering calls
        
        # tell OpenGL that the VBO contains an array of vertices
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        
        self.world.draw()

    def resizeGL(self, width, height):
        """Called upon window resizing: reinitialize the viewport.
        """
        # update the window size    
        self.width, self.height = width, height
        # paint within the whole window
        gl.glViewport(0, 0, self.width, self.height)
        # set orthographic projection (2D only)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        # the window corner OpenGL coordinates are (-+1, -+1)
        gl.glOrtho(0, 100, 0, 100, -1, 1)

 
if __name__ == '__main__':
    # import numpy for generating random data points
    import sys


 
    # define a QT window with an OpenGL widget inside it
    class TestWindow(QtGui.QMainWindow):
        def __init__(self):
            super(TestWindow, self).__init__()
            # initialize the GL widget

            self.player = Player(50, 50)

            self.world = World(self.player)

            self.widget = GLPlotWidget(100, 100, self.world)
            self.color = COLOURS['white']
            self.keys = set()

            self.widget.setGeometry(0, 0, self.widget.width, self.widget.height)
            self.setCentralWidget(self.widget)
            self.show()

            self.paint_timer = QtCore.QTimer()
            QtCore.QObject.connect(self.paint_timer, QtCore.SIGNAL("timeout()"), self.widget.updateGL)
            
            self.button_timer = QtCore.QTimer()
            QtCore.QObject.connect(self.button_timer, QtCore.SIGNAL("timeout()"), self.check)

            self.tick_timer = QtCore.QTimer()
            QtCore.QObject.connect(self.tick_timer, QtCore.SIGNAL("timeout()"), self.world.tick)

            QtCore.QMetaObject.connectSlotsByName(self)
            
            self.paint_timer.start(30)
            self.tick_timer.start(30)
            self.button_timer.start(25)

            self.resize(600, 400)

        def keyPressEvent(self, event):
            self.keys.add(event.key())

        def keyReleaseEvent(self, event):
            try:
                self.keys.remove(event.key())
            except:
                pass

        def check(self):

            x = self.world.player.x
            y = self.world.player.y

            player_movement = -50

            for key in self.keys:  

                if key == QtCore.Qt.Key_A:
                    player_movement += DIRECTIONS['left'] 
                elif key == QtCore.Qt.Key_D:
                    player_movement += DIRECTIONS['right']
                elif key == QtCore.Qt.Key_W:
                    player_movement += DIRECTIONS['up']
                elif key == QtCore.Qt.Key_S:
                    player_movement += DIRECTIONS['down']

                elif key == QtCore.Qt.Key_Up:
                    self.world.add_object(Egg(x + 2, y + 7, COLOURS['white'], 'Up', 2))
                    self.world.player.facing = DIRECTIONS['up']
                elif key == QtCore.Qt.Key_Down:
                    self.world.add_object(Egg(x + 2, y - 7, COLOURS['white'], 'Down', 2))
                    self.world.player.facing = DIRECTIONS['down']
                elif key == QtCore.Qt.Key_Right:
                    self.world.add_object(Egg(x + 7, y + 2, COLOURS['white'], 'Right', 2))
                    self.world.player.facing = DIRECTIONS['right']
                elif key == QtCore.Qt.Key_Left:
                    self.world.add_object(Egg(x - 7, y + 2, COLOURS['white'], 'Left', 2))
                    self.world.player.facing = DIRECTIONS['left']


                elif key == QtCore.Qt.Key_Space:
                    self.world.add_object(Egg(x, y, COLOURS['white'], 'Up', 2))
                elif key == QtCore.Qt.Key_1:
                    self.world.player.color = COLOURS['white']
                elif key == QtCore.Qt.Key_2:
                    self.world.player.color = COLOURS['grey']
                elif key == QtCore.Qt.Key_3:
                    self.world.player.color = COLOURS['other-grey']
                elif key == QtCore.Qt.Key_4:
                    self.world.player.color = COLOURS['black']

            if player_movement > -50:
                self.world.move_player(player_movement + 50)



 
    # create the QT App and window
    app = QtGui.QApplication(sys.argv)
    window = TestWindow()
    window.show()
    app.exec_()
