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

    def reset(self):
        self.last = -1
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
        for rshift, cshift in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            r = self.row + rshift
            c = self.col + cshift
            if 0 <= r < ROWS and 0 <= c < COLS:
                ne_node = nodes[r][c]
                if not ne_node.wall and self.dist + 1 < ne_node.dist:
                    neigh.append((r, c))
        return neigh