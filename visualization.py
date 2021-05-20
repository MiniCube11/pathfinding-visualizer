import pygame
import sys
import time
import math
from constants import *
from collections import deque
from node import Node


class Visualization:
    def __init__(self, win):
        self.nodes = [[Node(win, r, c) for c in range(COLS)] for r in range(ROWS)]
        self.mouse_pos = (0, 0)
        self.mouse_clicked = False
        self.last_square = (-1, 0)
        self.start = (0, 0)
        self.target = (ROWS - 1, COLS - 1)
        self.running = False

    def check_quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def wait_for(self, wait_time):
        start_time = time.time()
        while True:
            self.check_quit()
            if time.time() - start_time >= wait_time:
                break

    def get_node(self, node_pos):
        r, c = node_pos
        return self.nodes[r][c]

    def reset_path(self):
        for row in self.nodes:
            for node in row:
                node.reset()

    def reset_graph(self):
        for row in self.nodes:
            for node in row:
                node.wall = False

    def run(self):
        while True:
            self.mouse_pos = pygame.mouse.get_pos()
            self.mouse_clicked = pygame.mouse.get_pressed()[0]

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.reset_path()
                        self.bfs()
                        self.running = False
                    if event.key == pygame.K_c:
                        self.reset_graph()
                    if event.key == pygame.K_r:
                        self.reset_path()
                if event.type == pygame.QUIT:
                    return "QUIT"

            self.render()

    def render(self):
        if not self.mouse_clicked:
            self.last_square = (-1, 0)
        for r in range(ROWS):
            for c in range(COLS):
                node = self.nodes[r][c]
                node.state = 0
                if node.x < self.mouse_pos[0] <= node.x + SQUARE_SIZE and node.y < self.mouse_pos[1] <= node.y + SQUARE_SIZE:
                    if not self.running:
                        node.state = 1
                    if self.mouse_clicked and self.last_square != (r, c) and self.target != (r, c):
                        node.wall = not node.wall
                        self.last_square = (r, c)
                if node.wall:
                    node.state = 2
                if node.dist != math.inf:
                    node.state = 3
                node.render(self.start == (r, c), self.target == (r, c))
        pygame.display.update()

    def find_path(self):
        current_node_pos = self.target
        while True:
            if current_node_pos == self.start:
                return
            current_node = self.get_node(current_node_pos)
            current_node.path = True
            self.render()
            self.wait_for(0.05)
            current_node_pos = current_node.last

    def bfs(self):
        self.running = True
        print('Breadth First Search')
        q = deque()
        q.append(self.start)
        self.get_node(self.start).dist = 0
        last_dist = 1

        while q:
            node_pos = q.popleft()
            node = self.get_node(node_pos)

            if node.dist != last_dist:
                self.render()
                self.wait_for(0.1)
                last_dist = node.dist

            if node_pos == self.target:
                self.find_path()
                return "finished"

            for neigh in node.get_neighbours(self.nodes):
                neigh_node = self.get_node(neigh)
                neigh_node.dist = node.dist + 1
                neigh_node.last = node_pos
                q.append(neigh)

        print("NO PATH")
