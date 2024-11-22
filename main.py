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
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

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

    # check if barriers or not. If not, add to neighbours list
    def update_neighbors(self, grid):
        self.neighbors = []
        # checking if row that we're at is less than total rows - 1
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN A ROW
                self.neighbors.append(grid[self.row + 1][self.col]) # append to next row down

        # if not at row 0, 
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.neighbors.append(grid[self.row - 1][self.col]) 

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1]) 

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])


    # less than, compare 2 nodes together
    def __lt__(self, other):
        return False
    
# define our heuristic function
def h(p1, p2):
    # we use manhattan distance
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs (y1 - y2)

# current node starts in end node
# traverse from end node back to start node
# eventually current will be equal to where we came from the last node
def reconstruct_path(came_from, current, draw):
    # while in dictionary (for backtracking)
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    # add to PriorityQueue (add startNode with F score to openSet)
    open_set.put((0, count, start)) # tie breakers
    # backtracking 
    came_from = {} # keeps track of which nodes came from where so we can find best path at the end
    # shortest distance from start node to this node
    g_score = {node: float("inf") for row in grid for node in row} 
    g_score[start] = 0 
    
    # f is heuristic (predicted) from this node to end
    f_score = {node: float("inf") for row in grid for node in row}
    # f is initially heuristic from start to start
    f_score[start] = h(start.get_pos(), end.get_pos())

    # if node is in queue (open set) or not
    open_set_hash = {start}
    # If empty weve considered every possible node that were going to
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # index stores f_score, count, and node. We just want the node
        # pop lowest value f_score from open set
        # current node were looking at (start node)
        current = open_set.get()[2]
        # take what node we just popped out of priority queue
        # and synchronize it in open set hash
        open_set_hash.remove(current)

        # if end node, we found the shortest path! reocnstruct and draw it
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        # otherwise consider all neighbors of current node
        for neighbor in current.neighbors:
            # calculate temp g_score
            temp_g_score = g_score[current] + 1 # assume all edges are 1

            # if we found a better way to reach neighbor (less)
            if temp_g_score < g_score[neighbor]:
                # update because we found a better path using row, col for the node
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                # add to open hash if they're already not in there
                if neighbor not in open_set_hash:
                    count += 1
                    # put in new neighbor that has better path
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw()

        # if current is not the start node, make it closed (red)
        if current != start:
            current.make_closed()

    # no path is found
    return Fale
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

def main(win, width):
    ROWS = 50
    # generate grid and gives us 2D array
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    started = False
    while run:
        draw(win, grid, ROWS, width)
        # loop through all events and check what they are 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # if user presses down on mouse
            # left mouse button
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                # gives us row, col we clicked on (node)
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]

                # if initial node not there
                if not start and node != end:
                    start = node
                    start.make_start()
                
                # if goal node not there
                elif not end and node != start:
                    end = node
                    end.make_end()
                
                # if we're not clicking on node nor end
                elif node != end and node != start:
                    node.make_barrier() 

            # right mousebutton
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                # reset it to be white
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None
            
            # did we press a key on keyDown. run algorithm
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            # update all neighbors
                            node.update_neighbors(grid)
                    # once we start, we call algorithm function
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                # clear if c is pressed
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    # remake entire grid
                    grid = make_grid(ROWS, width)

    # exits pygame
    pygame.quit()

main(WIN, WIDTH)