from commons import *
from time import time
import json

class FoodType(Enum):
    onion = 1,
    mushroom = 2,
    tomato = 3,
    slicedOnion = 4,
    slicedMushroom = 5,
    slicedTomato = 6,
    onionSoup = 7,
    mushroomSoup = 8,
    tomatoSoup = 9

RAW_FOOD = [FoodType.onion, FoodType.mushroom, FoodType.tomato]
SLICED_FOOD = [FoodType.slicedOnion, FoodType.slicedMushroom, FoodType.slicedTomato]
SOUP_FOOD = [FoodType.onionSoup, FoodType.mushroomSoup, FoodType.tomatoSoup]

class Food(object):

    def __init__(self, ftype, pos, progress = 0):
        self.type = ftype
        self.pos = pos
        self.start_progress = progress
        self.cooking = False

    def cook(self, time_to_cook = PREPARE_TIME):
        self.cooking = True
        self.cook_start = time()
        self.cook_finish = self.cook_start + time_to_cook

    @property
    def progress(self):
        if self.start_progress >= 1:
            return 1

        if self.cooking:
            if time() > self.cook_finish:
                return 1
            else:
                return self.start_progress + (float(self.cook_finish - time()) / (self.cook_finish - self.cook_start))

    def drop_to(self, player, other_ent):
        if other_ent is None:
            player.drop(True)
            return True
        elif isinstance(other_ent, Food):
            return False
        elif isinstance(other_ent, Plate) or isinstance(other_ent, Pan):
            dropped = other_ent.add(self)
            if dropped:
                player.drop(False)

        return False

    def to_json(self):
        return {
            "type": "food",
            "position": self.pos.to_json(),
            "entity": {
                "type": self.type.name,
                "progress": self.progress
            }
        }


class Plate(object):

    def __init__(self, pos):
        self.pos = pos
        self.content = []

    def add(self, food):
        if food.type in SOUP_FOOD and len(self.content) < 1:
            self.content.append(food)
            return True
        return False

    def drop_to(self, player, other_ent):
        tile = player.game.grid.tile(player.active_tile())
        if tile == TileType.exit:
            correct = False
            for order in player.game.active_recipes:
                if order.check(self.content):
                    correct = True
                    player.game.score += COMPLETE_ORDER_BONUS
                    player.game.complete_order(order)
                    break

            if not correct:
                player.game.score -= WRONG_ORDER_PENALTY

            player.drop(False)
            return True
        elif other_ent is None:
            player.drop(True)
            return True
        elif isinstance(other_ent, Pan) and len(other_ent.content) == 0:
            other_ent.content = self
            player.drop(False)
            return True
        elif isinstance(other_ent, Pan) and other_ent.progress == 1 and len(self.content) == 0 and other_ent.content[0].type in SOUP_FOOD:
            self.content = other_ent.content
            other_ent.content = []
            return False

        return False

    def to_json(self):
        return {
            "type": "plate",
            "position": self.pos.to_json(),
            "entity": {
                "content": [x.to_json for x in self.content]
            }
        }

class Pan(object):

    def __init__(self, pos):
        self.pos = pos
        self.content = []

    def add(self, food):
        if food.type in SLICED_FOOD and len(self.content) < 3:
            self.content.append(food)
            food.cook()
            return True

        return False

    def drop_to(self, player, other_ent):
        if isinstance(other_ent, Plate) and len(other_ent.content) == 0 and self.progress == 1 and self.content[0].type in SOUP_FOOD:
            other_ent.content = self.content
            self.content = []
            return False
        elif other_ent is None:
            player.drop(True)
            return True

        return False

    @property
    def progress(self):
        if self.content:
            ret = mean([x.progress for x in self.content])
            if ret == 1 and len(set([x.type for x in self.content])) == 1 and len(self.content) == 3:
                self.content = [FoodType[self.content[0].value + 3]]

            return ret
        else:
            return 0

    def to_json(self):
        return {
            "type": "pan",
            "position": self.pos.to_json(),
            "entity": {
                "content": [x.to_json for x in self.content],
                "progress": self.progress
            }
        }


