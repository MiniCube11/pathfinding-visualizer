import pygame
from visualization import Visualization
from constants import *

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinding")

visualization = Visualization(win)
visualization.run()

pygame.quit()
