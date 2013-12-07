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


keeper = [[choice(colours) for _ in xrange(100)] for _ in xrange(100)]
 
b = {colour: [] for colour in colours}

for x in xrange(100):
    for y in xrange(100):
        c = choice(colours)
        b[c].append((x, y))

class GLPlotWidget(QGLWidget):
    # default window size

    def __init__(self, width, height, player, *args):
        QGLWidget.__init__(self, *args)
        self.width = width
        self.height = height
        self.player = player
        self.melted = []

    def draw_square(self, x, y, size=1):
        gl.glRectf(x, y, x + size, y + size)

    def melt(self):
        self.melted.append((self.player.x, self.player.y))

    def draw_ice(self, x, y):
        gl.glBegin(gl.GL_TRIANGLE_STRIP)
        width = 1
        height = 1

        gl.glColor3f(0, 0, 0.5)
        gl.glVertex3f(x, y, 0)
        gl.glVertex3f(x + width, y, 0)
        gl.glVertex3f(x, y + height, 0)
        
        gl.glVertex3f(x + width, y + height, 0)
        gl.glVertex3f(x, y + height, 0)
        gl.glColor3f(0, 0.2, 0.7)
        gl.glVertex3f(x + width, y, 0)


        gl.glEnd()

    def draw_player(self):
        gl.glBegin(gl.GL_TRIANGLES)

        x = self.player.x
        y = self.player.y
        
        width = 3
        height = 3

        gl.glColor3f(1, 0, 0)
        gl.glVertex3f(x, y, 0)

        gl.glColor3f(0.6, 0.2, 0)
        gl.glVertex3f(x + (width / 2), y + height, 0)

        gl.glColor3f(0.8, 0.1, 0.2)
        gl.glVertex3f(x + width, y, 0)

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
        
        """
        for color in b:
            gl.glPushMatrix()
            gl.glColor3f(*color)
            for (i, j) in b[color]:
                self.draw_square(i, j)
            gl.glPopMatrix()
        """

        gl.glColor3f(0.5, 0.2, 0.3)
        for (i, j) in self.melted:
            self.draw_square(i, j)
            

        for i in xrange(20):
            for j in xrange(20):
                if (i, j) not in self.melted:
                    self.draw_ice(i, j)

        gl.glPushMatrix()
        self.draw_player()
        gl.glPopMatrix()

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
        # the window corner OpenGL coordinates are (-+1, -+1)
        gl.glOrtho(0, 20, 0, 20, -1, 1)



class Player(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y 
        self.z = z

if __name__ == '__main__':
    # import numpy for generating random data points
    import sys


 
    # define a QT window with an OpenGL widget inside it
    class TestWindow(QtGui.QMainWindow):
        def __init__(self):
            super(TestWindow, self).__init__()
            # initialize the GL widget
            self.player = Player(0, 0, 0)
            self.keys = set()

            self.widget = GLPlotWidget(600, 400, self.player)

            self.widget.setGeometry(0, 0, self.widget.width, self.widget.height)
            self.setCentralWidget(self.widget)
            self.show()


            self.paint_timer = QtCore.QTimer()
            QtCore.QObject.connect(self.paint_timer, QtCore.SIGNAL("timeout()"), self.widget.updateGL)

            self.checker = QtCore.QTimer()
            QtCore.QObject.connect(self.checker, QtCore.SIGNAL("timeout()"), self.check)


            QtCore.QMetaObject.connectSlotsByName(self)
            
            self.paint_timer.start(50)
            self.checker.start(25)
            self.resize(600, 400)

        def keyPressEvent(self, event):
            self.keys.add(event.key())

        def keyReleaseEvent(self, event):
            try:
                self.keys.remove(event.key())
            except:
                pass

        def check(self):

            for key in self.keys:  

                if key == QtCore.Qt.Key_A:
                    self.widget.player.x -= 1
                elif key == QtCore.Qt.Key_D:
                    self.widget.player.x += 1
                elif key == QtCore.Qt.Key_W:
                    self.widget.player.y += 1
                elif key == QtCore.Qt.Key_S:
                    self.widget.player.y -= 1

            self.widget.melt()

             
    # create the QT App and window
    app = QtGui.QApplication(sys.argv)
    window = TestWindow()
    window.show()
    app.exec_()