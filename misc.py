from __future__ import division

import OpenGL.GL as gl

from random import choice, randint
from collections import OrderedDict

COLOURS = { 'black' : (0, 0, 0),
            'other-grey' : (0.25, 0.25, 0.25),
            'grey' : (0.4, 0.4, 0.4),
            'red' :  (255, 0, 0),
            'white' : (1, 1, 1)}

DIRECTIONS = {
        'still' : 0,
        'up' : 1,
        'down' : -1,
        'right' : 20,
        'left' : -20
}


def random_color():
    return tuple(y / 255 for y in (randint(0, 255), randint(0, 255), randint(0, 255)))

def draw_square(x, y, x_size=1, y_size=1):
    gl.glRectf(x, y, x + x_size, y + y_size)

def into_sections(blocklist):

    into_dict = OrderedDict()

    for block in blocklist:
        x, y = block
        if y not in into_dict:
            into_dict[y] = OrderedDict()
        into_dict[y][x] = True

    sections = []

    for y in into_dict:
        last_x = -1
        current_section = 1
        start_x = None

        for x in into_dict[y]:
            if x == last_x + 1:
                if start_x is None:
                    start_x = x
                else:
                    current_section += 1
            else:
                if start_x is None:
                    start_x = x

                width = current_section
                
                if width <= 1:
                    sections.append((start_x, y, 1, 1))
                else:
                    sections.append((start_x, y, width, 1))
                
                start_x = None
                current_section = 1
            last_x = x
        else:
            if start_x is None:
                start_x = x
            width = current_section

            sections.append((start_x, y, width, 1))

    return sections