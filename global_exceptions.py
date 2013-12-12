class CollisionException(Exception):
    def __init__(self, other, *args):
        Exception.__init__(self, *args)
        self.other = other

class OutOfWorldException(Exception):
    pass

class MovementException(Exception):
    def __init__(self, direction, distance, *args):
        Exception.__init__(self, *args)
        self.direction = direction
        self.distance = distance
