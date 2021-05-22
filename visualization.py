import pygame
import sys
import time
import math
from constants import *
from collections import deque
from queue import PriorityQueue
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
        self.s_pressed = False
        self.t_pressed = False
        self.algorithm = 0

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

    def run_algorithm(self):
        self.reset_path()
        if self.algorithm == 0:
            self.bfs()
        elif self.algorithm == 1:
            self.a_star()
        self.running = False

    def handle_key(self, key):
        if key == pygame.K_SPACE:
            self.run_algorithm()

        elif key == pygame.K_c:
            self.reset_path()
            self.reset_graph()

        elif key == pygame.K_r:
            self.reset_path()

        elif key == pygame.K_a:
            self.algorithm += 1
            self.algorithm %= len(ALGORITHMS)
            print(f"Changed algorithm to {ALGORITHMS[self.algorithm]}")

    def run(self):
        while True:
            self.mouse_pos = pygame.mouse.get_pos()
            self.mouse_clicked = pygame.mouse.get_pressed()[0]

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.handle_key(event.key)
                if event.type == pygame.QUIT:
                    return "QUIT"

            keys = pygame.key.get_pressed()
            self.s_pressed = keys[pygame.K_s]
            self.t_pressed = keys[pygame.K_t]

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
                        if self.s_pressed:
                            if self.target != (r, c):
                                self.start = (r, c)
                                node.wall = False
                        elif self.t_pressed:
                            if self.start != (r, c):
                                self.target = (r, c)
                                node.wall = False
                        else:
                            if self.start != (r, c) and self.target != (r, c):
                                node.wall = not node.wall
                                self.last_square = (r, c)
                if node.wall:
                    node.state = 2
                if node.dist != math.inf:
                    node.state = 3
                node.render(self.start == (r, c), self.target == (r, c))
        pygame.display.update()

    def find_path(self, start_node, target_node):
        current_node = target_node
        while True:
            if current_node == start_node:
                return
            current_node.path = True
            self.render()
            self.wait_for(0.05)
            current_node = self.get_node(current_node.last)

    def bfs(self):
        self.running = True
        print('Starting Breadth First Search...')
        last_dist = 1

        start_node = self.get_node(self.start)
        start_node.dist = 0
        target_node = self.get_node(self.target)

        q = deque()
        q.append(start_node)

        while q:
            node = q.popleft()

            if node.dist != last_dist:
                self.render()
                self.wait_for(0.1)
                last_dist = node.dist

            if node == target_node:
                self.find_path(start_node, target_node)
                return "finished"

            for neigh in node.get_neighbours(self.nodes):
                neigh_node = self.get_node(neigh)
                neigh_node.dist = node.dist + 1
                neigh_node.last = (node.row, node.col)
                q.append(neigh_node)

        print("NO PATH")

    def a_star(self):
        self.running = True
        print("Starting A* Search...")

        start_node = self.get_node(self.start)
        start_node.dist = 0
        target_node = self.get_node(self.target)

        q = PriorityQueue()
        q.put((0, 0, 0, start_node))

        while not q.empty():
            priority, _, _, node = q.get()

            if node == target_node:
                self.find_path(start_node, target_node)
                return "finished"

            self.render()
            self.wait_for(0.02)

            for idx, neigh in enumerate(node.get_neighbours(self.nodes)):
                neigh = self.get_node(neigh)
                new_dist = node.dist + 1
                if new_dist < neigh.dist:
                    neigh.dist = new_dist
                    h = neigh.heuristic(self.target)
                    priority = new_dist + h
                    q.put((priority, h, idx, neigh))
                    neigh.last = (node.row, node.col)

        print("NO PATH")
