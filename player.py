from commons import *
import json
import random

class Player:

    def __init__(self, game):
        self.game = game
        self.pos_max = game.grid.top_right_pos()

        self.pos = random.choice(game.empty_tiles())  # TODO random pick
        self.direction = Direction.up
        self.hands = None

    def _new_tile(self, new_x, new_y):
        if 0 <= new_x <= self.pos_max.x and 0 <= new_y <= self.pos_max.y:
            return Position(new_x, new_y)
        else:
            return Position(self.pos.x, self.pos.y)

    def _move_to(self, new_pos):
        if new_pos in self.game.empty_tiles():
            self.pos = new_pos
            if self.hands is not None:
                self.hands.pos = new_pos

    def move(self, command):
        getattr(self, command)()

    def up(self):
        self.direction = Direction.up
        self._move_to(self.active_tile())

    def down(self):
        self.direction = Direction.down
        self._move_to(self.active_tile())

    def left(self):
        self.direction = Direction.left
        self._move_to(self.active_tile())

    def right(self):
        self.direction = Direction.right
        self._move_to(self.active_tile())

    def active_tile(self):
        if self.direction == Direction.up:
            return self._new_tile(self.pos.x, self.pos.y - 1)
        elif self.direction == Direction.down:
            return self._new_tile(self.pos.x, self.pos.y + 1)
        if self.direction == Direction.right:
            return self._new_tile(self.pos.x + 1, self.pos.y)
        elif self.direction == Direction.left:
            return self._new_tile(self.pos.x - 1, self.pos.y)

    def drop(self, add_entity=True):
        if self.hands:
            if add_entity:
                self.game.entities.append(self.hands)

            self.hands.pos = Position(self.active_tile().x, self.active_tile().y)
            self.hands = None

    def to_json(self):
        return {
            "type": "player",
            "position": self.pos.to_json(),
            "entity": {
                "direction": self.direction.name,
                "hands": self.hands.to_json() if self.hands else None
            }
        }