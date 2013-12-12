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


def random_color():
    return tuple(y / 255 for y in (randint(0, 255), randint(0, 255), randint(0, 255)))


class Player(object):
    def __init__(self, x, y, health=3, color=COLOURS['grey']):
        self.x = x
        self.y = y
        self.health = health
        self.facing = DIRECTIONS['up']
        self.color = color

    def new_color(self):
        o = []

        for i in self.color:
        
            i *= 255
        
            if i < 5:
                i += randint(10, 25)
            elif i > 250:
                i -= randint(10, 25)
            else:
                i += randint(-20, 25)

            o.append(i / 255)

        self.color = tuple(o)

    def tick(self):
        pass


class GLPlotWidget(QGLWidget):
    # default window size
    width, height = 96, 96
    bunny_point = [30, 50]
    player = Player(20, 20)
    eggs = {v : [] for v in COLOURS.values()}
    monsters = [Player(randint(0, 96), randint(0, 64), randint(15, 50), random_color()) for _ in xrange(randint(5, 20))]
 
    def initializeGL(self):
        """Initialize OpenGL, VBOs, upload data on the GPU, etc.
        """
        # background color
        gl.glClearColor(0,0,0,0)
        gl.glViewport(0, 0, self.width, self.height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
 
    def draw_square(self, x, y, size=1):
        gl.glRectf(x, y, x + size, y + size)

    def add_egg(self, x, y, color=COLOURS['white'], direction=0, speed=0):
        self.eggs[color].append([x, y, direction, speed, False])

    def draw_eggs(self):        

        for color, items in self.eggs.iteritems():
            r, g, b = color
            gl.glColor3f(r, g, b)
            for item in items[:]:

                x = item[0]
                y = item[1]

                if x < 0 or x > self.width or y < 0 or y > self.height:
                    items.remove(item)
                    continue

                goto_break = False

                for monster in self.monsters[:]:
                    if monster.x < x < monster.x + 5 and monster.y < y < monster.y + 5:
                        if item[4]:
                            monster.health -= 0.9
                        item[4] = True

                        monster.health -= 0.5
                        monster.new_color()
                        goto_break = True

                        if monster.health < 0:
                            self.monsters.remove(monster)
                        break


                if goto_break:
                    pass
                else:
                    gl.glColor3f(r, g, b)

                if item[4]:
                    r1, g1, b1 = COLOURS['red']
                    gl.glColor3f(r1, g1, b1)

                self.draw_square(x, y, 1)

                if item[2] == 'Up':
                    item[1] = y + item[3]
                elif item[2] == 'Down':
                    item[1] = y - item[3]
                elif item[2] == 'Right':
                    item[0] = x + item[3]
                elif item[2] == 'Left':
                    item[0] = x - item[3]  

    def draw_player(self, player):

        gl.glPushMatrix()

        r, g, b = player.color
        gl.glColor3f(r, g, b)

        if player.facing in (DIRECTIONS['down'], DIRECTIONS['up']):
            for x in xrange(player.x, player.x + 5):
                for y in xrange(player.y, player.y + 2):
                    self.draw_square(x, y)
            if player.facing == DIRECTIONS['up']:
                self.draw_square(x - 3, y + 1)
                self.draw_square(x - 2, y + 1)
                self.draw_square(x - 2, y + 2)
                self.draw_square(x - 1, y + 1)
            else:
                y = player.y
                self.draw_square(x - 3, y - 1)
                self.draw_square(x - 2, y - 1)
                self.draw_square(x - 2, y - 2)
                self.draw_square(x - 1, y - 1)
        else:
            for x in xrange(player.x, player.x + 2):
                for y in xrange(player.y, player.y + 5):
                    self.draw_square(x, y)
            if player.facing == DIRECTIONS['right']:
                self.draw_square(x + 1, y - 1)
                self.draw_square(x + 1, y - 2)
                self.draw_square(x + 1, y - 3)
                self.draw_square(x + 2, y - 2)
            else:
                x = player.x
                self.draw_square(x - 1, y - 1)
                self.draw_square(x - 1, y - 2)
                self.draw_square(x - 1, y - 3)
                self.draw_square(x - 2, y - 2)
       

        gl.glPopMatrix() 


    def move_player(self, direction):
        self.player.move(direction)

    def paintGL(self):
        """Paint the scene.
        """
        # clear the buffer
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        # set yellow color for subsequent drawing rendering calls
        
        # tell OpenGL that the VBO contains an array of vertices
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        
        r, g, b = COLOURS['grey']
        gl.glColor3f(r, g, b)

        self.draw_eggs()
        self.draw_player(self.player)

        for monster in self.monsters:
            self.draw_player(monster)

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
        gl.glOrtho(0, 96, 0, 96, -1, 1)
 
if __name__ == '__main__':
    # import numpy for generating random data points
    import sys


 
    # define a QT window with an OpenGL widget inside it
    class TestWindow(QtGui.QMainWindow):
        def __init__(self):
            super(TestWindow, self).__init__()
            # initialize the GL widget
            self.widget = GLPlotWidget()
            self.color = COLOURS['white']
            self.keys = set()

            self.widget.setGeometry(0, 0, self.widget.width, self.widget.height)
            self.setCentralWidget(self.widget)
            self.show()

            self.paint_timer = QtCore.QTimer()
            QtCore.QObject.connect(self.paint_timer, QtCore.SIGNAL("timeout()"), self.widget.updateGL)
            
            self.button_timer = QtCore.QTimer()
            QtCore.QObject.connect(self.button_timer, QtCore.SIGNAL("timeout()"), self.check)

            self.monster_timer = QtCore.QTimer()
            QtCore.QObject.connect(self.monster_timer, QtCore.SIGNAL("timeout()"), self.move_monsters)

            QtCore.QMetaObject.connectSlotsByName(self)
            
            self.paint_timer.start(30)
            self.button_timer.start(25)
            self.monster_timer.start(100)

            self.resize(600, 400)

        def keyPressEvent(self, event):
            self.keys.add(event.key())

        def keyReleaseEvent(self, event):
            try:
                self.keys.remove(event.key())
            except:
                pass

        def move_monsters(self):
            for monster in self.widget.monsters:
                if 4 < monster.x < (self.widget.width - 4):
                    monster.x += randint(-1, 1)
                if 2 < monster.y < (self.widget.height - 2):
                    monster.y += randint(-1, 1)

        def check(self):

            x = self.widget.player.x
            y = self.widget.player.y

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
                    self.widget.add_egg(x + 2, y + 7, COLOURS['white'], 'Up', 2)
                    self.widget.player.facing = DIRECTIONS['up']
                elif key == QtCore.Qt.Key_Down:
                    self.widget.add_egg(x + 2, y - 7, COLOURS['white'], 'Down', 2)
                    self.widget.player.facing = DIRECTIONS['down']
                elif key == QtCore.Qt.Key_Right:
                    self.widget.add_egg(x + 7, y + 2, COLOURS['white'], 'Right', 2)
                    self.widget.player.facing = DIRECTIONS['right']
                elif key == QtCore.Qt.Key_Left:
                    self.widget.add_egg(x - 7, y + 2, COLOURS['white'], 'Left', 2)
                    self.widget.player.facing = DIRECTIONS['left']


                elif key == QtCore.Qt.Key_Space:
                    self.widget.add_egg(x, y, self.widget.player.color, 'N', 0)
                elif key == QtCore.Qt.Key_1:
                    self.widget.player.color = COLOURS['white']
                elif key == QtCore.Qt.Key_2:
                    self.widget.player.color = COLOURS['grey']
                elif key == QtCore.Qt.Key_3:
                    self.widget.player.color = COLOURS['other-grey']
                elif key == QtCore.Qt.Key_4:
                    self.widget.player.color = COLOURS['black']

            if player_movement > -50:
                self.widget.world.move_player(player_movement + 50)



 
    # create the QT App and window
    app = QtGui.QApplication(sys.argv)
    window = TestWindow()
    window.show()
    app.exec_()
