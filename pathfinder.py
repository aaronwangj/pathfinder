import math
import pygame
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("Pathfinding Visualization")

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

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_open(self):
        return self.color == GREEN

    def is_closed(self):
        return self.color == RED

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def set_open(self):
        self.color = GREEN
    
    def set_closed(self):
        self.color = RED

    def set_barrier(self):
        self.color = BLACK

    def set_start(self):
        self.color = ORANGE

    def set_end(self):
        self.color = TURQUOISE

    def set_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row+1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x2 - x1) + abs(y2 - y1)

def draw_path(origin, end, draw):
    while end in origin:
        end = origin[end]
        end.set_path()
        draw()


def astar(draw, grid, start, end):
    count = 0
    os = PriorityQueue()
    os.put((0, count, start))
    origin = {}
    g = {node: float("inf") for row in grid for node in row}
    g[start] = 0
    f = {node: float("inf") for row in grid for node in row}
    f[start] = h(start.get_pos(), end.get_pos())

    os_hash = {start}

    while not os.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = os.get()[2]
        os_hash.remove(current)

        if current == end:
            draw_path(origin, end, draw)
            end.set_end()
            start.set_start()
            return True

        for neighbor in current.neighbors:
            temp_g = g[current] + 1

            if temp_g < g[neighbor]:
                origin[neighbor] = current
                g[neighbor] = temp_g
                f[neighbor] = temp_g + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in os_hash:
                    count += 1
                    os.put((f[neighbor], count, neighbor))
                    os_hash.add(neighbor)
                    neighbor.set_open()

        draw()

        if current != start:
            current.set_closed()
    
    return False

def set_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

def main(win, width):
    ROWS = 50
    grid = set_grid(ROWS, width)

    start = None
    end = None
    run = True

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                
                if not start and node != end:
                    start = node
                    start.set_start()
                
                elif not end and node != start:
                    end = node
                    end.set_end()

                elif node != start and node != end:
                    node.set_barrier()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                if node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    astar(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_BACKSPACE:
                    start = None
                    end = None
                    grid = set_grid(ROWS, width)


    pygame.quit()

main(WIN, WIDTH)




















