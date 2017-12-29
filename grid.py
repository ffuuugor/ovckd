from commons import *


class Grid:

    DEFAULT_GRID = [
        [1, 3, 2, 2, 2, 2, 1],
        [2, 0, 0, 0, 0, 0, 2],
        [4, 0, 2, 6, 2, 0, 5],
        [2, 0, 0, 0, 0, 0, 2],
        [4, 0, 2, 7, 2, 0, 5],
        [2, 0, 0, 0, 0, 0, 2],
        [1, 2, 2, 2, 2, 2, 1],
    ]

    def __init__(self, grid=None):
        if grid:
            self.grid = grid
        else:
            self.grid = self.DEFAULT_GRID

    def top_right_pos(self):
        return Position(len(self.grid[0])-1, len(self.grid))

    def tile(self, x, y):
        return TileType(self.grid[y, x])

    def empty_tiles(self):
        ret = []
        for y in range(0, len(self.grid)):
            for x in range(0, len(self.grid[y])):
                if self.grid[y][x] == 0:
                    ret.append(Position(x, y))

        return ret