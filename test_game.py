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
            'white' : (1, 1, 1)}

class Player(object):
    def __init__(self, x, y, health=3):
        self.x = x
        self.y = y
        self.health = health
        self.is_exploded = False
        self.color = COLOURS['grey']


class GLPlotWidget(QGLWidget):
    # default window size
    width, height = 96, 64
    bunny_point = [30, 50]
    player = Player(20, 20)
    eggs = {v : [] for v in COLOURS.values()}
 
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

    def add_egg(self, x, y, color=COLOURS['white']):
        self.eggs[color].append((x, y))

    def draw_eggs(self):        
        for color, items in self.eggs.iteritems():
            r, g, b = color
            gl.glColor3f(r, g, b)
            for item in items:
                x = item[0]
                y = item[1]
                self.draw_square(x, y, 1)

    def draw_player(self):

        if self.player.is_exploded:
            r, g, b = COLOURS['other-grey']
            gl.glColor3f(r, g, b)
            for x in xrange(self.player.x - 4, self.player.x + 5):
                for y in xrange(self.player.y - 4, self.player.y + 5):
                    if choice((True, False)):
                        self.draw_square(x, y)

        r, g, b = self.player.color
        gl.glColor3f(r, g, b)
        for x in xrange(self.player.x, self.player.x + 4):
            for y in xrange(self.player.y, self.player.y + 3):
                self.draw_square(x, y)

            self.draw_square(x, y + 4)

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

        #self.draw_bunny(bunny_point[0], 20, bunny_point[1], 15)
        self.draw_eggs()
        self.draw_player()

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
            self.keys = []

            self.widget.setGeometry(0, 0, self.widget.width, self.widget.height)
            self.setCentralWidget(self.widget)
            self.show()

            self.paint_timer = QtCore.QTimer()
            QtCore.QObject.connect(self.paint_timer, QtCore.SIGNAL("timeout()"), self.widget.updateGL)
            
            self.button_timer = QtCore.QTimer()
            QtCore.QObject.connect(self.button_timer, QtCore.SIGNAL("timeout()"), self.check)

            QtCore.QMetaObject.connectSlotsByName(self)
            self.paint_timer.start(2560)
            self.button_timer.start(60)

            self.resize(600, 400)

        def keyPressEvent(self, event):
            self.keys.append(event.key())

        def keyReleaseEvent(self, event):
            self.keys.remove(event.key())

        def check(self):

            for key in self.keys:
                if key == QtCore.Qt.Key_A:
                    self.widget.player.x -= 1
                if key == QtCore.Qt.Key_D:
                    self.widget.player.x += 1
                if key == QtCore.Qt.Key_W:
                    self.widget.player.y += 1
                if key == QtCore.Qt.Key_S:
                    self.widget.player.y -= 1
                if key == QtCore.Qt.Key_Space:
                    self.widget.add_egg(self.widget.player.x, self.widget.player.y, self.widget.player.color)
                if key == QtCore.Qt.Key_1:
                    self.widget.player.color = COLOURS['white']
                if key == QtCore.Qt.Key_2:
                    self.widget.player.color = COLOURS['grey']
                if key == QtCore.Qt.Key_3:
                    self.widget.player.color = COLOURS['other-grey']
                if key == QtCore.Qt.Key_4:
                    self.widget.player.color = COLOURS['black']

            if len(self.keys) > 0:
                self.widget.updateGL()

 
    # create the QT App and window
    app = QtGui.QApplication(sys.argv)
    window = TestWindow()
    window.show()
    app.exec_()