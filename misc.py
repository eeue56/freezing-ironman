from __future__ import division

import OpenGL.GL as gl

from random import choice, randint

COLOURS = { 'black' : (0, 0, 0),
            'other-grey' : (0.25, 0.25, 0.25),
            'grey' : (0.4, 0.4, 0.4),
            'red' :  (255, 0, 0),
            'white' : (1, 1, 1)}

DIRECTIONS = {
        'up' : 1,
        'down' : 2,
        'left' : 30,
        'right' : 40
}


def random_color():
    return tuple(y / 255 for y in (randint(0, 255), randint(0, 255), randint(0, 255)))

def draw_square(x, y, size=1):
    gl.glRectf(x, y, x + size, y + size)
