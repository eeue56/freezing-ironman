from __future__ import division

from misc import *
from global_exceptions import *
from collections import defaultdict
from copy import deepcopy as copy


class World(object):

    def __init__(self, player, levels=None, height=100, width=100):
        self.player = player
        self.height = height
        self.width = width

        self._last_collide = None
        self._dead_ids = []
        self._removing = False

        self.objects = []
        self.object_array = [[None for x in xrange(width)] for y in xrange(height)]

        if levels is None:
            levels = defaultdict(lambda:[])
        self.levels = levels
        self.current_level = 0
        self.generate_level()

    def add_objects(self, objects):
        for object_ in objects:
            self.add_object(object_)

    def add_object(self, object_):
        for (x, y) in object_.populated_squares:
            try:
                self.object_array[y][x] = object_
            except IndexError:
                raise OutOfWorldException
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
        if distance <= 0 or direction == DIRECTIONS['still']:
            return

        x, y = MOVEMENTS[direction]
            
        for _ in xrange(distance):
            if self.is_object_going_to_collide(object_, x=x, y=y):
                raise CollisionException(self._last_collide)
            self._move_object(object_, x=x, y=y)

    def move(self, x, y, direction, distance=1):
        object_ = self.object_array[y][x]
        self._dirty_move(object_, direction, distance)       

    def move_object(self, object_, direction, distance=1):
        self._dirty_move(object_, direction, distance)

    def move_player(self, direction, distance=1):
        self.move_object(self.player, direction, distance)

    def next_free_space(self, x, y, directions=None):
        i = 0
        j = 0

        visited = []
        last_visited_count = 0

        while True:
            for n in range(x - i, x + i):
                if n < 0:
                    continue
                if n > self.width: 
                    break

                for m in range(y - j, y + j):
                    if m < 0:
                        continue
                    if m > self.height:
                        break

                    if (n, m) not in visited:
                        if self.object_array[m][n] is None:
                            return (n, m)
                        else:
                            visited.append((n, m))

            if last_visited_count == len(visited):
                break

            last_visited_count = len(visited)
            i += 1
            j += 1
        return (-1, -1)


    def find_path_to_point(self, object_, x, y):
        my_x, my_y = object_.x, object_.y

        direction = DIRECTIONS['still']

        if my_x < x:
            direction += DIRECTIONS['right']
        elif my_x > x:
            direction += DIRECTIONS['left']
    
        if my_y < y:
            direction += DIRECTIONS['up']
        elif my_y > y:
            direction += DIRECTIONS['down']

        return direction

    def find_path(self, object_, other_object):
        my_x, my_y = object_.x, object_.y
        (x, y) = other_object.closest_point(my_x, my_y)
        return self.find_path_to_point(object_, x, y)

    def remove_object(self, object_):
        self._removing = True
        for (x, y) in object_.populated_squares:
            self.object_array[y][x] = None

        try:
            self.objects.remove(object_)
        except ValueError:
            pass
        self._removing = False


    def move_level(self):
        if self.player.x > 50:
            self.move_player(DIRECTIONS['left'], distance=5)
        else:
            self.move_player(DIRECTIONS['right'], distance=5)
        self.current_level += 1
        self._last_collide = None

        self.objects = []
        self.object_array = [[None for x in xrange(self.width)] for y in xrange(self.height)]
        self.generate_level()

    def generate_level(self):
        level = self.levels[self.current_level]
        self.add_objects(level)

    def draw(self):
        for object_ in self.objects:
            object_.draw()

        self.player.draw()

    def tick(self):
        for object_ in self.objects:
            object_.tick(self)

        try:
            self.player.tick(self)
        except OutOfWorldException:
            self.move_level()
