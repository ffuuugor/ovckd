from grid import Grid
from commons import *
from player import Player
from time import time
from order import Order
from food import *
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

    def entity_at(self, pos):
        for ent in self.entities:
            if ent.pos == pos:
                return ent

        return None

    def empty_tiles(self):
        return list(set(self.grid.empty_tiles()) - set([x.pos for x in self.entities]))

    @property
    def ready(self):
        return len(self.players) >= self.num_players

    @property
    def recipes_count_to_time(self):
        return int((time() - self.start_time)/ORDER_CREATION_INTERVAL)

    @property
    def active_recipes(self):
        if not self.start_time:
            return []
        else:
            for i in range(self.recipies_generated, self.recipes_count_to_time):
                self.recipies_generated += 1
                self._active_recipes.append(Order.next())

        return self._active_recipes

    def complete_order(self, order):
        self._active_recipes = self._active_recipes - order

    def start(self):
        self.start_time = time()

    def to_json(self):
        return json.dumps({
            "score": self.score,
            "orderList": [x.to_json() for x in self.active_recipes],
            "grid": self.grid.grid,
            "entities": [x.to_json() for x in self.entities]
        })

    def move(self, player_id, cmd):
        self.players[player_id].move(cmd)

    def start_cut(self, player_id):
        player = self.players[player_id]
        ent = self.entity_at(player.active_tile())
        if ent is not None and isinstance(ent, Food) and ent.type in RAW_FOOD and self.grid.tile(player.active_tile()) == TileType.knife.value:
            ent.cook()

    def take_or_drop(self, player_id):
        player = self.players[player_id]
        external_ent = self.entity_at(player.active_tile())

        if player.hands:
            if player.pos != player.active_tile():
                player.hands.drop_to(player, external_ent)
        elif external_ent:
           player.hands = external_ent
           self.entities.remove(external_ent)
        else:
            tile = self.grid.tile(player.active_tile())
            if tile == TileType.mushroom_box:
                self.entities.append(Food(FoodType.mushroom, player.active_tile()))
            elif tile == TileType.onion_box:
                self.entities.append(Food(FoodType.onion, player.active_tile()))
            elif tile == TileType.tomato_box:
                self.entities.append(Food(FoodType.tomato, player.active_tile()))


