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
        
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)

        # call the draw method of the world, which then calls the draw method of 
        # everythin in the world        
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
        # the window corner OpenGL coordinates are the same as the world height and width
        gl.glOrtho(0, self.world.width, 0, self.world.height, -1, 1)

 
if __name__ == '__main__':
    # import numpy for generating random data points
    import sys


 
    # define a QT window with an OpenGL widget inside it
    class TestWindow(QtGui.QMainWindow):
        def __init__(self):
            super(TestWindow, self).__init__()
            # initialize the GL widget

            world_height = 175
            world_width = 175

            self.player = Player(110, 110, speed=2)
            levels = [
                [
                    Wall(world_width, world_height, facing=DIRECTIONS['left'], gaps=range(30, 60)),
                    Wall(world_width, world_height, facing=DIRECTIONS['down']),
                    Wall(world_width, world_height, facing=DIRECTIONS['up']),
                    Wall(world_width, world_height, facing=DIRECTIONS['right']),
                    Monster(70, 70, color=COLOURS['white']),
                    Monster(23, 25, color=COLOURS['grey']),
                    Monster(53, 83, color=COLOURS['white']),
                    Monster(10, 40, color=COLOURS['grey'])
                ],
                [
                    Wall(world_width, world_height, facing=DIRECTIONS['left']),
                    Wall(world_width, world_height, facing=DIRECTIONS['down']),
                    Wall(world_width, world_height, facing=DIRECTIONS['up']),
                    Wall(world_width, world_height, facing=DIRECTIONS['right'], gaps=range(60, 90)),
                    Monster(23, 25, color=COLOURS['grey']),
                    Monster(53, 83, color=COLOURS['white']),
                    Monster(10, 40, color=COLOURS['grey'])
                ],
                [
                    Wall(world_width, world_height, facing=DIRECTIONS['up']),
                    Wall(world_width, world_height, facing=DIRECTIONS['down']),
                    Wall(world_width, world_height, facing=DIRECTIONS['left']),
                    Wall(world_width, world_height, facing=DIRECTIONS['right'])
                ]
            ]

            self.world = World(self.player, levels=levels, width=world_width, height=world_height)

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
            self.tick_timer.start(25)
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

            player_movement = DIRECTIONS['still']
            face_movement = DIRECTIONS['still']
            egg_direction = DIRECTIONS['still']
            egg = None

            for key in self.keys:  

                if key == QtCore.Qt.Key_A:
                    face_movement += DIRECTIONS['left']
                elif key == QtCore.Qt.Key_D:
                    face_movement += DIRECTIONS['right']
                elif key == QtCore.Qt.Key_W:
                    face_movement += DIRECTIONS['up']
                elif key == QtCore.Qt.Key_S:
                    face_movement += DIRECTIONS['down']
                    

                elif key == QtCore.Qt.Key_Up:
                    player_movement += DIRECTIONS['up']
                elif key == QtCore.Qt.Key_Down:
                    player_movement += DIRECTIONS['down']
                elif key == QtCore.Qt.Key_Right:
                    player_movement += DIRECTIONS['right']
                elif key == QtCore.Qt.Key_Left:
                    player_movement += DIRECTIONS['left']


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

            if player_movement != DIRECTIONS['still']:
                self.world.player.facing = player_movement
                self.world.player.spawn_egg(self.world)

            self.world.player.movement_facing = face_movement

 
    # create the QT App and window
    app = QtGui.QApplication(sys.argv)
    window = TestWindow()
    window.show()
    app.exec_()
