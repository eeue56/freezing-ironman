from __future__ import division

# PyQT4 imports
from PyQt4 import QtGui, QtCore, QtOpenGL
from PyQt4.QtOpenGL import QGLWidget
# PyOpenGL imports
import OpenGL.GL as gl
import OpenGL.arrays.vbo as glvbo
from random import choice

COLOURS = { 'black' : (0, 0, 0),
            'other-grey' : (0.25, 0.25, 0.25),
            'grey' : (0.4, 0.4, 0.4),
            'red' : (255, 0, 0),
            'white' : (1, 1, 1)}

DIRECTIONS = {
        'up' : 1,
        'down' : 2,
        'left' : 3,
        'right' : 4
}

class Player(object):
    def __init__(self, x, y, health=3):
        self.x = x
        self.y = y
        self.health = health
        self.facing = DIRECTIONS['up']
        self.color = COLOURS['grey']


class GLPlotWidget(QGLWidget):
    # default window size
    width, height = 96, 64
    bunny_point = [30, 50]
    player = Player(20, 20)
    eggs = {v : [] for v in COLOURS.values()}
    monsters = [Player(50, 40)]
 
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
        self.eggs[color].append([x, y, direction, speed])

    def draw_eggs(self):        

        for color, items in self.eggs.iteritems():
            r, g, b = color
            gl.glColor3f(r, g, b)
            for item in items[:]:
                x = item[0]
                y = item[1]

                if x < 0 or x > 96 or y < 0 or y > 64:
                    items.remove(item)
                    continue

                goto_break = False

                for monster in self.monsters:
                    if monster.x < x < monster.x + 5 and monster.y < y < monster.y + 5:
                        items.remove(item)
                        monster.health -= 1
                        monster.color = COLOURS['red']
                        goto_break = True
                        break

                if goto_break:
                    continue

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
        gl.glOrtho(0, 96, 0, 64, -1, 1)
 
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

            QtCore.QMetaObject.connectSlotsByName(self)
            self.paint_timer.start(40)
            self.button_timer.start(35)

            self.resize(600, 400)

        def keyPressEvent(self, event):
            self.keys.add(event.key())

        def keyReleaseEvent(self, event):
            try:
                self.keys.remove(event.key())
            except:
                print event.key()
                print self.keys

        def check(self):

            x = self.widget.player.x
            y = self.widget.player.y

            for key in self.keys:  

                if key == QtCore.Qt.Key_A:
                    self.widget.player.x -= 1
                if key == QtCore.Qt.Key_D:
                    self.widget.player.x += 1
                if key == QtCore.Qt.Key_W:
                    self.widget.player.y += 1
                if key == QtCore.Qt.Key_S:
                    self.widget.player.y -= 1

                if key == QtCore.Qt.Key_Up:
                    self.widget.add_egg(x + 2, y + 10, COLOURS['white'], 'Up', 2)
                    self.widget.player.facing = DIRECTIONS['up']
                if key == QtCore.Qt.Key_Down:
                    self.widget.add_egg(x + 2, y - 10, COLOURS['white'], 'Down', 2)
                    self.widget.player.facing = DIRECTIONS['down']
                if key == QtCore.Qt.Key_Right:
                    self.widget.add_egg(x + 10, y + 2, COLOURS['white'], 'Right', 2)
                    self.widget.player.facing = DIRECTIONS['right']
                if key == QtCore.Qt.Key_Left:
                    self.widget.add_egg(x - 10, y + 2, COLOURS['white'], 'Left', 2)
                    self.widget.player.facing = DIRECTIONS['left']


                if key == QtCore.Qt.Key_Space:
                    self.widget.add_egg(x, y, self.widget.player.color, 'N', 0)
                if key == QtCore.Qt.Key_1:
                    self.widget.player.color = COLOURS['white']
                if key == QtCore.Qt.Key_2:
                    self.widget.player.color = COLOURS['grey']
                if key == QtCore.Qt.Key_3:
                    self.widget.player.color = COLOURS['other-grey']
                if key == QtCore.Qt.Key_4:
                    self.widget.player.color = COLOURS['black']


 
    # create the QT App and window
    app = QtGui.QApplication(sys.argv)
    window = TestWindow()
    window.show()
    app.exec_()