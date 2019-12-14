import pygame


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

WIDTH = 74
HEIGHT = 74
MARGIN = 1

grid = [[0] * 8 for box in range(8)]
self = [1, 8]
other = [2, 9]
blank = 3

pygame.init()

WINDOW_SIZE = [600, 600]
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("checkers")
background_image = pygame.image.load("img/board.png").convert()
self_image = pygame.image.load("img/self.png").convert()
other_image = pygame.image.load("img/other.png").convert()
hint_img = pygame.image.load("img/hints.png").convert()
hide_img = pygame.image.load("img/hide.png").convert()
icon = pygame.image.load("img/checkers.png")
pygame.display.set_icon(icon)

# print(grid)
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

def checkers_board():
    for row in range(8):
        for column in range(8):
            color = WHITE
            if grid[row][column] == 1:
                color = GREEN
            pygame.draw.rect(screen, color, [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])

    screen.blit(background_image, [0, 0])

def get_indexes():
    pos = pygame.mouse.get_pos()
    column = pos[0] // (WIDTH + MARGIN)
    row = pos[1] // (HEIGHT + MARGIN)
    return row, column

def get_coordinates(row, column):
    if row==None and column==None:
        return None, None
    else:
        x = row * (WIDTH + MARGIN)
        y = column * (WIDTH + MARGIN)
        return x, y

def initial_board(grid):
    for i in range(8):
        for j in range(8):
            if j == 1:
                x, y = get_coordinates(i, j)
                if i%2 == 1:
                    screen.blit(self_image, [x + 5, y + 5])
                    grid[j][i] = self[0]
            elif j == 0 or j == 2:
                x, y = get_coordinates(i, j)
                if i%2 == 0:
                    screen.blit(self_image, [x+5, y+5])
                    grid[j][i] = self[0]

            elif j == 3:
                if i % 2 == 1:
                    grid[j][i] = blank

            elif j == 4:
                if i % 2 == 0:
                    grid[j][i] = blank

            elif j == 5 or j == 7:
                x, y = get_coordinates(i, j)
                if i%2 == 1:
                    screen.blit(other_image, [x + 5, y + 5])
                    grid[j][i] = other[0]
            elif j == 6:
                x, y = get_coordinates(i, j)
                if i%2 == 0:
                    screen.blit(other_image, [x+5, y+5])
                    grid[j][i] = other[0]

def hint_image(x,y):
    p, q = get_coordinates(x, y)
    if p==None and q==None:
        return
    else:
        screen.blit(hint_img, (q+5, p+5))

def hide_image(x,y):
    print("again hint", x4, y4)
    p, q = get_coordinates(x, y)
    if p==None and q==None:
        return None, None
    else:
        screen.blit(hide_img, (q+5, p+5))
    return None, None

def get_hints(grid, x, y, value):
    for i in range(8):
        for j in range(8):
            if value==0 or value==3:
                return None

            elif x%2==0 and y==0:
                if x==j and y==i and value==self[0]:
                    return [[x+1, y+1, grid[x+1][y+1]]]

                elif x==j and y==i and value==other[0]:
                    return [[x-1, y+1, grid[x-1][y+1]]]

            elif x%2==1 and y==7:
                if x==j and y==i and value==self[0]:
                    return [[x+1, y-1, grid[x+1][y-1]]]

                elif x==j and y==i and value==other[0]:
                    return [[x-1, y-1, grid[x-1][y-1]]]

            else:
                if x==j and y==i and value==self[0]:
                    return [[x+1, y-1, grid[x+1][y-1]] , [x+1, y+1, grid[x+1][y+1]]]

                elif x==j and y==i and value==other[0]:
                    return [[x-1, y-1, grid[x-1][y-1]] , [x-1, y+1, grid[x-1][y+1]]]

def move(grid, initial_x, initial_y,final_x, final_y):
    tmp = grid[initial_x][initial_y]
    grid[final_x][final_y] = tmp
    grid[initial_x][initial_y] = 3


def when_self(grid, initial_x, initial_y, initial_value, x1, y1, x2, y2, x3, y3, x4, y4, value1, value2, value3, value4):

    hint_list = get_hints(grid, initial_x, initial_y, initial_value)
    print("hint lists ", hint_list)

    for i in range(len(hint_list)):
        if i == 0:
            x1, y1, value1 = hint_list[0]
            if value1 == self[0]:
                x1 = None
                y1 = None
            elif value1 == 0:
                x1 = None
                y1 = None
            elif value1 == 3:
                pass

        elif i == 1:
            x2, y2, value2 = hint_list[1]
            if value2 == self[0]:
                x2 = None
                y2 = None
            elif value2 == 0:
                x2 = None
                y2 = None
            elif value2 == 3:
                pass

        elif i == 2:
            x3, y3, value3 = hint_list[3]
            if value3 == self[0]:
                x3 = None
                y3 = None
            elif value3 == 0:
                x3 = None
                y3 = None
            elif value3 == 3:
                pass

        elif i == 3:
            x4, y4, value4 = hint_list[4]
            if value4 == self[0]:
                x4 = None
                y4 = None
            elif value4 == 0:
                x4 = None
                y4 = None
            elif value4 == 3:
                pass

    hint_image(x1, y1)
    hint_image(x2, y2)
    hint_image(x3, y3)
    hint_image(x4, y4)
    pygame.display.update()
    print("hint1", x1, y1, value1)
    print("hint2", x2, y2, value2)
    print("hint3", x3, y3, value3)
    print("hint4", x4, y4, value4)
    return x1, y1, x2, y2, x3, y3, x4, y4, value1, value2, value3, value4


def on_click(grid, running, turn, initial_x, initial_y, initial_value, x1, y1, x2, y2, x3, y3, x4, y4, value1, value2, value3, value4):
    x1, y1, x2, y2, x3, y3, x4, y4 = None, None, None, None, None, None, None, None
    value1, value2, value3, value4 = 0, 0, 0, 0
    initial_x, initial_y, initial_value = 0, 0, 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x1, y1, x2, y2, x3, y3, x4, y4 = None, None, None, None, None, None, None, None
            value1, value2, value3, value4 = 0, 0, 0, 0
            print(grid)
            initial_x, initial_y = get_indexes()
            initial_value = grid[initial_x][initial_y]
            print("initials",initial_x, initial_y, initial_value)


            if initial_value == 3:
                break

            elif initial_value == 0:
                break

            elif turn == True and initial_value == self[0] or initial_value == self[1]:

                x1, y1, x2, y2, x3, y3, x4, y4, value1, value2, value3, value4 = when_self(grid, initial_x, initial_y, initial_value, x1, y1, x2, y2, x3, y3, x4, y4, value1, value2, value3, value4)



                keep = True
                while keep == True:

                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:

                            next_x, next_y = get_indexes()
                            next_value = grid[next_x][next_y]
                            print("nexts ", next_x, next_y, next_value)
                            if next_value == self[0] or next_value == self[1]:
                                x1, y1 = hide_image(x1, y1)
                                x2, y2 = hide_image(x2, y2)
                                x3, y3 = hide_image(x3, y3)
                                x4, y4 = hide_image(x4, y4)
                                pygame.display.update()
                                # print("again hint1", x1, y1)
                                # print("again hint2", x2, y2)
                                # print("again hint3", x3, y3)
                                print("again hint4", x4, y4)

                                when_self(grid, next_x, next_y, next_value, x1, y1, x2, y2, x3, y3, x4, y4, value1, value2, value3, value4)

                            elif next_value == 0:
                                turn = True


x1, y1, x2, y2, x3, y3, x4, y4 = None, None, None, None, None, None, None, None
value1, value2, value3, value4 = 0, 0, 0, 0
initial_x, initial_y, initial_value = 0, 0, 0

running = True
turn = True

while running:

    checkers_board()
    initial_board(grid)
    # screen.blit(other_image, [5, 5])
    on_click(grid, running, turn, initial_x, initial_y, initial_value, x1, y1, x2, y2, x3, y3, x4, y4, value1, value2, value3, value4)


                # print(turn)

            # elif turn == False and initial_value == other[0] or initial_value == other[1]:
            #     hint_list = get_hints(grid, initial_x, initial_y, initial_value)
            #     print("hint lists ", hint_list)
            #
            #     for i in range(len(hint_list)):
            #         if i == 0:
            #             x1, y1, value1 = hint_list[0]
            #             if value1 == self[0]:
            #                 x1 = None
            #                 y1 = None
            #             elif value1 == 0:
            #                 x1 = None
            #                 y1 = None
            #             elif value1 == 3:
            #                 pass
            #
            #         elif i == 1:
            #             x2, y2, value2 = hint_list[1]
            #             if value2 == self[0]:
            #                 x2 = None
            #                 y2 = None
            #             elif value2 == 0:
            #                 x2 = None
            #                 y2 = None
            #             elif value2 == 3:
            #                 pass
            #
            #         elif i == 2:
            #             x3, y3, value3 = hint_list[3]
            #             if value3 == self[0]:
            #                 x3 = None
            #                 y3 = None
            #             elif value3 == 0:
            #                 x3 = None
            #                 y3 = None
            #             elif value3 == 3:
            #                 pass
            #
            #         elif i == 3:
            #             x4, y4, value4 = hint_list[4]
            #             if value4 == self[0]:
            #                 x4 = None
            #                 y4 = None
            #             elif value4 == 0:
            #                 x4 = None
            #                 y4 = None
            #             elif value4 == 3:
            #                 pass
            #
            #     print("hint1", x1, y1, value1)
            #     print("hint2", x2, y2, value2)
            #     print("hint3", x3, y3, value3)
            #     print("hint4", x4, y4, value4)
            #
            #     keep = True
            #     while keep == True:
            #         hint_image(x1, y1)
            #         hint_image(x2, y2)
            #         hint_image(x3, y3)
            #         hint_image(x4, y4)
            #         pygame.display.update()
            #         if initial_value == other[0] or initial_value == other[1]:
            #             turn = False
            #             keep = False
            #
            #         elif initial_value == 0:
            #             turn = False
            #             keep = False






    clock.tick(60)

    pygame.display.flip()


# pygame.quit()