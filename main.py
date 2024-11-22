import pygame
import math
from queue import PriorityQueue


WIDTH = 800
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("A* Pathfinding Algorithm Visualizer")


RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

# holds different values, keep track where it is, what row column
# know width so it can draw itself
# keeps track of all its neighbours
class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        # keep track of coordinate position (x,y)
        self.x = row * width
        self.y = col * width 
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col
    
    # have we already looked/considered the node
    def is_closed(self):
        return self.color == RED

    # is the node in the open set
    def is_open(self):
        return self.color == GREEN
    
    def is_barrier(self):
        return self.color == BLACK
    
    # initial node
    def is_start(self):
        return self.color == ORANGE
    
    # goal node
    def is_end(self):
        return self.color == PURPLE
    
    def reset(self):
        self.color == WHITE

    def make_closed(self):
        self.color = RED
    
    def make_open(self):
        self.color = GREEN
    
    # make walls
    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE
    
    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        # draw a cube in pygame
        pygame.draw.rect(win, self.color,(self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        pass

    # less than, compare 2 nodes together
    def __lt__(self, other):
        return False
    
# define our heuristic function
def h(p1, p2):
    # we use manhattan distance
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs (y1 - y2)

# make a grid
def make_grid(rows, width):
    grid = []
    # gap should be between each rows (or width of each cube)
    gap = width // rows
    for i in range (rows):
        grid.append([])
        for j in range(rows):
            # row, column, width, total rows
            node = Node(i, j, gap, rows)
            # list of list
            grid[i].append(node)

    return grid

# draw the grid
def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        # for every row we draw a horizontal line
        # multiply the current index of the row were on by gap
        # will tell us where we should be drawing the grid line
        pygame.draw.line(win,GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            # draw vertical lines. shift along x axis and draw
            pygame.draw.line(win,GREY, (j * gap, 0), (j * gap, width))

# main draw function that draws
def draw(win, grid, rows, width):
    # fills entire screen with a color for each frame
    win.fill(WHITE)

    # draws its own color on its x,y,width (cube)
    for row in grid:
        for node in row:
            node.draw(win)

    # draw grid lines on top
    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    # find x, y position and divide by width of cubes
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    # return row, col of clicked
    return row, col

