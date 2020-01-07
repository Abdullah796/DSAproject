import pygame
import time
import random

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

running = True
turn = False
repeat = False
keep = True

pygame.init()

WINDOW_SIZE = [600, 600]
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("checkers")

background_image = pygame.image.load("img/board.png").convert()
self_img = pygame.image.load("img/self.png").convert()
you_image = pygame.image.load("img/you-win.png").convert()
computer_image = pygame.image.load("img/computer-win.png").convert()
self_king_img = pygame.image.load("img/self-king.png").convert()
other_img = pygame.image.load("img/other.png").convert()
other_king_img = pygame.image.load("img/other-king.png").convert()
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
                    screen.blit(self_img, [x + 5, y + 5])
                    grid[j][i] = self[0]
            elif j == 0 or j == 2:
                x, y = get_coordinates(i, j)
                if i%2 == 0:
                    screen.blit(self_img, [x+5, y+5])
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
                    screen.blit(other_img, [x + 5, y + 5])
                    grid[j][i] = other[0]
            elif j == 6:
                x, y = get_coordinates(i, j)
                if i%2 == 0:
                    screen.blit(other_img, [x+5, y+5])
                    grid[j][i] = other[0]

def hint_image(x,y):
    p, q = get_coordinates(x, y)
    if p==None and q==None:
        return
    else:
        screen.blit(hint_img, (q+5, p+5))
        pygame.display.update()

def self_image(x,y):
    p, q = get_coordinates(x, y)
    if p==None and q==None:
        return
    else:
        screen.blit(self_img, (q+5, p+5))
        pygame.display.update()

def self_king_image(x,y):
    p, q = get_coordinates(x, y)
    if p==None and q==None:
        return
    else:
        screen.blit(self_king_img, (q+5, p+5))
        pygame.display.update()

def other_image(x,y):
    p, q = get_coordinates(x, y)
    if p==None and q==None:
        return
    else:
        screen.blit(other_img, (q+5, p+5))
        pygame.display.update()

def other_king_image(x,y):
    p, q = get_coordinates(x, y)
    if p==None and q==None:
        return
    else:
        screen.blit(other_king_img, (q+5, p+5))
        pygame.display.update()


def hide_image(x,y):
    p, q = get_coordinates(x, y)
    if p==None and q==None:
        return
    else:
        screen.blit(hide_img, (q+5, p+5))
        pygame.display.update()

def hide_image_if_blank(grid,x,y):
    p, q = get_coordinates(x, y)
    if p==None and q==None:
        return
    elif grid[x][y] == self[0] or grid[x][y] == self[1] or grid[x][y] == other[0] or grid[x][y] == other[1]:
        return
    else:
        screen.blit(hide_img, (q+5, p+5))
        pygame.display.update()



def get_hints(grid, x, y, value):
    for i in range(8):
        for j in range(8):
            if value==0: # or value==3:
                return None
            elif x%2==0 and y==0 and x==j and y==i:
                if value==self[0]:
                    return [[None, None, 0] , [x+1, y+1, grid[x+1][y+1]]]
                elif value==other[0]:
                    return [[None, None, 0], [x-1, y+1, grid[x-1][y+1]]]
                elif value==self[1] or other[1]:
                    if x==0:
                        return [[None, None, 0], [x + 1, y + 1, grid[x + 1][y + 1]], [None, None, 0],[None, None, 0]]
                    else:
                        return [[None, None, 0], [x + 1, y + 1, grid[x + 1][y + 1]], [None, None, 0], [x-1, y+1, grid[x-1][y+1]]]

            elif x%2==1 and y==7 and x==j and y==i:
                if value==self[0]:
                    return [[x+1, y-1, grid[x+1][y-1]], [None, None, 0]]
                elif value==other[0]:
                    return [[x-1, y-1, grid[x-1][y-1]], [None, None, 0]]
                elif value == self[1] or other[1]:
                    if x==7:
                        return [[None, None, 0], [None, None, 0], [x-1, y-1, grid[x-1][y-1]],[None, None, 0]]
                    else:
                        return [[x+1, y-1, grid[x+1][y-1]], [None, None, 0], [x-1, y-1, grid[x-1][y-1]], [None, None, 0]]

            elif x==j and y==i:
                if value==self[0]:
                    return [[x+1, y-1, grid[x+1][y-1]] , [x+1, y+1, grid[x+1][y+1]]]
                elif value==other[0]:
                    return [[x-1, y-1, grid[x-1][y-1]] , [x-1, y+1, grid[x-1][y+1]]]
                elif value == self[1] or other[1]:
                    if x==0:
                        return [[x + 1, y - 1, grid[x + 1][y - 1]], [x + 1, y + 1, grid[x + 1][y + 1]],[None, None, 0], [None, None, 0]]
                    elif x==7:
                        return [[None, None, 0], [None, None, 0],[x - 1, y - 1, grid[x - 1][y - 1]], [x - 1, y + 1, grid[x - 1][y + 1]]]
                    else:
                        return [[x+1, y-1, grid[x+1][y-1]] , [x+1, y+1, grid[x+1][y+1]], [x-1, y-1, grid[x-1][y-1]] , [x-1, y+1, grid[x-1][y+1]]]


def get_hint_next_left(grid, x,  y, got_value):
    if x == None and y==None:
        return None, None, 0
    else:
        for i in range(8):
            for j in range(8):
                if got_value==self[0]:
                    if x+1<8 and y-1>=0:
                        return x+1, y-1, grid[x+1][y-1]
                    else:
                        return None, None, 0
                elif got_value == other[0]:
                    if x-1 >=0 and y-1 >= 0:
                        return x-1, y-1, grid[x-1][y-1]
                    else:
                        return None, None, 0

def get_hint_next_right(grid, x,  y, got_value):
    if x == None and y==None:
        return None, None, 0
    else:
        for i in range(8):
            for j in range(8):
                if got_value==self[0]:
                    if x+1<8 and y+1<8:
                        return x+1, y+1, grid[x+1][y+1]
                    else:
                        return None, None, 0
                elif got_value == other[0]:
                    if x-1 >=0 and y+1 <8:
                        return x-1, y+1, grid[x-1][y+1]
                    else:
                        return None, None, 0

def hint_next_down_left(grid, x,  y):
    if x == None and y==None:
        return [None, None, 0]
    else:
        for i in range(8):
            for j in range(8):
                if x + 1 < 8 and y - 1 >= 0:
                    return [x + 1, y - 1, grid[x + 1][y - 1]]
                else:
                    return [None, None, 0]

def hint_next_down_right(grid, x,  y):
    if x == None and y==None:
        return [None, None, 0]
    else:
        for i in range(8):
            for j in range(8):
                if x + 1 < 8 and y + 1 < 8:
                    return [x + 1, y + 1, grid[x + 1][y + 1]]
                else:
                    return [None, None, 0]

def hint_next_up_left(grid, x,  y):
    if x == None and y==None:
        return [None, None, 0]
    else:
        for i in range(8):
            for j in range(8):
                if x - 1 >= 0 and y - 1 >= 0:
                    return [x - 1, y - 1, grid[x - 1][y - 1]]
                else:
                    return [None, None, 0]

def hint_next_up_right(grid, x,  y):
    if x == None and y==None:
        return [None, None, 0]
    else:
        for i in range(8):
            for j in range(8):
                if x - 1 >= 0 and y + 1 < 8:
                    return [x - 1, y + 1, grid[x - 1][y + 1]]
                else:
                    return [None, None, 0]

def get_hint_next_list(grid, hints):
    hints_next = []

    x1,y1,value1 = hints[0]
    hint_next1 = hint_next_down_left(grid, x1,y1)
    hints_next.append(hint_next1)

    x2,y2,value2 = hints[1]
    hint_next2 = hint_next_down_right(grid, x2,y2)
    hints_next.append(hint_next2)

    x3,y3,value3 = hints[2]
    hint_next3 = hint_next_up_left(grid, x3,y3)
    hints_next.append(hint_next3)

    x4,y4,value4 = hints[3]
    hint_next4 = hint_next_up_right(grid, x4,y4)
    hints_next.append(hint_next4)

    return hints_next


def getSeparateHints(grid, initial_x, initial_y, initial_value, hint_x1, hint_y1, hint_x2, hint_y2, hint_x3, hint_y3, hint_x4, hint_y4, hint_value1, hint_value2, hint_value3, hint_value4):

    hint_list = get_hints(grid, initial_x, initial_y, initial_value)
    print("hint lists ", hint_list)

    for i in range(len(hint_list)):
        if i == 0:
            hint_x1, hint_y1, hint_value1 = hint_list[0]
            if hint_value1 == 0:
                hint_x1 = None
                hint_y1 = None
            elif hint_value1 == 3:
                pass

        elif i == 1:
            hint_x2, hint_y2, hint_value2 = hint_list[1]
            if hint_value2 == 0:
                hint_x2 = None
                hint_y2 = None
            elif hint_value2 == 3:
                pass

        elif i == 2:
            hint_x3, hint_y3, hint_value3 = hint_list[3]
            if hint_value3 == 0:
                hint_x3 = None
                hint_y3 = None
            elif hint_value3 == 3:
                pass

        elif i == 3:
            hint_x4, hint_y4, hint_value4 = hint_list[4]
            if hint_value4 == 0:
                hint_x4 = None
                hint_y4 = None
            elif hint_value4 == 3:
                pass

    pygame.display.update()
    print("hint1", hint_x1, hint_y1, hint_value1)
    print("hint2", hint_x2, hint_y2, hint_value2)
    print("hint3", hint_x3, hint_y3, hint_value3)
    print("hint4", hint_x4, hint_y4, hint_value4)
    return hint_x1, hint_y1, hint_x2, hint_y2, hint_x3, hint_y3, hint_x4, hint_y4, hint_value1, hint_value2, hint_value3, hint_value4

def moveSelfHintBlank(grid,self_x,self_y,self_value,blank_x,blank_y,blank_value):
    if blank_value == 3:
        if blank_x == 7:
            grid[self_x][self_y] = blank_value
            grid[blank_x][blank_y] = self[1]
            self_value = blank_value
            self_king_image(blank_x, blank_y)
            pygame.display.update()
        else:
            grid[self_x][self_y] = blank_value
            grid[blank_x][blank_y] = self_value
            self_value = blank_value
            self_image(blank_x, blank_y)
            pygame.display.update()

        hide_image(self_x, self_y)
        pygame.display.update()
        print("moved",grid)
    else:
        return

def moveSelfNextHintBlank(grid,self_x,self_y,self_value,other_x,other_y,other_value,blank_x,blank_y,blank_value):
    if blank_value == 3:
        if blank_x == 7:
            grid[self_x][self_y] = blank_value
            grid[other_x][other_y] = blank_value
            grid[blank_x][blank_y] = self[1]
            self_king_image(blank_x, blank_y)
        else:
            grid[self_x][self_y] = blank_value
            grid[other_x][other_y] = blank_value
            grid[blank_x][blank_y] = self_value
            self_image(blank_x, blank_y)
        hide_image(self_x, self_y)
        hide_image(other_x, other_y)
        pygame.display.update()
        print("moved",grid)
    else:
        return

def moveOtherNextHintBlank(grid,self_x,self_y,self_value,other_x,other_y,other_value,blank_x,blank_y,blank_value):
    if blank_value == 3:
        if blank_x == 0:
            grid[self_x][self_y] = blank_value
            grid[other_x][other_y] = blank_value
            grid[blank_x][blank_y] = other[1]
            other_king_image(blank_x, blank_y)
        else:
            grid[self_x][self_y] = blank_value
            grid[other_x][other_y] = blank_value
            grid[blank_x][blank_y] = self_value
            other_image(blank_x, blank_y)
        hide_image(self_x, self_y)
        hide_image(other_x, other_y)
        pygame.display.update()
        print("moved",grid)
    else:
        return

def moveOtherHintBlank(grid,self_x,self_y,self_value,blank_x,blank_y,blank_value):
    if blank_value == 3:
        if blank_x == 0:
            grid[self_x][self_y] = blank_value
            grid[blank_x][blank_y] = other[1]
            self_value = blank_value
            other_king_image(blank_x, blank_y)
            pygame.display.update()
        else:
            grid[self_x][self_y] = blank_value
            grid[blank_x][blank_y] = self_value
            self_value = blank_value
            other_image(blank_x, blank_y)
            pygame.display.update()
        hide_image(self_x, self_y)
        pygame.display.update()
        print("moved",grid)
    else:
        return

def moveSelfKingHintBlank(grid,self_x,self_y,self_value,blank_x,blank_y,blank_value):
    if blank_value == 3:
        grid[self_x][self_y] = blank_value
        grid[blank_x][blank_y] = self_value
        self_king_image(blank_x, blank_y)
        pygame.display.update()
        hide_image(self_x, self_y)
        pygame.display.update()
        print("moved", grid)
    else:
        return

def moveOtherKingHintBlank(grid,self_x,self_y,self_value,blank_x,blank_y,blank_value):
    if blank_value == 3:
        grid[self_x][self_y] = blank_value
        grid[blank_x][blank_y] = self_value
        other_king_image(blank_x, blank_y)
        pygame.display.update()
        hide_image(self_x, self_y)
        pygame.display.update()
        print("moved", grid)
    else:
        return

def moveSelfKingNextHintBlank(grid,self_x,self_y,self_value,other_x,other_y,other_value,blank_x,blank_y,blank_value):
    if blank_value == 3:
        grid[self_x][self_y] = blank_value
        grid[other_x][other_y] = blank_value
        grid[blank_x][blank_y] = self_value
        self_king_image(blank_x, blank_y)
        hide_image(self_x, self_y)
        hide_image(other_x, other_y)
        pygame.display.update()
        print("moved",grid)
    else:
        return

def moveOtherKingNextHintBlank(grid,self_x,self_y,self_value,other_x,other_y,other_value,blank_x,blank_y,blank_value):
    if blank_value == 3:
        grid[self_x][self_y] = blank_value
        grid[other_x][other_y] = blank_value
        grid[blank_x][blank_y] = self_value
        other_king_image(blank_x, blank_y)
        hide_image(self_x, self_y)
        hide_image(other_x, other_y)
        pygame.display.update()
        print("moved",grid)
    else:
        return


def get_hint_next_list_self(grid, hints):  # used in priority_1 for self[0] only
    hints_next = []
    if hints[0][2] == 2 or hints[0][2] == 9:
        x1, y1, value1 = hints[0]
        hint_next1 = hint_next_down_left(grid, x1, y1)
        hints_next.append(hint_next1)
    if hints[1][2] == 2 or hints[1][2] == 9:
        x2, y2, value2 = hints[1]
        hint_next2 = hint_next_down_right(grid, x2, y2)
        hints_next.append(hint_next2)

    return hints_next


def get_hint_next_list_queen(grid, hints):  # used in priority_1 for self[1] only
    hints_next = []
    if hints[0][2] == 2 or hints[0][2] == 9:
        x1, y1, value1 = hints[0]
        hint_next1 = hint_next_down_left(grid, x1, y1)
        hints_next.append(hint_next1)
    if hints[1][2] == 2 or hints[1][2] == 9:
        x2, y2, value2 = hints[1]
        hint_next2 = hint_next_down_right(grid, x2, y2)
        hints_next.append(hint_next2)
    if hints[2][2] == 2 or hints[2][2] == 9:
        x3, y3, value3 = hints[2]
        hint_next3 = hint_next_up_left(grid, x3, y3)
        hints_next.append(hint_next3)
    if hints[3][2] == 2 or hints[3][2] == 9:
        x4, y4, value4 = hints[3]
        hint_next4 = hint_next_up_right(grid, x4, y4)
        hints_next.append(hint_next4)

    return hints_next


def isPriority_1(grid):
    list1 = []
    list1_indexes = []
    list2 = []
    list2_indexes = []
    list3 = []
    list3_indexes = []
    list4 = []
    list4_indexes = []
    for i in range(8):
        for j in range(8):
            if grid[i][j] == 1:
                list1.append(get_hints(grid, i, j, 1))
                list1_indexes.append([i, j, grid[i][j]])
            if grid[i][j] == 8:
                list3.append(get_hints(grid, i, j, 8))
                list3_indexes.append([i, j, grid[i][j]])
    for i in list1:
        list2.append(get_hint_next_list_self(grid, i))
    for i in list3:
        list4.append(get_hint_next_list_queen(grid, i))
    counta = 0

    for i in list4:

        if len(i) > 0:
            if i[0][2] == 3:
                list4_indexes.append(counta)
        counta += 1

    for i in list4_indexes:
        return list3_indexes[i]
        break

    count1 = 0
    for i in list2:
        if len(i) > 0:
            if i[0][2] == 3:
                list2_indexes.append(count1)
        count1 += 1
    for i in list2_indexes:
        return list1_indexes[i]
        break


def isPriority_2(grid):
    list1 = []
    list1_indexes = []
    list2 = []
    for i in range(8):
        for j in range(8):
            if grid[i][j] == 1:
                list1.append(get_hints(grid, i, j, 1))
                list1_indexes.append([i, j, grid[i][j]])
            if grid[i][j] == 8:
                list1.append(get_hints(grid, i, j, 8))
                list1_indexes.append([i, j, grid[i][j]])

    counta = 0
    list2_indexes = []
    for i in list1:
        for j in i:
            if j[2] == 3:
                list2_indexes.append(counta)
        counta += 1
    for i in list2_indexes:
        return list1_indexes[i]
        break

def is_win(grid, turn):
    count_computer = 0
    count_you = 0
    for i in grid:
        for j in i:
            if j == self[0] or j == self[1]:
                count_computer += 1
            elif j == other[0] or j == other[1]:
                count_you += 1
    if count_computer==0:
        screen.blit(you_image, [0, 0])
        pygame.display.update()
        while True:
            print("you win")
    elif count_you == 0:
        screen.blit       (computer_image, [0, 0])
        pygame.display.update()
        while True:
            print("computer win")


hint_x1, hint_y1, hint_x2, hint_y2, hint_x3, hint_y3, hint_x4, hint_y4 = None, None, None, None, None, None, None, None
hint_value1, hint_value2, hint_value3, hint_value4 = 0, 0, 0, 0
next_hint_x1, next_hint_y1, next_hint_x2, next_hint_y2,next_hint_value1, next_hint_value2 = None, None, None, None, 0, 0
next_hint_x3, next_hint_y3, next_hint_x4, next_hint_y4,next_hint_value3, next_hint_value4 = None, None, None, None, 0, 0

initial_x, initial_y, initial_value = 0, 0, 0
tab_hint_x, tab_hint_y, tab_hint_value = 0, 0, 0

hint1, hint2, hint1, hint2 = 0, 0, 0, 0

hints = 0
next_hints = 0
first_priority = []
second_priority = []


# running = True
# turn = True
# repeat = False



checkers_board()
initial_board(grid)
print(grid)


while running == True:

    is_win(grid, turn)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if turn == True:

            time.sleep(1)

            x = isPriority_1(grid)
            y = isPriority_2(grid)
            if x != None:
                initial_x, initial_y, initial_value = x
            elif y!= None:
                initial_x, initial_y, initial_value = y
            elif x == None and y==None:
                screen.blit(you_image, [0, 0])
                pygame.display.update()
                while True:
                    print("you win")

            print("initials",initial_x, initial_y, initial_value)


            if initial_value == 3 or initial_value == 0:
                pass


            elif initial_value == self[1]:
                hints = get_hints(grid, initial_x, initial_y, initial_value)
                print(hints)
                next_hints = get_hint_next_list(grid, hints)
                print(next_hints)

                for i in range(4):                           #no of hints of king =4
                    if hints[i][-1] !=3 and next_hints[i][-1] == 3:
                        if hints[i][-1] == other[0] or hints[i][-1] == other[1]:
                            first_priority.append([hints[i],next_hints[i]])
                    elif hints[i][-1] == 3:
                        second_priority.append(hints[i])

                random.shuffle(first_priority)
                random.shuffle(second_priority)

                print("first priority", first_priority)
                print("Second priority", second_priority)

                if len(first_priority) == 1:
                    hint_x1, hint_y1, hint_value1 = first_priority[0][0][0], first_priority[0][0][1], first_priority[0][0][2]
                    next_hint_x1, next_hint_y1, next_hint_value1 = first_priority[0][1][0], first_priority[0][1][1], first_priority[0][1][2]
                    moveSelfKingNextHintBlank(grid,initial_x, initial_y, initial_value, hint_x1, hint_y1, hint_value1, next_hint_x1, next_hint_y1, next_hint_value1)
                    turn = False

                elif len(first_priority) > 1:
                    index = 0
                    final_separate_hints = [None, None, 0, None, None, 0, None, None, 0, None, None, 0]
                    final_separate_next_hints = [None, None, 0, None, None, 0, None, None, 0, None, None, 0]
                    for i in range(len(first_priority)):
                        for j in range(3):
                            final_separate_hints[index] = first_priority[i][0][j]
                            final_separate_next_hints[index] = first_priority[i][1][j]
                            index+=1
                    print(final_separate_hints)
                    print(final_separate_next_hints)
                    hint_x1, hint_y1, hint_value1, hint_x2, hint_y2, hint_value2, hint_x3, hint_y3, hint_value3, hint_x4, hint_y4, hint_value4 = final_separate_hints[0], final_separate_hints[1], final_separate_hints[2], final_separate_hints[3], final_separate_hints[4], final_separate_hints[5], final_separate_hints[6], final_separate_hints[7], final_separate_hints[8], final_separate_hints[9], final_separate_hints[10], final_separate_hints[11],
                    next_hint_x1, next_hint_y1, next_hint_value1, next_hint_x2, next_hint_y2, next_hint_value2, next_hint_x3, next_hint_y3, next_hint_value3, next_hint_x4, next_hint_y4, next_hint_value4  = final_separate_next_hints[0], final_separate_next_hints[1], final_separate_next_hints[2], final_separate_next_hints[3], final_separate_next_hints[4], final_separate_next_hints[5], final_separate_next_hints[6], final_separate_next_hints[7], final_separate_next_hints[8], final_separate_next_hints[9], final_separate_next_hints[10], final_separate_next_hints[11],

                    moveSelfKingNextHintBlank(grid, initial_x, initial_y, initial_value, hint_x1,hint_y1, hint_value1, next_hint_x1, next_hint_y1,next_hint_value1)
                    keep = False
                    turn = False

                elif len(second_priority)==1:
                    hint_x1, hint_y1, hint_value1 = second_priority[0][0], second_priority[0][1], second_priority[0][2]
                    moveSelfKingHintBlank(grid, initial_x, initial_y, initial_value, hint_x1, hint_y1, hint_value1)
                    turn = False

                elif len(second_priority) > 1:
                    index=0
                    final_separate_hints = [None, None, 0, None, None, 0, None, None, 0, None, None, 0]
                    for i in range(len(second_priority)):
                        for j in range(3):
                            final_separate_hints[index] = second_priority[i][j]
                            index+=1
                    print(final_separate_hints)
                    hint_x1, hint_y1, hint_value1, hint_x2, hint_y2, hint_value2, hint_x3, hint_y3, hint_value3, hint_x4, hint_y4, hint_value4 = final_separate_hints[0], final_separate_hints[1], final_separate_hints[2], final_separate_hints[3], final_separate_hints[4], final_separate_hints[5], final_separate_hints[6], final_separate_hints[7], final_separate_hints[8], final_separate_hints[9], final_separate_hints[10], final_separate_hints[11],

                    moveSelfKingHintBlank(grid, initial_x, initial_y, initial_value, hint_x1, hint_y1,hint_value1)
                    turn = False


            elif initial_value == self[0]: #or initial_value == self[1]



                print("self turn")
                hint_value1, hint_value2, hint_value3, hint_value4 = 0, 0, 0, 0
                hint_x1, hint_y1, hint_x2, hint_y2, hint_x3, hint_y3, hint_x4, hint_y4, hint_value1, hint_value2, hint_value3, hint_value4 = getSeparateHints(grid, initial_x, initial_y, initial_value, hint_x1, hint_y1, hint_x2, hint_y2, hint_x3, hint_y3, hint_x4, hint_y4, hint_value1, hint_value2, hint_value3, hint_value4)

                next_hint_x1, next_hint_y1, next_hint_value1 = get_hint_next_left(grid, hint_x1, hint_y1, initial_value)
                next_hint_x2, next_hint_y2, next_hint_value2 = get_hint_next_right(grid, hint_x2, hint_y2,initial_value)

                print("next hint 1: ", next_hint_x1, next_hint_y1, next_hint_value1)
                print("next hint 2: ",next_hint_x2, next_hint_y2, next_hint_value2)

                print(hint_value1, hint_value2, hint_value3, hint_value4)


                # hint1 and hint2 are blank
                if hint_value1 == 3 and hint_value2 == 3:
                    print("both blank")

                    moveSelfHintBlank(grid, initial_x, initial_y, initial_value, hint_x1, hint_y1, hint_value1)
                    hint_x1, hint_y1, hint_value1 = None, None, 0
                    turn = False

                #hint1 and hint2 are not blank
                elif hint_value1!=3 and hint_value2!=3 and hint_value1!=0 and hint_value2!=0 :
                    print("self both are gots")
                    if hint_value1 == self[0] and hint_value2 == self[0]:
                        print("donon self")
                        pass
                    elif hint_value1 == self[1] and hint_value2 == self[1]:
                        print("donon self")
                        pass
                    elif hint_value1 == self[0] and hint_value2 == self[1]:
                        print("donon self")
                        pass
                    elif hint_value1 == self[1] and hint_value2 == self[0]:
                        print("donon self")
                        pass
                    elif next_hint_value1 != 3 and next_hint_value2 != 3:
                        print("next hint khali nai hain")
                        pass

                        # checking alternate self and other(when both hints are not blank)
                    # if left is other and right is self
                    elif hint_value1 == other[0] and next_hint_value1 == 3 and hint_value2 != 3 and next_hint_value2 != 3:
                        moveSelfNextHintBlank(grid, initial_x, initial_y, initial_value, hint_x1, hint_y1,hint_value1, next_hint_x1, next_hint_y1, next_hint_value1)
                        turn = False


                    elif hint_value1 == other[1] and next_hint_value1 == 3 and hint_value2 != 3 and next_hint_value2 != 3:
                        moveSelfNextHintBlank(grid, initial_x, initial_y, initial_value, hint_x1, hint_y1,hint_value1, next_hint_x1, next_hint_y1, next_hint_value1)
                        turn = False

                    elif hint_value2 == self[0] and next_hint_value1 == 3:
                        if hint_value1 == other[0] or hint_value1 == other[1]:
                            moveSelfNextHintBlank(grid, initial_x, initial_y, initial_value, hint_x1, hint_y1,hint_value1, next_hint_x1, next_hint_y1, next_hint_value1)
                            turn = False

                    elif hint_value2 == self[1] and next_hint_value1 == 3:
                        if hint_value1 == other[0] or hint_value1 == other[1]:
                            moveSelfNextHintBlank(grid, initial_x, initial_y, initial_value, hint_x1, hint_y1,hint_value1, next_hint_x1, next_hint_y1, next_hint_value1)
                            turn = False

                    # if right is other and left is self
                    elif hint_value2 == other[0] and next_hint_value2 == 3 and hint_value1 != 3 and next_hint_value1 != 3:
                        moveSelfNextHintBlank(grid, initial_x, initial_y, initial_value, hint_x2, hint_y2,hint_value2, next_hint_x2, next_hint_y2, next_hint_value2)
                        turn = False

                    elif hint_value2 == other[1] and next_hint_value2 == 3 and hint_value1 != 3 and next_hint_value1 != 3:
                        moveSelfNextHintBlank(grid, initial_x, initial_y, initial_value, hint_x2, hint_y2,hint_value2, next_hint_x2, next_hint_y2, next_hint_value2)
                        turn = False

                    elif hint_value1 == self[0] and next_hint_value2 == 3:
                        if hint_value2 == other[0] or hint_value2 == other[1]:
                            moveSelfNextHintBlank(grid, initial_x, initial_y, initial_value, hint_x2, hint_y2,hint_value2, next_hint_x2, next_hint_y2, next_hint_value2)
                            turn = False

                    elif hint_value1 == self[1] and next_hint_value2 == 3:
                        if hint_value2 == other[0] or hint_value2 == other[1]:
                            moveSelfNextHintBlank(grid, initial_x, initial_y, initial_value, hint_x2, hint_y2,hint_value2, next_hint_x2, next_hint_y2, next_hint_value2)
                            turn = False

                    elif next_hint_value1 == 3 and next_hint_value2 == 3:
                        print("next hints donon khali hain")

                        moveSelfNextHintBlank(grid, initial_x, initial_y, initial_value, hint_x1, hint_y1, hint_value1, next_hint_x1, next_hint_y1, next_hint_value1)
                        hide_image(next_hint_x2, next_hint_y2)
                        turn = False

                elif hint_value1 == 3 or hint_value1 == 0 :
                    print("self value 1 is blank khali hai")
                    #if hint_value1 is blank
                    if hint_value2!=3 and next_hint_value2!=3:
                        moveSelfHintBlank(grid, initial_x, initial_y, initial_value, hint_x1, hint_y1, hint_value1)
                        hint_x1, hint_y1, hint_value1 = None, None, 0
                        turn = False

                    elif hint_value2 == self[0]:
                        moveSelfHintBlank(grid, initial_x, initial_y, initial_value, hint_x1, hint_y1, hint_value1)
                        hint_x1, hint_y1, hint_value1 = None, None, 0
                        turn = False

                    elif hint_value2 == self[1]:
                        moveSelfHintBlank(grid, initial_x, initial_y, initial_value, hint_x1, hint_y1, hint_value1)
                        hint_x1, hint_y1, hint_value1 = None, None, 0
                        turn = False

                    elif hint_value1 == 0 and hint_value2==3:
                        moveSelfHintBlank(grid, initial_x, initial_y, initial_value, hint_x2, hint_y2, hint_value2)
                        hint_x1, hint_y1, hint_value1 = None, None, 0
                        turn = False

                    # hint1 is blank and next hint 2 is also blank
                    elif hint_value2 != 3 and next_hint_value2 == 3:
                        if hint_value2 == other[0] or hint_value2 == other[1]:
                            moveSelfNextHintBlank(grid, initial_x, initial_y, initial_value, hint_x2, hint_y2, hint_value2, next_hint_x2, next_hint_y2, next_hint_value2)
                            hide_image(hint_x1, hint_y1)
                            # keep = False
                            turn = False

                elif hint_value2 == 3 or hint_value2 == 0:
                    # if hint_value2 is blank
                    if hint_value1 != 3 and next_hint_value1 != 3:
                        moveSelfHintBlank(grid, initial_x, initial_y, initial_value, hint_x2, hint_y2, hint_value2)
                        hint_x1, hint_y1, hint_value1 = None, None, 0
                        turn = False
                    elif hint_value1 == self[0]:
                        moveSelfHintBlank(grid, initial_x, initial_y, initial_value, hint_x2, hint_y2, hint_value2)
                        hint_x1, hint_y1, hint_value1 = None, None, 0
                        turn = False
                    elif hint_value1 == self[1]:
                        moveSelfHintBlank(grid, initial_x, initial_y, initial_value, hint_x2, hint_y2, hint_value2)
                        hint_x1, hint_y1, hint_value1 = None, None, 0
                        turn = False

                    # hint2 is blank and next hint 1 is also blank
                    elif hint_value1 != 3 and next_hint_value1 == 3:
                        if hint_value1 == other[0] or hint_value1 == other[1]:
                            moveSelfNextHintBlank(grid, initial_x, initial_y, initial_value, hint_x1, hint_y1,hint_value1, next_hint_x1, next_hint_y1, next_hint_value1)
                            hide_image(hint_x2, hint_y2)
                            # keep = False
                            turn = False


            print("self end")
            # hide_image_if_blank(grid, hint_x1, hint_y1)
            # hide_image_if_blank(grid, hint_x2, hint_y2)
            # hide_image_if_blank(grid, hint_x3, hint_y3)
            # hide_image_if_blank(grid, hint_x4, hint_y4)
            clock.tick(30)

        elif turn == False:

            if event.type == pygame.MOUSEBUTTONDOWN:
                print("other turn")

                initial_x, initial_y = get_indexes()
                initial_value = grid[initial_x][initial_y]

                print("initials", initial_x, initial_y, initial_value)

                if initial_value == 3 or initial_value == 0:
                    pass

                elif initial_value == other[1]:
                    hints = get_hints(grid, initial_x, initial_y, initial_value)
                    print(hints)
                    next_hints = get_hint_next_list(grid, hints)
                    print(next_hints)

                    for i in range(4):                           #no of hints of king =4
                        if hints[i][-1] !=3 and next_hints[i][-1] == 3:
                            if hints[i][-1] == self[0] or hints[i][-1] == self[1]:
                                first_priority.append([hints[i],next_hints[i]])
                        elif hints[i][-1] == 3:
                            second_priority.append(hints[i])

                    print("first priority", first_priority)
                    print("Second priority", second_priority)

                    if len(first_priority) == 1:
                        hint_x1, hint_y1, hint_value1 = first_priority[0][0][0], first_priority[0][0][1], first_priority[0][0][2]
                        next_hint_x1, next_hint_y1, next_hint_value1 = first_priority[0][1][0], first_priority[0][1][1], first_priority[0][1][2]
                        moveOtherKingNextHintBlank(grid,initial_x, initial_y, initial_value, hint_x1, hint_y1, hint_value1, next_hint_x1, next_hint_y1, next_hint_value1)
                        turn = True

                    elif len(first_priority) > 1:
                        index = 0
                        final_separate_hints = [None, None, 0, None, None, 0, None, None, 0, None, None, 0]
                        final_separate_next_hints = [None, None, 0, None, None, 0, None, None, 0, None, None, 0]
                        for i in range(len(first_priority)):
                            for j in range(3):
                                final_separate_hints[index] = first_priority[i][0][j]
                                final_separate_next_hints[index] = first_priority[i][1][j]
                                index+=1
                        print(final_separate_hints)
                        print(final_separate_next_hints)
                        hint_x1, hint_y1, hint_value1, hint_x2, hint_y2, hint_value2, hint_x3, hint_y3, hint_value3, hint_x4, hint_y4, hint_value4 = final_separate_hints[0], final_separate_hints[1], final_separate_hints[2], final_separate_hints[3], final_separate_hints[4], final_separate_hints[5], final_separate_hints[6], final_separate_hints[7], final_separate_hints[8], final_separate_hints[9], final_separate_hints[10], final_separate_hints[11],
                        next_hint_x1, next_hint_y1, next_hint_value1, next_hint_x2, next_hint_y2, next_hint_value2, next_hint_x3, next_hint_y3, next_hint_value3, next_hint_x4, next_hint_y4, next_hint_value4  = final_separate_next_hints[0], final_separate_next_hints[1], final_separate_next_hints[2], final_separate_next_hints[3], final_separate_next_hints[4], final_separate_next_hints[5], final_separate_next_hints[6], final_separate_next_hints[7], final_separate_next_hints[8], final_separate_next_hints[9], final_separate_next_hints[10], final_separate_next_hints[11],

                        hint_image(next_hint_x1, next_hint_y1)
                        hint_image(next_hint_x2, next_hint_y2)
                        hint_image(next_hint_x3, next_hint_y3)
                        hint_image(next_hint_x4, next_hint_y4)

                        while keep == True:
                            for event4 in pygame.event.get():
                                if event4.type == pygame.MOUSEBUTTONDOWN:
                                    tab_hint_x, tab_hint_y = get_indexes()
                                    tab_hint_value = grid[tab_hint_x][tab_hint_y]

                                    if tab_hint_x == next_hint_x1 and tab_hint_y == next_hint_y1 and tab_hint_value == 3:
                                        moveOtherKingNextHintBlank(grid, initial_x, initial_y, initial_value, hint_x1,hint_y1, hint_value1, tab_hint_x, tab_hint_y,tab_hint_value)
                                        keep = False
                                        turn = True

                                    elif tab_hint_x == next_hint_x2 and tab_hint_y == next_hint_y2 and tab_hint_value == 3:
                                        moveOtherKingNextHintBlank(grid, initial_x, initial_y, initial_value, hint_x2,hint_y2, hint_value2, tab_hint_x, tab_hint_y,tab_hint_value)
                                        keep = False
                                        turn = True

                                    elif tab_hint_x == next_hint_x3 and tab_hint_y == next_hint_y3 and tab_hint_value == 3:
                                        moveOtherKingNextHintBlank(grid, initial_x, initial_y, initial_value, hint_x3, hint_y3, hint_value3, tab_hint_x, tab_hint_y,tab_hint_value)
                                        keep = False
                                        turn = True

                                    elif tab_hint_x == next_hint_x4 and tab_hint_y == next_hint_y4 and tab_hint_value == 3:
                                        moveOtherKingNextHintBlank(grid, initial_x, initial_y, initial_value, hint_x4,hint_y4, hint_value4, tab_hint_x, tab_hint_y,tab_hint_value)
                                        keep = False
                                        turn = True

                    elif len(second_priority)==1:
                        hint_x1, hint_y1, hint_value1 = second_priority[0][0], second_priority[0][1], second_priority[0][2]
                        moveOtherKingHintBlank(grid, initial_x, initial_y, initial_value, hint_x1, hint_y1, hint_value1)
                        turn = True

                    elif len(second_priority) > 1:
                        index=0
                        final_separate_hints = [None, None, 0, None, None, 0, None, None, 0, None, None, 0]
                        for i in range(len(second_priority)):
                            for j in range(3):
                                final_separate_hints[index] = second_priority[i][j]
                                index+=1
                        print(final_separate_hints)
                        hint_x1, hint_y1, hint_value1, hint_x2, hint_y2, hint_value2, hint_x3, hint_y3, hint_value3, hint_x4, hint_y4, hint_value4 = final_separate_hints[0], final_separate_hints[1], final_separate_hints[2], final_separate_hints[3], final_separate_hints[4], final_separate_hints[5], final_separate_hints[6], final_separate_hints[7], final_separate_hints[8], final_separate_hints[9], final_separate_hints[10], final_separate_hints[11],


                        hint_image(hint_x1, hint_y1)
                        hint_image(hint_x2, hint_y2)
                        hint_image(hint_x3, hint_y3)
                        hint_image(hint_x4, hint_y4)

                        while keep == True:
                            for event1 in pygame.event.get():
                                if event1.type == pygame.MOUSEBUTTONDOWN:
                                    tab_hint_x, tab_hint_y = get_indexes()
                                    tab_hint_value = grid[tab_hint_x][tab_hint_y]

                                    if tab_hint_x == hint_x1 and tab_hint_y == hint_y1 and tab_hint_value == 3:
                                        moveOtherKingHintBlank(grid, initial_x, initial_y, initial_value, tab_hint_x, tab_hint_y,tab_hint_value)
                                        keep = False
                                        turn = True

                                    elif tab_hint_x == hint_x2 and tab_hint_y == hint_y2 and tab_hint_value == 3:
                                        moveOtherKingHintBlank(grid, initial_x, initial_y, initial_value, tab_hint_x, tab_hint_y,tab_hint_value)
                                        keep = False
                                        turn = True

                                    elif tab_hint_x == hint_x3 and tab_hint_y == hint_y3 and tab_hint_value == 3:
                                        moveOtherKingHintBlank(grid, initial_x, initial_y, initial_value, tab_hint_x, tab_hint_y,tab_hint_value)
                                        keep = False
                                        turn = True

                                    elif tab_hint_x == hint_x4 and tab_hint_y == hint_y4 and tab_hint_value == 3:
                                        moveOtherKingHintBlank(grid, initial_x, initial_y, initial_value, tab_hint_x, tab_hint_y,tab_hint_value)
                                        keep = False
                                        turn = True


                elif initial_value == other[0]:  # or initial_value == self[1]
                    hint_value1, hint_value2, hint_value3, hint_value4 = 0, 0, 0, 0
                    hint_x1, hint_y1, hint_x2, hint_y2, hint_x3, hint_y3, hint_x4, hint_y4, hint_value1, hint_value2, hint_value3, hint_value4 = getSeparateHints(grid, initial_x, initial_y, initial_value, hint_x1, hint_y1, hint_x2, hint_y2, hint_x3, hint_y3,hint_x4, hint_y4, hint_value1, hint_value2, hint_value3, hint_value4)

                    next_hint_x1, next_hint_y1, next_hint_value1 = get_hint_next_left(grid, hint_x1, hint_y1,initial_value)
                    next_hint_x2, next_hint_y2, next_hint_value2 = get_hint_next_right(grid, hint_x2, hint_y2,initial_value)

                    print("next hint 1: ", next_hint_x1, next_hint_y1, next_hint_value1)
                    print("next hint 2: ", next_hint_x2, next_hint_y2, next_hint_value2)

                    print(hint_value1, hint_value2, hint_value3, hint_value4)

                    # hint1 and hint2 are blank
                    if hint_value1 == 3 and hint_value2 == 3:

                        if hint_value1 == 3:
                            hint_image(hint_x1, hint_y1)
                            pygame.display.update()
                        if hint_value2 == 3:
                            hint_image(hint_x2, hint_y2)
                            pygame.display.update()

                        while keep == True:
                            for event5 in pygame.event.get():
                                if event5.type == pygame.MOUSEBUTTONDOWN:

                                    tab_hint_x, tab_hint_y = get_indexes()
                                    tab_hint_value = grid[tab_hint_x][tab_hint_y]

                                    if tab_hint_x == hint_x1 and tab_hint_y == hint_y1 and tab_hint_value == 3:
                                        moveOtherHintBlank(grid, initial_x, initial_y, initial_value, tab_hint_x,tab_hint_y, tab_hint_value)
                                        hint_x1, hint_y1, hint_value1 = None, None, 0
                                        keep = False
                                        turn = True

                                    elif tab_hint_x == hint_x2 and tab_hint_y == hint_y2 and tab_hint_value == 3:
                                        moveOtherHintBlank(grid, initial_x, initial_y, initial_value, tab_hint_x,tab_hint_y, tab_hint_value)
                                        hint_x2, hint_y2, hint_value2 = None, None, 0
                                        keep = False
                                        turn = True

                    # hint1 and hint2 are not blank
                    elif hint_value1 != 3 and hint_value2 != 3 and hint_value1 != 0 and hint_value2 != 0:
                        if hint_value1 == other[0] and hint_value2 == other[0]:
                            print("donon other")
                            pass
                        elif hint_value1 == other[1] and hint_value2 == other[1]:
                            print("donon other")
                            pass
                        elif hint_value1 == other[0] and hint_value2 == other[1]:
                            print("donon other")
                            pass
                        elif hint_value1 == other[1] and hint_value2 == other[0]:
                            print("donon other")
                            pass
                        elif next_hint_value1 != 3 and next_hint_value2 != 3:
                            print("next hint khali nai hain")
                            pass

                        elif hint_value1 == self[0] and next_hint_value1 == 3 and hint_value2 != 3 and next_hint_value2 != 3:
                            moveOtherNextHintBlank(grid, initial_x, initial_y, initial_value, hint_x1, hint_y1,hint_value1, next_hint_x1, next_hint_y1, next_hint_value1)
                            turn = True

                        elif hint_value1 == self[1] and next_hint_value1 == 3 and hint_value2 != 3 and next_hint_value2 != 3:
                            moveOtherNextHintBlank(grid, initial_x, initial_y, initial_value, hint_x1, hint_y1,hint_value1, next_hint_x1, next_hint_y1, next_hint_value1)
                            turn = True

                        elif hint_value2 == other[0] and next_hint_value1 == 3:
                            if hint_value1 == self[0] or hint_value1 == self[1]:
                                moveOtherNextHintBlank(grid, initial_x, initial_y, initial_value, hint_x1, hint_y1,hint_value1, next_hint_x1, next_hint_y1, next_hint_value1)
                                turn = True

                        elif hint_value2 == other[1] and next_hint_value1 == 3:
                            if hint_value1 == self[0] or hint_value1 == self[1]:
                                moveOtherNextHintBlank(grid, initial_x, initial_y, initial_value, hint_x1, hint_y1,hint_value1, next_hint_x1, next_hint_y1, next_hint_value1)
                                turn = True

                        # if right is self and left other
                        elif hint_value2 == self[0] and next_hint_value2 == 3 and hint_value1 != 3 and next_hint_value1 != 3:
                            moveOtherNextHintBlank(grid, initial_x, initial_y, initial_value, hint_x2, hint_y2,hint_value2, next_hint_x2, next_hint_y2, next_hint_value2)
                            turn = True

                        elif hint_value2 == self[1] and next_hint_value2 == 3 and hint_value1 != 3 and next_hint_value1 != 3:
                            moveOtherNextHintBlank(grid, initial_x, initial_y, initial_value, hint_x2, hint_y2,hint_value2, next_hint_x2, next_hint_y2, next_hint_value2)
                            turn = True

                        elif hint_value1 == other[0] and next_hint_value2 == 3:
                            if hint_value2 == self[0] or hint_value2 == self[1]:
                                moveOtherNextHintBlank(grid, initial_x, initial_y, initial_value, hint_x2, hint_y2,hint_value2, next_hint_x2, next_hint_y2, next_hint_value2)
                                turn = True

                        elif hint_value1 == other[1] and next_hint_value2 == 3:
                            if hint_value2 == self[0] or hint_value2 == self[1]:
                                moveOtherNextHintBlank(grid, initial_x, initial_y, initial_value, hint_x2, hint_y2,hint_value2, next_hint_x2, next_hint_y2, next_hint_value2)
                                turn = True

                        elif next_hint_value1 == 3 and next_hint_value2 == 3:
                            print("next hints donon khali hain")
                            hint_image(next_hint_x1, next_hint_y1)
                            hint_image(next_hint_x2, next_hint_y2)
                            pygame.display.update()

                            while keep == True:
                                for event6 in pygame.event.get():
                                    if event6.type == pygame.MOUSEBUTTONDOWN:

                                        tab_hint_x, tab_hint_y = get_indexes()
                                        tab_hint_value = grid[tab_hint_x][tab_hint_y]

                                        # if tab_hint_value != next_hint_value1 or tab_hint_value != next_hint_value2:
                                        #     pass
                                        if tab_hint_x == next_hint_x1 and tab_hint_y == next_hint_y1 and tab_hint_value == 3:
                                            moveOtherNextHintBlank(grid, initial_x, initial_y, initial_value, hint_x1,hint_y1, hint_value1, tab_hint_x, tab_hint_y,tab_hint_value)
                                            hide_image(next_hint_x2, next_hint_y2)
                                            keep = False
                                            turn = True
                                        elif tab_hint_x == next_hint_x2 and tab_hint_y == next_hint_y2 and tab_hint_value == 3:
                                            moveOtherNextHintBlank(grid, initial_x, initial_y, initial_value, hint_x2,hint_y2, hint_value2, tab_hint_x, tab_hint_y,tab_hint_value)
                                            hide_image(next_hint_x1, next_hint_y1)
                                            keep = False
                                            turn = True


                    elif hint_value1 == 3 or hint_value1 == 0:
                        print("other khali hai")
                        # if hint_value1 is blank
                        if hint_value2 != 3 and next_hint_value2 != 3:
                            moveOtherHintBlank(grid, initial_x, initial_y, initial_value, hint_x1, hint_y1, hint_value1)
                            hint_x1, hint_y1, hint_value1 = None, None, 0
                            turn = True
                        elif hint_value2 == other[0]:
                            moveOtherHintBlank(grid, initial_x, initial_y, initial_value, hint_x1, hint_y1, hint_value1)
                            hint_x1, hint_y1, hint_value1 = None, None, 0
                            turn = True
                        elif hint_value2 == other[1]:
                            moveOtherHintBlank(grid, initial_x, initial_y, initial_value, hint_x1, hint_y1, hint_value1)
                            hint_x1, hint_y1, hint_value1 = None, None, 0
                            turn = True

                        elif hint_value1 == 0 and hint_value2==3:
                            moveOtherHintBlank(grid, initial_x, initial_y, initial_value, hint_x2, hint_y2, hint_value2)
                            hint_x1, hint_y1, hint_value1 = None, None, 0
                            turn = True

                        # hint1 is blank and next hint 2 is also blank
                        elif hint_value2 != 3 and next_hint_value2 == 3:
                            if hint_value2 == self[0] or hint_value2 == self[1]:
                                moveOtherNextHintBlank(grid, initial_x, initial_y, initial_value, hint_x2, hint_y2,hint_value2, next_hint_x2, next_hint_y2, next_hint_value2)
                                hide_image(hint_x1, hint_y1)
                                turn = True


                    elif hint_value2 == 3 or hint_value2 == 0:
                        print("value 2 khali hai")
                        # if hint_value2 is blank
                        if hint_value1 != 3 and next_hint_value1 != 3:
                            print("condition 1")
                            moveOtherHintBlank(grid, initial_x, initial_y, initial_value, hint_x2, hint_y2, hint_value2)
                            hint_x1, hint_y1, hint_value1 = None, None, 0
                            turn = True
                        elif hint_value1 == other[0]:
                            print("condition 2")
                            moveOtherHintBlank(grid, initial_x, initial_y, initial_value, hint_x2, hint_y2, hint_value2)
                            hint_x1, hint_y1, hint_value1 = None, None, 0
                            turn = True
                        elif hint_value1 == other[1]:
                            print("condition 3")
                            moveOtherHintBlank(grid, initial_x, initial_y, initial_value, hint_x2, hint_y2, hint_value2)
                            hint_x1, hint_y1, hint_value1 = None, None, 0
                            turn = True

                        # hint2 is blank and next hint 1 is also blank
                        elif hint_value1 != 3 and next_hint_value1 == 3:
                            if hint_value1 == self[0] or hint_value1 == self[1]:
                                moveOtherNextHintBlank(grid, initial_x, initial_y, initial_value, hint_x1, hint_y1,hint_value1, next_hint_x1, next_hint_y1, next_hint_value1)
                                hide_image(hint_x2, hint_y2)
                                turn = True


                    print("other end")

            hide_image_if_blank(grid, hint_x1, hint_y1)
            hide_image_if_blank(grid, hint_x2, hint_y2)
            hide_image_if_blank(grid, hint_x3, hint_y3)
            hide_image_if_blank(grid, hint_x4, hint_y4)

            hide_image_if_blank(grid, next_hint_x1, next_hint_y1)
            hide_image_if_blank(grid, next_hint_x2, next_hint_y2)
            hide_image_if_blank(grid, next_hint_x3, next_hint_y3)
            hide_image_if_blank(grid, next_hint_x4, next_hint_y4)



    hint1, hint2, hint1, hint2 = 0, 0, 0, 0

    hints = 0
    next_hints = []
    first_priority = []
    second_priority = []

    next_hint_x1, next_hint_y1, next_hint_x2, next_hint_y2, next_hint_value1, next_hint_value2 = None, None, None, None, 0, 0
    next_hint_x3, next_hint_y3, next_hint_x4, next_hint_y4, next_hint_value3, next_hint_value4 = None, None, None, None, 0, 0
    hint_x1, hint_y1, hint_x2, hint_y2, hint_x3, hint_y3, hint_x4, hint_y4 = None, None, None, None, None, None, None, None
    hint_value1, hint_value2, hint_value3, hint_value4 = 0, 0, 0, 0
    keep = True

    clock.tick(30)

    pygame.display.flip()


# pygame.quit()