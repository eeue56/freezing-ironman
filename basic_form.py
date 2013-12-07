
class Characteristic(object):
    def __init__(self, value=0, min_value=0, max_value=100):
        self.value = 0
        self.min_value = min_value
        self.max_value = max_value

        self.set_value(value)

    def increase_by(self, amount):
        if amount + self.value > self.max_value:
            self.value = self.max_value
        elif amount + self.value < self.min_value:
            self.value = self.min_value
        else:
            self.value += amount

    def decrease_by(self, amount):
        self.increase_by(-amount)

    def set_value(self, value):
        self.value = value
        self.increase_by(0)

    def __add__(self, other):
        if isinstance(other, Characteristic):
            return self.value + other.value
        else:
            return self.value + other

    def __neg__(self, other):
        if isinstance(other, Characteristic):
            return self.value - other.value
        else:
            return self.value - other

    def __iadd__(self, other):
        if isinstance(other, Characteristic):
            self.increase_by(other.value)
        else:
            self.increase_by(other)

        return self




class Player(object):

    def __init__(self):
        """ Each characteristic should be from the range
            [0, 100] by default. I can increase or decrease
            this range in order to find the optimal spread of values.
            Limiting to this range prevents issues with floating point
            and allows for greater variation in the specs of each player.


            In order to have the greatest chance of finding some features
            that are easily changable, I have broken down a player into a 
            number of fields
        
            So far, I have:
                speed   
                    The speed of the player's movement. 
                    This affects walking and running only

                turning_speed
                    The speed of a player's turning

                reload_speed
                    The speed of a player's reloading
                    TODO: If broken down into weapons, this
                    should be moved out into the weapon rather 
                    than the player

                stance_speed
                    The speed at which a player changes stance
                    This includes moving from crawling, prone
                    and crouching

                limp_speed


                fire_speed
                    The speed at which shots are fired

                shot_size
                    The size of the bullet shots

                shot_range
                    The range of the bullets 

                damage
                    The amount of damage dealt by this player

                max_health
                    The max health of the player

                limp_health
                    The health at which the health has to drop to
                    before the player starts limping

                health_regen_rate
                    The rate at which health regenerates.
                    Note: This will probably be shut off.

                regen_start_rate
                    The rate at which health will start regenerating
                    after taking damage
                    
                size
                    The player size. Affects hitbox only.



        """

        self.speed = Characteristic(50)

def test_characteristic():
    def test_create():
        c = Characteristic()
        assert c.value == 0
    
        c = Characteristic(101)
        assert c.value == 100
    
        c = Characteristic(56)
        assert c.value == 56

        c = Characteristic(min_value=-1, max_value=1000)
        assert c.value == 0

        c = Characteristic(1001, max_value=1000)
        assert c.value == 1000

        c = Characteristic(min_value=5)
        assert c.value == 5

    def test_increase_by():
        c = Characteristic()

        c.increase_by(5)
        assert c.value == 5

        c.increase_by(500)
        assert c.value == 100

        c.increase_by(-99)
        assert c.value == 1

    def test_add():
        c = Characteristic(10)
        d = Characteristic(50)

        assert c + d == 60
        assert c + 50 == 60

    test_create()
    test_increase_by()
    test_add()

def test():
    test_characteristic()

if __name__ == '__main__':
    test()