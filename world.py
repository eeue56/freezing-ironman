from __future__ import division

from misc import *
from global_exceptions import *
from copy import deepcopy as copy


class World(object):

    def __init__(self, player, height=100, width=100):
        self.player = player
        self.height = height
        self.width = width

        self._last_collide = None
        self._dead_ids = []
        self._removing = False

        self.objects = []
        self.object_array = [[None for x in xrange(width)] for y in xrange(height)]

    def add_objects(self, objects):
        for object_ in objects:
            for (x, y) in object_.populated_squares:
                self.object_array[y][x] = object_
            self.objects.append(object_)

    def add_object(self, object_):
        for (x, y) in object_.populated_squares:
            self.object_array[y][x] = object_
        self.objects.append(object_)

    def is_object_there(self, x, y):
        return self.object_array[y][x] is not None

    def is_going_to_collide(self, old_object, populated_next):
        for (x, y) in populated_next:
            if y < 0 or y >= self.height or x < 0 or x >= self.width:
                raise OutOfWorldException

            if self.object_array[y][x] is not None and self.object_array[y][x] != old_object:
                self._last_collide = self.object_array[y][x]
                return True
        return False

    def is_object_going_to_collide(self, object_, x=0, y=0):
        projected_points = object_.populated_at(object_.x + x, object_.y + y)

        return self.is_going_to_collide(object_, projected_points)

    def _move(self, old, new, object_):

        for (x, y) in old:
            self.object_array[y][x] = None
        for (new_x, new_y) in new:
            self.object_array[new_y][new_x] = object_

    def _move_object(self, object_, x=0, y=0):
        self._move(object_.populated_squares, 
            object_.populated_at(object_.x + x, object_.y + y), 
            object_)
        object_.x += x
        object_.y += y

    def _dirty_move(self, object_, direction, distance):
        if distance <= 0:
            return

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
        self._dirty_move(object_, direction, distance)

    def move_player(self, direction, distance=1):
        self.move_object(self.player, direction, distance)

    def remove_object(self, object_):
        self._removing = True
        for (x, y) in object_.populated_squares:
            self.object_array[y][x] = None
        self.objects.remove(object_)

        self._removing = False

    def draw(self):
        for object_ in self.objects:
            object_.draw()

        self.player.draw()

    def tick(self):
        for object_ in self.objects:
            object_.tick(self)

        self.player.tick(self)
