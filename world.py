from __future__ import division

from misc import *

class World(object):

    def __init__(self, player, height=96, width=96):
        self.player = player
        self.objects = []

        self.object_array = [[None for x in xrange(width)] for y in xrange(height)]

    def add_objects(self, objects):
        self.objects.extend(objects)

        for object_ in objects:
            self.object_array[object_.y][object_.x] = object_

    def is_object_there(self, x, y):
        return self.object_array[y][x] is not None

    def is_going_to_collide(self, old_x, old_y, new_x, new_y, object_):
        if old_x > new_x:
            old_x, new_x = new_x, old_x

        if old_y > new_y:
            old_y, new_y = new_y, old_y

        for x in xrange(old_x + 1, new_x + 1):
            for y in xrange(old_y + 1, new_y + 1):
                if x == object_.x and y == object_.y:
                    continue

                if self.object_array[y][x] is not None:
                    return True
        return False

    def is_object_going_to_collide(self, object_, x=0, y=0):
        return self.is_going_to_collide(object_.x, object_.y, 
            object_.x + x, object_.y + y,
            object_)

    def _move(self, x, y, new_x, new_y):
        self.object_array[new_y][new_x] = self.object_array[y][x]
        self.object_array[y][x].x = new_x
        self.object_array[y][x].y = new_y
        self.object_array[y][x] = None

    def _move_object(self, object_, x=0, y=0):
        self._move(object_.x, object_.y, object_.x + x, object_.y + y)

    def move(self, x, y, direction, distance=1):
        object_ = self.object_array[y][x]

        if direction == DIRECTIONS['up']:
            for _ in [1 for _ in xrange(distance)]:
                if self.is_object_going_to_collide(object_, y=1):
                    self._move_object(object_, y=1)

        elif direction == DIRECTIONS['down']:
            for _ in [1 for _ in xrange(distance)]:
                if self.is_object_going_to_collide(object_, y=-1):
                    self._move_object(object_, y=-1)

        elif direction == DIRECTIONS['left']:
            for _ in [1 for _ in xrange(distance)]:
                if self.is_object_going_to_collide(object_, x=-1):
                    self._move_object(object_, x=-1)

        elif direction == DIRECTIONS['right']:
            for _ in [1 for _ in xrange(distance)]:
                if self.is_object_going_to_collide(object_, x=1):
                    self._move_object(object_, x=1)


        elif direction == DIRECTIONS['up'] + DIRECTIONS['left']:
            for _ in [1 for _ in xrange(distance)]:
                if self.is_object_going_to_collide(object_, x=1, y=-1):
                    self._move_object(object_, x=1, y=-1)

        elif direction == DIRECTIONS['up'] + DIRECTIONS['right']:
            for _ in [1 for _ in xrange(distance)]:
                if self.is_object_going_to_collide(object_, x=1, y=1):
                    self._move_object(object_, x=1, y=1)

        elif direction == DIRECTIONS['down'] + DIRECTIONS['left']:
            for _ in [1 for _ in xrange(distance)]:
                if self.is_object_going_to_collide(object_, x=-1, y=-1):
                    self._move_object(object_, x=-1, y=-1)

        elif direction == DIRECTIONS['down'] + DIRECTIONS['right']:
            for _ in [1 for _ in xrange(distance)]:
                if self.is_object_going_to_collide(object_, x=-1, y=1):
                    self._move_object(object_, x=-1, y=1)

    def move_object(self, object_, direction, distance=1):
        self.move(object_.x, object_.y, direction, distance)

    def move_player(self, direction, distance=1):
        self.move_object(self.player, direction, distance)
