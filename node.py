import pygame
import math
from constants import *


class Node:
    def __init__(self, win, row, col):
        self.win = win
        self.wall = False
        self.row = row
        self.col = col
        self.state = 0
        self.x = col * SQUARE_SIZE
        self.y = row * SQUARE_SIZE
        self.reset()

    def __lt__(self, other):
        if self.row == other.row:
            return self.col < other.col
        return self.row < other.row

    def reset(self):
        self.last = (-1, 0)
        self.dist = math.inf
        self.path = False

    def render(self, is_start, is_target):
        color = SQUARE_COLORS[self.state]
        if self.path:
            color = PATH_COLOR
        if is_start:
            color = START_COLOR
        if is_target:
            color = TARGET_COLOR
        pygame.draw.rect(self.win, SQUARE_BORDER_COLOR, (self.x, self.y, SQUARE_SIZE, SQUARE_SIZE))
        pygame.draw.rect(self.win, color, (self.x, self.y, SQUARE_SIZE - 2, SQUARE_SIZE - 2))

    def get_neighbours(self, nodes):
        neigh = []
        last_shift = (self.row - self.last[0], self.col - self.last[1])
        for rshift, cshift in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            r = self.row + rshift
            c = self.col + cshift
            if 0 <= r < ROWS and 0 <= c < COLS:
                ne_node = nodes[r][c]
                if not ne_node.wall and self.dist + 1 < ne_node.dist:
                    if (rshift, cshift) == last_shift:
                        neigh.insert(0, (r, c))
                    else:
                        neigh.append((r, c))
        return neigh

    def heuristic(self, target):
        return abs(target[0] - self.row) + abs(target[1] - self.col)
