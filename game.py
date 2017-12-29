from grid import Grid
from commons import *
from player import Player
from time import time
from order import Order
import json

class Game:

    def __init__(self):
        self.score = 0
        self.num_players = NUM_PLAYERS
        self.start_time = None
        self._active_recipes = []
        self.recipies_generated = 0
        self.grid = Grid()
        self.entities = [] #TODO initial postions of plates
        self.players = {}

    def add_player(self, plid):
        player = Player(self)
        self.players[plid] = player
        self.entities.append(player)

    def empty_tiles(self):
        return self.grid.empty_tiles() - [x.pos for x in self.entities]

    @property
    def ready(self):
        return len(self.players) >= self.num_players

    @property
    def recipes_count_to_time(self):
        return (time() - self.start_time)/ORDER_CREATION_INTERVAL

    @property
    def active_recipes(self):
        if not self.start_time:
            return []
        else:
            for i in range(self.recipies_generated, self.recipes_count_to_time):
                self.recipies_generated += 1
                self._active_recipes.append(Order.next())

        return self._active_recipes

    def start(self):
        self.start_time = time()

    def to_json(self):
        return json.dumps({
            "score": self.score,
            "orderList": [x.to_json() for x in self.active_recipes],
            "grid": self.grid.to_json(),
            "entities": [x.to_json() for x in self.entities]
        })


