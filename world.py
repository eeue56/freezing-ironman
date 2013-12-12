from __future__ import division

from misc import *
from global_exceptions import *

class World(object):

    def __init__(self, player, height=100, width=100):
        self.player = player
        self.objects = []
        self.height = height
        self.width = width

        self._last_collide = None

        self.object_array = [[None for x in xrange(width)] for y in xrange(height)]

    def add_objects(self, objects):
        self.objects.extend(objects)

        for object_ in objects:
            for (x, y) in object_.populated_squares:
                self.object_array[y][x] = object_

    def add_object(self, object_):
        self.objects.append(object_)
        for (x, y) in object_.populated_squares:
            self.object_array[y][x] = object_

    def is_object_there(self, x, y):
        return self.object_array[y][x] is not None

    def is_going_to_collide(self, new_object):
        
        for (x, y) in new_object.populated_squares:
            if y < 0 or y >= self.height or x < 0 or x >= self.width:
                raise OutOfWorldException

            if self.object_array[y][x] is not None:
                self._last_collide = self.object_array[y][x]
                return True
        return False

    def is_object_going_to_collide(self, object_, x=0, y=0):
        new_object = copy(object_)
        new_object.x += x
        new_object.y += y

        return self.is_going_to_collide(new_object)

    def _move(self, old, new, object_):

        for (x, y) in old:
            self.object_array[y][x] = None
        for (new_y, new_x) in new:
            self.object_array[new_y][new_x] = object_

    def _move_object(self, object_, x=0, y=0):
        old_populated = object_.populated_squares
        object_.x += x
        object_.y += y
        self._move(old_populated, object_.populated_squares, object_)

    def _dirty_move(self, object_, direction, distance):
        if direction == DIRECTIONS['up']:
            for _ in [1 for _ in xrange(distance)]:
                if self.is_object_going_to_collide(object_, y=1):
                    raise CollisionException(self._last_collide)
                self._move_object(object_, y=1)

        elif direction == DIRECTIONS['down']:
            for _ in [1 for _ in xrange(distance)]:
                if self.is_object_going_to_collide(object_, y=-1):
                    raise CollisionException(self._last_collide)
                self._move_object(object_, y=-1)

        elif direction == DIRECTIONS['left']:
            for _ in [1 for _ in xrange(distance)]:
                if self.is_object_going_to_collide(object_, x=-1):
                    raise CollisionException(self._last_collide)
                self._move_object(object_, x=-1)

        elif direction == DIRECTIONS['right']:
            for _ in [1 for _ in xrange(distance)]:
                if self.is_object_going_to_collide(object_, x=1):
                    raise CollisionException(self._last_collide)
                self._move_object(object_, x=1)

        elif direction == DIRECTIONS['down'] + DIRECTIONS['right']:
            for _ in [1 for _ in xrange(distance)]:
                if self.is_object_going_to_collide(object_, x=1, y=-1):
                    raise CollisionException(self._last_collide)
                self._move_object(object_, x=1, y=-1)

        elif direction == DIRECTIONS['up'] + DIRECTIONS['right']:
            for _ in [1 for _ in xrange(distance)]:
                if self.is_object_going_to_collide(object_, x=1, y=1):
                    raise CollisionException(self._last_collide)
                self._move_object(object_, x=1, y=1)

        elif direction == DIRECTIONS['down'] + DIRECTIONS['left']:
            for _ in [1 for _ in xrange(distance)]:
                if self.is_object_going_to_collide(object_, x=-1, y=-1):
                    raise CollisionException(self._last_collide)
                self._move_object(object_, x=-1, y=-1)

        elif direction == DIRECTIONS['up'] + DIRECTIONS['left']:
            for _ in [1 for _ in xrange(distance)]:
                if self.is_object_going_to_collide(object_, x=-1, y=1):
                    raise CollisionException(self._last_collide)
                self._move_object(object_, x=-1, y=1)

    def move(self, x, y, direction, distance=1):
        object_ = self.object_array[y][x]
        self._dirty_move(object_, direction, distance)       

    def move_object(self, object_, direction, distance=1):
        if distance > 0:
            self._dirty_move(object_, direction, distance)

    def move_player(self, direction, distance=1):
        if distance > 0:
            self.move_object(self.player, direction, distance)

    def remove_object(self, object_):
        try:
            self.objects.remove(object_)
            self.object_array[object_.y][object_.x] = None
        except IndexError:
            pass

    def draw(self):
        for object_ in self.objects:
            object_.draw()
        self.player.draw()

    def tick(self):
        for object_ in self.objects:
            object_.tick(self)
        self.player.tick(self)
