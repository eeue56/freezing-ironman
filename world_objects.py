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
        self._square_cache = {}

    def draw(self):
        gl.glPushMatrix()

        r, g, b = self.color
        gl.glColor3f(r, g, b)

        for square in self.populated_squares:
            x, y = square
            draw_square(x, y)

        gl.glPopMatrix() 

    def take_damage(self, damage, world):
        pass

    def tick(self, world):
        pass

    def populated_at(self, x, y):
        return [(x, y)]
        
    @property
    def populated_squares(self):
        if (self.x, self.y) not in self._square_cache:
            self._square_cache[(self.x, self.y)] = self.populated_at(self.x, self.y)
        return self._square_cache[(self.x, self.y)]


class Player(WorldObject):
    def __init__(self, x, y, health=3, color=COLOURS['grey']):
        WorldObject.__init__(self, x, y, color, take_damage=True)
        self.health = health
        self.facing = DIRECTIONS['up']
        self.movement_facing = DIRECTIONS['up']
        self.speed = 0
        self.width = 5
        self.height = 2

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

    def tick(self, world):
        try:
            world.move_object(self, self.movement_facing, self.speed)
        except CollisionException as e:
            if e.other.can_take_damage:
                e.other.take_damage(1, world)
                self.take_damage(0.1, world)
        except OutOfWorldException:
            pass
        except:
            raise

    def take_damage(self, damage, world):
        self.health -= damage

        if self.health <= 0:
            world.remove_object(self)

    def populated_at(self, xs, ys):
        populated = []
        populate = lambda x, y: populated.append((x, y))

        if self.facing in (DIRECTIONS['down'], DIRECTIONS['up']):
            for x in xrange(xs, xs + self.width):
                for y in xrange(ys, ys + self.height):
                    populate(x, y)
            if self.facing == DIRECTIONS['up']:
                populate(x - 3, y + 1)
                populate(x - 2, y + 1)
                populate(x - 2, y + 2)
                populate(x - 1, y + 1)
            else:
                y = ys
                populate(x - 3, y - 1)
                populate(x - 2, y - 1)
                populate(x - 2, y - 2)
                populate(x - 1, y - 1)
        else:
            for x in xrange(xs, xs + self.height):
                for y in xrange(ys, ys + self.width):
                    populate(x, y)
            if self.facing == DIRECTIONS['right']:
                populate(x + 1, y - 1)
                populate(x + 1, y - 2)
                populate(x + 1, y - 3)
                populate(x + 2, y - 2)
            else:
                x = xs
                populate(x - 1, y - 1)
                populate(x - 1, y - 2)
                populate(x - 1, y - 3)
                populate(x - 2, y - 2)
        return populated


class Monster(WorldObject):
    def __init__(self, x, y, speed=1, health=3, color=COLOURS['grey']):
        WorldObject.__init__(self, x, y, color, take_damage=True)
        self.health = health
        self.speed = 0
        self.facing = DIRECTIONS['up']
        self.width = 5
        self.height = 2

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
        self.health -= damage

        if self.health <= 0:
            world.remove_object(self)

    def populated_at(self, xs, ys):
        populated = []
        populate = lambda x, y: populated.append((x, y))

        if self.facing in (DIRECTIONS['down'], DIRECTIONS['up']):
            for x in xrange(xs, xs + self.width):
                for y in xrange(ys, ys + self.height):
                    populate(x, y)
            if self.facing == DIRECTIONS['up']:
                populate(x - 3, y + 1)
                populate(x - 2, y + 1)
                populate(x - 2, y + 2)
                populate(x - 1, y + 1)
            else:
                y = ys
                populate(x - 3, y - 1)
                populate(x - 2, y - 1)
                populate(x - 2, y - 2)
                populate(x - 1, y - 1)
        else:
            for x in xrange(xs, xs + self.height):
                for y in xrange(ys, ys + self.width):
                    populate(x, y)
            if self.facing == DIRECTIONS['right']:
                populate(x + 1, y - 1)
                populate(x + 1, y - 2)
                populate(x + 1, y - 3)
                populate(x + 2, y - 2)
            else:
                x = xs
                populate(x - 1, y - 1)
                populate(x - 1, y - 2)
                populate(x - 1, y - 3)
                populate(x - 2, y - 2)
        return populated


class Egg(WorldObject):
    def __init__(self, x, y, color, facing=DIRECTIONS['up'], speed=1):
        WorldObject.__init__(self, x, y, color, take_damage=False)
        self.facing = facing
        self.speed = speed
        self.width = 1
        self.height = 1
        self.health = 1

    def tick(self, world):
        try:
            world.move_object(self, self.facing, self.speed)
        except CollisionException as e:
            print 'collided'
            if e.other.can_take_damage:
                e.other.take_damage(1, world)
            world.remove_object(self)
            self.health = 0
        except OutOfWorldException:
            world.remove_object(self)
            self.health = 0
        except:
            raise

    def take_damage(self, damage, world):
        world.remove_object(self)

    def populated_at(self, x, y):
        return [(x, y)]

        
    @property
    def populated_squares(self):
        return self.populated_at(self.x, self.y)
