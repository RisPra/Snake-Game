import pygame
import time
import random
from pygame.locals import *
pygame.font.init()
font = pygame.font.SysFont('Lucida Console', 30)

class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((500, 500))
        bg = pygame.image.load("resources/background.png").convert()
        self.surface.blit(bg, (0, 0))
        self.snake = Snake(self.surface, 2)
        self.snake.draw()
        self.apple = Apple(50, self.surface, self.snake)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    
                    if event.key == K_UP:   
                        self.snake.move_up()
                        continue
                    
                    if event.key == K_DOWN:
                        self.snake.move_down()
                        continue
                    
                    if event.key == K_LEFT:
                        self.snake.move_left()
                        continue
                    
                    if event.key == K_RIGHT:
                        self.snake.move_right()
                        continue
                elif event.type == QUIT:
                    running = False
            
            self.snake.walk()
            if self.snake.headCollisionCheck():
                running = False
            if self.snake.boundCheck():
                running = False
            
            if self.snake.getPos() == self.apple.getPos():
                self.apple = Apple(50, self.surface, self.snake)
                self.snake.ate()
            self.apple.show()
            time.sleep(0.3)

        temp = "Your score was " + str(self.snake.length-2)
        end = font.render(temp, True, (255, 255, 255))
        self.surface.blit(end, (100, 230))
        pygame.display.flip()
        time.sleep(2)
        
class Snake:
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.snakeHead = pygame.image.load("resources/snakeHead.png").convert_alpha()
        self.snakeTail = pygame.image.load("resources/snakeTail.png").convert_alpha()
        self.snakeStraight = pygame.image.load("resources/snakeBodyStraight.png").convert_alpha()
        self.snakeTurn = pygame.image.load("resources/snakeBodyTurn.png").convert_alpha()
        self.alive = True
        self.direction = 'up'
        self.length = length
        self.side = 50
        self.x, self.y = [200]*100, [500]*100

    def draw(self):
        bg = pygame.image.load("resources/background.png").convert()
        self.parent_screen.blit(bg, (0, 0))
        
        headDirDict = {"up":0, "right": 270, "down": 180, "left":90}
        bodyDirDict = {"ur":0, "rd": 270, "dl": 180, "lu":90, "sv":0, "sh":90}
        
        for i in range(self.length):
            temp = self.segmentDirection(i)
            if i == 0:
                rotatedSnakeHead = pygame.transform.rotate(self.snakeHead, headDirDict[self.direction])
                self.parent_screen.blit(rotatedSnakeHead, (self.x[i], self.y[i]))
            elif i == self.length-1:
                rotatedSnakeTail = pygame.transform.rotate(self.snakeTail, headDirDict[self.tailDir()])
                self.parent_screen.blit(rotatedSnakeTail, (self.x[i], self.y[i]))
            elif temp[0] == "s":
                rotatedSnakeStraight = pygame.transform.rotate(self.snakeStraight, bodyDirDict[temp])
                self.parent_screen.blit(rotatedSnakeStraight, (self.x[i], self.y[i]))
            else:
                rotatedSnakeTurn = pygame.transform.rotate(self.snakeTurn, bodyDirDict[self.segmentDirection(i)])
                self.parent_screen.blit(rotatedSnakeTurn, (self.x[i], self.y[i]))
        
        score = font.render(str(self.length-2), True, (255, 255, 255))
        self.parent_screen.blit(score, (10, 10))
        pygame.display.flip()

    def segmentDirection(self, i):
        xm = self.x[i-1]
        x = self.x[i]
        xp = self.x[i+1]
        ym = self.y[i-1]
        y = self.y[i]
        yp = self.y[i+1]

        if xp == xm:
            return "sv"
        if yp == ym:
            return "sh"
        
        if xp > xm:
            if yp < ym:
                if x == xp:
                    return "dl"
                return "ur"
            if yp > ym:
                if y == yp:
                    return "lu"
                return "rd"
        if xp < xm:
            if yp < ym:
                if x == xm:
                    return "rd"
                return "lu"
            if yp > ym:
                if y == ym:
                    return "ur"
                return "dl"        

    def tailDir(self):
        i = self.length-1
        x = self.x[i]
        xp = self.x[i-1]
        y = self.y[i]
        yp = self.y[i-1]

        if x == xp:
            if yp > y:
                return "down"
            if yp < y:
                return "up"
        if y == yp:
            if xp > x:
                return "right"
            if xp < x:
                return "left"
        return "up"
            

    def move_up(self): 
        if self.direction != "down":
            self.direction = 'up'

    def move_down(self): 
        if self.direction != "up":
            self.direction = 'down'

    def move_left(self): 
        if self.direction != "right":
            self.direction = 'left'

    def move_right(self): 
        if self.direction != "left":
            self.direction = 'right'

    def walk(self):
        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        
        if self.direction == 'up':
            self.y[0] -= self.side
        elif self.direction == 'down':
            self.y[0] += self.side
        elif self.direction == 'left':
            self.x[0] -= self.side
        elif self.direction == 'right':
            self.x[0] += self.side
        
        self.draw()

    def ate(self):
        self.length+=1

    def getPos(self):
        return self.x[0], self.y[0]

    def headCollisionCheck(self):
        for i in range(self.length-1):
            if self.x[0] == self.x[i+1] and self.y[0] == self.y[i+1]:
                return True
        return False
    
    def boundCheck(self):
        if self.x[0] == 500 or self.x[0] == -50 or self.y[0]==500 or self.y[0]==-50:
            return True
        return False

class Apple:
    def __init__(self, mul, parent_screen, snake):
        self.parentScreen = parent_screen
        self.mul = mul
        self.x, self.y = snake.getPos()
        snakeX, snakeY = snake.getPos()
        while self.x == snakeX or self.y == snakeY:
            self.x, self.y = random.randint(0, 9)*mul, random.randint(0, 9)*mul
        self.show()

    def show(self):
        apple = pygame.image.load("resources/apple.png").convert_alpha()
        self.parentScreen.blit(apple, (self.x, self.y))
        pygame.display.flip()
    
    def getPos(self):
        return self.x, self.y

if __name__ == '__main__':
    game = Game()
    game.run()