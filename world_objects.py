from __future__ import division

import OpenGL.GL as gl

from misc import *
from global_exceptions import *

class WorldObject(object):
    def __init__(self, x, y, color, facing=DIRECTIONS['up'], take_damage=False, moveable=True):
        self.x = x
        self.y = y
        self.color = color
        self.can_take_damage = take_damage
        self.moveable = moveable
        self._square_cache = {}
        self._section_cache = {}

    def draw(self):

        if (self.x, self.y, self.facing) not in self._section_cache:
            self._section_cache[(self.x, self.y, self.facing)] = into_sections(self.populated_squares)

        gl.glPushMatrix()

        r, g, b = self.color
        gl.glColor3f(r, g, b)

        for section in self._section_cache[(self.x, self.y, self.facing)]:
            (x, y, width, height) = section
            draw_square(x, y, width, height)
        gl.glPopMatrix() 

    def take_damage(self, damage, world):
        pass

    def tick(self, world):
        pass

    def populated_at(self, x, y):
        return [(x, y)]

    def closest_point(self, x, y):
        x2nd = x ** 2
        y2nd = y ** 2
        euclid = lambda i, j: (x2nd - (i ** 2)) + (y2nd - (j ** 2))

        small_score = 9000001
        smallest = None

        for (x, y) in self.populated_squares:
            score = euclid(x, y)
            if score < small_score:
                smallest = (x, y)
                small_score = score
        return smallest
        
    @property
    def populated_squares(self):
        if (self.x, self.y, self.facing) not in self._square_cache:
            self._square_cache[(self.x, self.y, self.facing)] = self.populated_at(self.x, self.y)
        return self._square_cache[(self.x, self.y, self.facing)]


class Player(WorldObject):
    def __init__(self, x, y, speed=1, health=3, color=COLOURS['grey']):
        WorldObject.__init__(self, x, y, color, take_damage=True)
        self.health = health
        self.facing = DIRECTIONS['up']
        self.movement_facing = DIRECTIONS['still']
        self.speed = speed
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
                e.other.take_damage(0.5, world)
                self.take_damage(0.1, world)
        except OutOfWorldException:
            raise
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
        self.speed = speed
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
        new_face = world.find_path(self, world.player)
        self.facing = new_face
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

class Wall(WorldObject):
    def __init__(self, x, y, width=5, gaps=None, color=COLOURS['grey'], facing=DIRECTIONS['up'], speed=1):
        WorldObject.__init__(self, x, y, color, take_damage=False, moveable=False)

        if gaps is None:
            gaps = []

        self.gaps = gaps
        self.facing = facing
        self.speed = speed
        self.width = width
        self.height = 2
        self.health = 1

    def tick(self, world):
        pass

    def take_damage(self, damage, world):
        pass

    def populated_at(self, *args):
        populated = []
        populate = lambda x, y: populated.append((x, y))
        x, y = self.x, self.y

        if self.facing == DIRECTIONS['down']:
            for i in xrange(x):
                if i not in self.gaps:
                    for w in xrange(self.width):
                        populate(i, w)
        elif self.facing == DIRECTIONS['up']:
            for i in xrange(x):
                if i not in self.gaps:
                    for w in xrange(y - self.width, y):
                        populate(i, w)
        elif self.facing == DIRECTIONS['left']:
            for j in xrange(y):
                if j not in self.gaps:
                    for w in xrange(self.width):
                        populate(w, j)
        elif self.facing == DIRECTIONS['right']:
            for j in xrange(y):
                if j not in self.gaps:
                    for w in xrange(x - self.width, x):
                        populate(w, j)
                
        return populated