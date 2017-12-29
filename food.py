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

    def to_json(self):
        return json.dumps({
            "type": "food",
            "position": self.pos.to_json(),
            "entity": {
                "type": self.type.name,
                "progress": self.progress
            }
        })


class Plate(object):

    def __init__(self, pos):
        self.pos = pos
        self.content = []

    def add(self, food):
        if food.type in [FoodType.mushroomSoup, FoodType.onionSoup, FoodType.tomatoSoup] and len(self.content) < 1:
            self.content.append(food)

    def to_json(self):
        return json.dumps({
            "type": "plate",
            "position": self.pos.to_json(),
            "entity": {
                "content": [x.to_json for x in self.content]
            }
        })

class Pan(object):

    def __init__(self, pos):
        self.pos = pos
        self.content = []

    def add(self, food):
        if food.type in [FoodType.slicedOnion, FoodType.slicedMushroom, FoodType.slicedTomato] and len(self.content) < 3:
            self.content.append(food)
            food.cook()

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
        return json.dumps({
            "type": "pan",
            "position": self.pos.to_json(),
            "entity": {
                "content": [x.to_json for x in self.content],
                "progress": self.progress
            }
        })


