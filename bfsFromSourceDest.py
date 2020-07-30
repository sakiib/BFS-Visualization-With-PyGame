import pygame

WIDTH = 650
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("BFS From Both Source & Destination!")


RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Spot:
    dx = [0, 0, 1, -1]
    dy = [1, -1, 0, 0]

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

    def is_closed(self):
        return self.color == TURQUOISE

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == RED

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = TURQUOISE

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = RED

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        for i in range(len(self.dx)):
            next_row = self.row + self.dx[i]
            next_col = self.col + self.dy[i]
            if 0 <= next_row < self.total_rows and 0 <= next_col < self.total_rows:
                if not grid[next_row][next_col].is_barrier():
                    self.neighbors.append(grid[next_row][next_col])


def reconstruct_path(came_start, came_end, current, draw, start, end):
    temp = current
    current.make_path()
    draw()
    while current in came_start:
        current = came_start[current]
        if current.color == ORANGE:
            break
        current.make_path()
        draw()
    current = temp
    while current in came_end:
        current = came_end[current]
        if current.color == BLUE:
            break
        current.make_path()
        draw()


def bfs_from_source_dest(draw, grid, start, end):
    cost_start = {spot: float("inf") for row in grid for spot in row}
    cost_end = {spot: float("inf") for row in grid for spot in row}
    visited_start = {spot: False for row in grid for spot in row}
    visited_end = {spot: False for row in grid for spot in row}
    cost_start[start] = 0
    cost_end[end] = 0
    visited_start[start] = True
    visited_end[end] = True
    queue_start = [start]
    queue_end = [end]
    came_start = {}
    came_end = {}
    while queue_start or queue_end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        if len(queue_start):
            current = queue_start.pop(0)
            if visited_start[current] and visited_end[current]:
                print('Shortest Distance = {}'.format(cost_start[current] + cost_end[current]))
                reconstruct_path(came_start, came_end, current, draw, start, end)
                end.make_end()
                return True
            for neighbor in current.neighbors:
                if cost_start[neighbor] == float("inf") or cost_start[neighbor] > cost_start[current] + 1:
                    came_start[neighbor] = current
                    visited_start[neighbor] = True
                    cost_start[neighbor] = cost_start[current] + 1
                    queue_start.append(neighbor)
                    neighbor.make_open()
            draw()
            if current != start and current != end:
                current.make_closed()
        if len(queue_end):
            current = queue_end.pop(0)
            if visited_start[current] and visited_end[current]:
                print('Shortest Distance = {}'.format(cost_start[current] + cost_end[current]))
                reconstruct_path(came_start, came_end, current, draw, start, end)
                end.make_end()
                return True
            for neighbor in current.neighbors:
                if cost_end[neighbor] == float("inf") or cost_end[neighbor] > cost_end[current] + 1:
                    came_end[neighbor] = current
                    visited_end[neighbor] = True
                    cost_end[neighbor] = cost_end[current] + 1
                    queue_end.append(neighbor)
                    neighbor.make_open()
            draw()
            if current != start and current != end:
                current.make_closed()
    return False


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
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
        for spot in row:
            spot.draw(win)
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
    grid = make_grid(ROWS, width)
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
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()
                elif not end and spot != start:
                    end = spot
                    end.make_end()
                elif spot != end and spot != start:
                    spot.make_barrier()
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    bfs_from_source_dest(lambda: draw(win, grid, ROWS, width), grid, start, end)
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
    pygame.quit()


if __name__ == '__main__':
    main(WIN, WIDTH)
