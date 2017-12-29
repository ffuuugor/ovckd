from enum import Enum
import json

PREPARE_TIME = 10
ORDER_TIMEOUT = 60
ORDER_CREATION_INTERVAL = 30
NUM_PLAYERS = 2

class TileType(Enum):
    empty = 0
    wall = 1
    table = 2
    exit = 3
    knife = 4
    cooking_panel = 5
    onion_box = 6
    mushroom_box = 7
    tomato_box = 8


class Direction(Enum):
    up = 0
    left = 1
    down = 2
    right = 3


class Position(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(self.x)*17 + hash(self.y)

    def to_json(self):
        return json.dumps({
            "x": self.x,
            "y": self.y
        })

def mean(arr):
    return float(sum(arr))/len(arr)



