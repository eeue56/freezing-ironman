from __future__ import division

import OpenGL.GL as gl

from misc import *
from global_exceptions import *

class WorldObject(object):
    def __init__(self, x, y, color, take_damage=False):
        self.x = x
        self.y = y
        self.color = color
        self.can_take_damage = take_damage

    def draw(self):
        pass

    def take_damage(self, damage, world):
        pass

    def tick(self, world):
        pass


class Player(WorldObject):
    def __init__(self, x, y, health=3, color=COLOURS['grey']):
        WorldObject.__init__(self, x, y, color, take_damage=True)
        self.health = health
        self.facing = DIRECTIONS['up']
        self.movement_facing = DIRECTIONS['up']
        self.speed = 0
        self.width = 2
        self.height = 3

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

    def draw(self):
        gl.glPushMatrix()

        r, g, b = self.color
        gl.glColor3f(r, g, b)

        if self.facing in (DIRECTIONS['down'], DIRECTIONS['up']):
            for x in xrange(self.x, self.x + 5):
                for y in xrange(self.y, self.y + 2):
                    draw_square(x, y)
            if self.facing == DIRECTIONS['up']:
                draw_square(x - 3, y + 1)
                draw_square(x - 2, y + 1)
                draw_square(x - 2, y + 2)
                draw_square(x - 1, y + 1)
            else:
                y = self.y
                draw_square(x - 3, y - 1)
                draw_square(x - 2, y - 1)
                draw_square(x - 2, y - 2)
                draw_square(x - 1, y - 1)
        else:
            for x in xrange(self.x, self.x + 2):
                for y in xrange(self.y, self.y + 5):
                    draw_square(x, y)
            if self.facing == DIRECTIONS['right']:
                draw_square(x + 1, y - 1)
                draw_square(x + 1, y - 2)
                draw_square(x + 1, y - 3)
                draw_square(x + 2, y - 2)
            else:
                x = self.x
                draw_square(x - 1, y - 1)
                draw_square(x - 1, y - 2)
                draw_square(x - 1, y - 3)
                draw_square(x - 2, y - 2)
       

        gl.glPopMatrix() 

    def tick(self, world):
        try:
            world.move_object(self, self.movement_facing, self.speed)
        except CollisionException as e:
            if e.other.can_take_damage:
                e.other.take_damage(1, world)
                self.take_damage(0.1, world)
        except:
            raise

    def take_damage(self, damage, world):
        self.health -= damage

        if self.health <= 0:
            world.remove_object(self)


class Monster(WorldObject):
    def __init__(self, x, y, health=3, color=COLOURS['grey']):
        WorldObject.__init__(self, x, y, color, take_damage=True)
        self.health = health
        self.facing = DIRECTIONS['up']

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

    def draw(self):
        gl.glPushMatrix()

        r, g, b = self.color
        gl.glColor3f(r, g, b)

        if self.facing in (DIRECTIONS['down'], DIRECTIONS['up']):
            for x in xrange(self.x, self.x + 5):
                for y in xrange(self.y, self.y + 2):
                    draw_square(x, y)
            if self.facing == DIRECTIONS['up']:
                draw_square(x - 3, y + 1)
                draw_square(x - 2, y + 1)
                draw_square(x - 2, y + 2)
                draw_square(x - 1, y + 1)
            else:
                y = self.y
                draw_square(x - 3, y - 1)
                draw_square(x - 2, y - 1)
                draw_square(x - 2, y - 2)
                draw_square(x - 1, y - 1)
        else:
            for x in xrange(self.x, self.x + 2):
                for y in xrange(self.y, self.y + 5):
                    draw_square(x, y)
            if self.facing == DIRECTIONS['right']:
                draw_square(x + 1, y - 1)
                draw_square(x + 1, y - 2)
                draw_square(x + 1, y - 3)
                draw_square(x + 2, y - 2)
            else:
                x = self.x
                draw_square(x - 1, y - 1)
                draw_square(x - 1, y - 2)
                draw_square(x - 1, y - 3)
                draw_square(x - 2, y - 2)
       

        gl.glPopMatrix() 

    def tick(self, world):
        try:
            world.move_object(self, self.facing, self.speed)
        except CollisionException as e:
            if e.other.can_take_damage:
                e.other.take_damage(1, world)
                self.take_damage(0.1, world)
        except:
            raise

    def take_damage(self, damage, world):
        return
        self.health -= damage

        if self.health <= 0:
            world.remove_object(self)


class Egg(WorldObject):
    def __init__(self, x, y, color, facing=DIRECTIONS['up'], speed=1):
        WorldObject.__init__(self, x, y, color, take_damage=False)
        self.facing = facing
        self.speed = speed

    def draw(self):
        gl.glColor3f(self.color.r, self.color.g, self.color.b)

        draw_square(self.x, self.y)

    def tick(self, world):
        try:
            world.move_object(self, self.facing, self.speed)
        except CollisionException as e:
            if e.other.can_take_damage:
                e.other.take_damage(1, world)
            else:
                world.remove_object(self)
        except OutOfWorldException:
            world.remove_object(self)
        except:
            raise

    def take_damage(self, damage, world):
        world.remove_object(self)
        
