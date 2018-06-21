import pygame, time, random
from pygame.locals import *

# Globals

SCREEN_W_H = 700,700

FPS = 200 # Uoc mo cua moi game thu ^^!

# Kiem soat toc do cua Ran
MOVE_SPEED = 1
NUM_FRAMES_TO_DELAY_MOVE = 10

APPLE_COLOR = pygame.Color(255, 0, 0)  # mau do
SNAKE_COLOR = pygame.Color(0, 255, 0)  # Mau xanh la cay

SQUARE_BLOCK_SIZE = 20


class Block:

    def __init__(self):
        self.color = pygame.Color(0, 0, 0)  # Mau Trang
        self.squareSize = SQUARE_BLOCK_SIZE
        self.pos = [0, 0]  # Default pos

    def draw(self, screen):
        rect = Rect(self.pos[0], self.pos[1], SQUARE_BLOCK_SIZE, SQUARE_BLOCK_SIZE)
        screen.fill(self.color, rect)


class BodySegment(Block):

    def __init__(self, pos):
        Block.__init__(self)
        self.color = pygame.Color(0, 255, 0)
        self.pos = pos

    def move(self, newPos):
        self.pos = newPos


class WallSegment(Block):

    def __init__(self, pos):
        Block.__init__(self)
        self.color = pygame.Color(200, 200, 200)
        self.pos = pos


class Apple(Block):

    def __init__(self):
        Block.__init__(self)
        self.color = pygame.Color(255, 0, 0)
        self.randomize()

    # Place apple in random block position
    def randomize(self):
        for i, widthOrHeight in enumerate(self.pos):
            self.pos[i] = random.choice(range(SQUARE_BLOCK_SIZE, SCREEN_W_H[0] - SQUARE_BLOCK_SIZE, SQUARE_BLOCK_SIZE))


class Chainable:

    def draw(self, screen):
        for seg in self.segments:
            seg.draw(screen)


class Wall(Chainable):

    def __init__(self):
        self.segments = []

        # Tao Wall

        for x in range(0, SCREEN_W_H[0], SQUARE_BLOCK_SIZE):
            self.segments.append(WallSegment([x, 0]))
            self.segments.append(WallSegment([x, SCREEN_W_H[1] - SQUARE_BLOCK_SIZE]))

        for y in range(SQUARE_BLOCK_SIZE, SCREEN_W_H[1] - SQUARE_BLOCK_SIZE, SQUARE_BLOCK_SIZE):
            self.segments.append(WallSegment([0, y]))
            self.segments.append(WallSegment([SCREEN_W_H[1] - SQUARE_BLOCK_SIZE, y]))

    def hit_Wall(self, snake):

        rect1 = Rect(snake.head.pos[0], snake.head.pos[1], SQUARE_BLOCK_SIZE, SQUARE_BLOCK_SIZE)

        for seg in self.segments:
            rect2 = Rect(seg.pos[0], seg.pos[1], SQUARE_BLOCK_SIZE, SQUARE_BLOCK_SIZE)
            if colide(rect1, rect2):
                return True
        return False


class Snake(Chainable):

    def __init__(self):
        self.direction = 'right'  # mac dinh di chuyen ban dua tu Phai qua trai
        self.moveDist = SQUARE_BLOCK_SIZE * MOVE_SPEED
        self.segments = []
        self.size = 0
        for i in range(2):
            # bat dau di chuyen tu vi tri goc trai man hinh
            if i == 0:
                self.segments.append(BodySegment([SQUARE_BLOCK_SIZE, 200]))  # Bat dau voi con Ran co 2 don vi
                self.head = self.segments[0]
            else:
                self.segments.append(BodySegment([0, 200]))

    def changeDir(self, direction):

        if self.direction == 'right' and direction == 'left':
            pass
        elif self.direction == 'left' and direction == 'right':
            pass
        elif self.direction == 'up' and direction == 'down':
            pass
        elif self.direction == 'down' and direction == 'up':
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
        elif self.direction == 'left':
            newHeadPos = [head.pos[0] - self.moveDist, head.pos[1]]
        else:
            newHeadPos = [head.pos[0] + self.moveDist, head.pos[1]]

        # Luu để tẹo nữa thêm segment vào đuôi rắn
        self.tailLastPos = self.segments[segmentsLen - 1].pos

        # đặt mỗi segments lên vị trí của đường đi mới( đè lên đường cho giống con rắn đang bò)
        for i in range(segmentsLen - 1, 0, -1):
            self.segments[i].move(self.segments[i - 1].pos)

        # Dat dau ran len vi tri di chuyen moi
        self.segments[0].move(newHeadPos)

    def addSegment(self):

        self.segments.append(BodySegment(self.tailLastPos))
        self.size += 1


def colide(rect1, rect2):
    if rect1.x == rect2.x and rect1.y == rect2.y:
        return True
    else:
        return False


# Di chuyen Ran dua tren String "direction"
# dung 'up', 'down', 'left' va 'right'
def changeDir(direction, snake):
    snake.changeDir(direction)






def setupScreen():
    pygame.init()

    screen = pygame.display.set_mode(SCREEN_W_H)

    return screen


def main():
    screen = setupScreen()

    fillRect = Rect(0, 0, SCREEN_W_H[0], SCREEN_W_H[1])

    screen.fill((255, 0, 0))








    wall = Wall()

    snake = Snake()

    apple = Apple()

    # Main Loop

    running = True
    framesSinceLastMove = 0
    while (running):

        time.sleep(1.0 / FPS)

        event = pygame.event.poll()

        direction = ''

        if event.type == QUIT:
            running = False
            continue
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                changeDir('up', snake)
            elif event.key == K_DOWN:
                changeDir('down', snake)
            elif event.key == K_LEFT:
                changeDir('left', snake)
            elif event.key == K_RIGHT:
                changeDir('right', snake)
            elif event.key == K_ESCAPE:
                running = False
                continue

        # Draw ra man hinh
        screen.fill((0, 0, 0))
        apple.draw(screen)
        snake.draw(screen)

        wall.draw(screen)

        if framesSinceLastMove == NUM_FRAMES_TO_DELAY_MOVE:
            snake.move()
            framesSinceLastMove = 0

        # check va cham
        headRect = Rect(snake.head.pos[0], snake.head.pos[1], SQUARE_BLOCK_SIZE, SQUARE_BLOCK_SIZE)
        appleRect = Rect(apple.pos[0], apple.pos[1], SQUARE_BLOCK_SIZE, SQUARE_BLOCK_SIZE)

        if colide(headRect, appleRect):
            apple = Apple()  # Tao them mot qua tao moi
            snake.addSegment()

        if snake.hit_Tail():
            # CHeck va cham voi duoi Ran

            pygame.display.update()
            time.sleep(3)
            running = False
            continue

        if wall.hit_Wall(snake):

            pygame.display.update()
            time.sleep(3)
            running = False
            continue



        pygame.display.update()

        framesSinceLastMove += 1


if __name__ == '__main__':
    main()