import pygame, time, random, math
from pygame.locals import *


SCREEN_W_H = 700,700
FPS = 200
MOVE_SPEED = 1
NUM_FRAMES_TO_DELAY_MOVE = 1 #cai nay vao game chinh lai cho hop li hon

SQUARE_BLOCK_SIZE = 50
RED = (255,0,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
GREEN = (0,255,0)
YELLOW = (255,255,255)

APPLE_COLOR = pygame.Color(RED)  # Red
SNAKE_COLOR = pygame.Color(BLUE)  # Blue


class Block:
    # tạo từng thành phần của thân con rắn ^^!
    def __init__(self):
        self.color = pygame.Color(WHITE)  # Default color
        self.squareSize = SQUARE_BLOCK_SIZE
        self.pos = [0, 0]  # Default pos

    def draw(self, screen):
        rect = Rect(self.pos[0], self.pos[1], SQUARE_BLOCK_SIZE, SQUARE_BLOCK_SIZE)
        screen.fill(self.color, rect)


class BodySegment(Block):
    def __init__(self, pos):
        Block.__init__(self)
        self.color = pygame.Color(GREEN)
        self.pos = pos

    def move(self, newPos):
        self.pos = newPos


class WallSegment(Block):
    def __init__(self, pos):
        Block.__init__(self)
        self.color = pygame.Color(YELLOW)
        self.pos = pos


class Apple(Block):
    def __init__(self):
        Block.__init__(self)
        self.color = pygame.Color(RED)
        self.randomize()

    # tiếp theo làm cho quả táo xuất hiện ngẫu nhiên
    def randomize(self):
        for i, WidthOrHeight in enumerate(self.pos):
            self.pos[i] = random.choice(range(SQUARE_BLOCK_SIZE, SCREEN_W_H[0] - SQUARE_BLOCK_SIZE, SQUARE_BLOCK_SIZE)


class Chainable:
    def draw(self, screen):
        for seg in self.segments:
            seg.draw(screen)


class Wall(Chainable):
    def __init__(self):
        self.segments = []

        # tạo tường

        for x in range(0, SCREEN_W_H[0], SQUARE_BLOCK_SIZE):
            self.segments.append( WallSegment([x, 0]))
            self.segments.append(WallSegment([x, SCREEN_W_H[1] - SQUARE_BLOCK_SIZE]))
        for y in range(SQUARE_BLOCK_SIZE, SCREEN_W_H[1] - SQUARE_BLOCK_SIZE, SQUARE_BLOCK_SIZE):
            self.segments.append(WallSegment([0, y]))
            self.segments.append(WallSegment([SCREEN_W_H[1] - SQUARE_BLOCK_SIZE, y]))

    def hit_Wall(self, Snake):
        rect1 = Rect(Snake.head.pos[0], Snake.head.pos[1], SQUARE_BLOCK_SIZE, SQUARE_BLOCK_SIZE)
        for seg in self.segments:
            rect2 = Rect(seg.pos[0], seg.pos[1], SQUARE_BLOCK_SIZE, SQUARE_BLOCK_SIZE)
            if colide(rect1, rect2):
                return True
        return False



class Snake(Chainable):
    def __init__(self):
        self.direction = 'right'  # mạc định con rắn sẽ di chuyển sang phải
        self.moveDist = SQUARE_BLOCK_SIZE * MOVE_SPEED  # tốc đọ di chuyển của con rắn
        self.segments = []
        self.size = 0
        for i in range(2):
            if i == 0:
                self.segments.append(BodySegment([SQUARE_BLOCK_SIZE, 200])) # bắt đầu chơi với 2 segments
            else:
                self.segments.append(BodySegment([0, 200]))

    def changeDir(self, direction):
        if self.direction == 'right' and direction == 'left':
            pass
        if self.direction == 'left' and direction == 'right':
            pass
        if self.direction == 'up' and direction == 'down':
            pass
        if self.direction == 'down' and direction == 'up':
            pass
        else:
            self.direction = direction

    def hit_Tail(self):
        for i, seg in enumerate(self.segments):
            if i == 0:
                continue
            rect1 = Rect(self.head.pos[0], self.head.pos[1], SQUARE_BLOCK_SIZE, SQUARE_BLOCK_SIZE)
            rect2 = Rect(seg.pos[0], seg.pos[1], SQUARE_BLOCK_SIZE, SQUARE_BLOCK_SIZE)
            if colide(rect1, rect2):
                return True
        return False

    def move(self):
        segmentsLen = len(self.segments)
        head = self.segments[0]

        newHeadPos = []

        if self.direction == 'up':
            newHeadPos = [head.pos[0], head.pos[1] - self.moveDist]
        elif self.direction == 'down':
            newHeadPos = [head.pos[0], head.pos[1] + self.moveDist]
        elif self.direction == "left":
            newHeadPos = [head.pos[1] - self.moveDist, head.pos[1]]
        else:
            newHeadPos = [head.pos[1] + self.moveDist, head.pos[1]]

        # lưu để tẹo nữa thêm segment vào đuôi rắn
        self.tailLastPos = self.segments[segmentsLen - 1].pos

        # đặt mỗi segments lên vị trí của đường đi mới( đè lên đường cho giống con rắn đang bò)
        for i in range(segmentsLen - 1, 0, -1):
            self.segments[i].move(self.segments[i - 1].pos)

        # Ta đặt đầu rắn lên đầu cảu vị trí di chuyên mới
        self.segments[0].move(newHeadPos)

    def addSegment(self):
        self.segments.append(BodySegment(self.tailLastPos))
        self.size += 1



def colide(rect1, rect2):
    if rect1.x == rect2.x and rect1.y == rect2.y:
        return True
    else:
        return False

#thay doi huong di cua Ran
def changeDir(direction, snake):
    snake.changeDir(direction)



