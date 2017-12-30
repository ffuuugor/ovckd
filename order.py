from time import time
from food import *
from commons import *

class Order(object):

    def __init__(self, ttl, recipe):
        self.expiration = time() + ttl
        self.recipe = recipe

    def check(self, input):
        all_cooked = all([x.progress == 1 for x in input])
        ingridients_match = sorted(self.recipe) == sorted([x.name for x in input])

        return all_cooked and ingridients_match

    def time_left(self):
        if time() > self.expiration:
            return 0
        else:
            return time() - self.expiration

    @staticmethod
    def next():
        return Order(ORDER_TIMEOUT, [FoodType.slicedOnion.name]*3)

    def to_json(self):
        pass