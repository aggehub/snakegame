import pygame
import numpy as np
import random
import time


### 20x20 grid
GRID = pygame.image.load('grid.jpg') # 20x20 grid
WIDTH, HEIGHT = GRID.get_width(), GRID.get_height()
NUM_SQUARES = 20
GRID_SQUARE_SIZE = WIDTH/NUM_SQUARES

# ### 10x10 grid
# GRID = pygame.image.load('grid - kopia.jpg') # 20x20 grid
# WIDTH, HEIGHT = GRID.get_width(), GRID.get_height()
# NUM_SQUARES = 10
# GRID_SQUARE_SIZE = WIDTH/NUM_SQUARES

GRID = pygame.image.load('purple_grid.jpg') # 20x20 grid
WIDTH, HEIGHT = GRID.get_width(), GRID.get_height()
NUM_SQUARES = 10
GRID_SQUARE_SIZE = WIDTH/NUM_SQUARES



SQUARE = pygame.transform.scale(pygame.image.load('red_square.png'), size=(GRID_SQUARE_SIZE,GRID_SQUARE_SIZE))
# SQUARE = pygame.transform.scale(pygame.image.load('berg.png'), size=(GRID_SQUARE_SIZE,GRID_SQUARE_SIZE))


APPLE = pygame.transform.scale(pygame.image.load('apple.png'), size=(GRID_SQUARE_SIZE,GRID_SQUARE_SIZE))

WIN = pygame.display.set_mode((WIDTH,HEIGHT+GRID_SQUARE_SIZE))
pygame.display.set_caption('SNAKE')
FPS = 60


# def blit_rotate_center(win, image, top_left, angle):    # BARA FÖR ATT ROTERA BILDEN
#     rotated_image = pygame.transform.rotate(image, angle)
#     new_rect = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)
#     win.blit(rotated_image, new_rect.topleft)


class Snake:
    def __init__(self,color,speed,grid_square_size,square_image):
        self.color = color
        self.speed = speed      # Rutor per sekund
        self.angle = 0
        self.square_size = grid_square_size
        self.img = square_image
        self.x, self.y = int(NUM_SQUARES/2)*self.square_size, int(NUM_SQUARES/2)*self.square_size
        self.list_of_coordinates = [(self.x,self.y),(self.x-self.square_size,self.y),(self.x-2*self.square_size,self.y)]

    def getAngle(self):
        return self.angle

    def getImg(self):
        return self.img

    def getCoords(self):
        return (self.x,self.y)

    def getListOfCoords(self):
        return self.list_of_coordinates

    def getSpeed(self):
        return self.speed

    def setAngle(self,angle):
        self.angle=angle

    def teleport(self,x,y): # För att teleportera snake till andra sidan
        self.x = x
        self.y = y
        self.list_of_coordinates.pop(0)
        self.list_of_coordinates.insert(0, (self.x, self.y))

    def move(self, eaten_apple):
        self.x += np.cos(self.angle) * self.square_size 
        self.y -= np.sin(self.angle) * self.square_size 
        if not eaten_apple:
            self.list_of_coordinates.pop(len(self.list_of_coordinates)-1)
        self.list_of_coordinates.insert(0, (self.x,self.y))

class Apple():
    def __init__(self,image,square_size):
        self.square_size = square_size
        self.coords = ((int(NUM_SQUARES/2)+3)*self.square_size, int(NUM_SQUARES/2)*self.square_size)   # Spawnar ett äpple 3 rutor framför snakeboi
        self.img = image

    def getImg(self):
        return self.img

    def getCoords(self):
        return self.coords

    def getImage(self):
        return self.image

    # def setCoords(self,new_coords):
    #     self.coords = coords

    def move(self, new_coords):
        self.coords = new_coords


### GÖR SELF.SQUARES TYP SOM LISTA
### Lista med (x,y) för varje cell


def draw_snake(win, snake):
    [win.blit(snake.getImg(), coords) for coords in snake.getListOfCoords()]
    # pygame.display.update()

def draw_apple(win, apple):
    win.blit(apple.getImg(),apple.getCoords())
    # pygame.display.update()

def random_coordinates(snake):
    x = GRID_SQUARE_SIZE*random.randint(0,NUM_SQUARES-1)
    y = GRID_SQUARE_SIZE*random.randint(0,NUM_SQUARES-1)
    if (x,y) in snake.getListOfCoords():
        return random_coordinates(snake)
    else:
        return (x,y)

def game_over(snake):
    if np.round(snake.getCoords(),2).tolist() in np.round(snake.getListOfCoords()[1:],2).tolist():
        return True
    else:
        return False

run = True
clock = pygame.time.Clock()

snake = Snake('red', 5, GRID_SQUARE_SIZE, SQUARE)
apple = Apple(APPLE, GRID_SQUARE_SIZE)

pygame.font.init()
font = pygame.font.Font('freesansbold.ttf', 32)

game_over_text = font.render('GAME OVER', True, 'red')
game_over_textRect = game_over_text.get_rect()
game_over_textRect.center = (int(NUM_SQUARES/2)*GRID_SQUARE_SIZE, int(NUM_SQUARES/2)*GRID_SQUARE_SIZE)

score=0
tick_counter = 0
already_pressed = False

while run:  # Gör kortare genom att göra om till funktioner
    clock.tick(FPS)
    tick_counter+=1

    text = font.render(f'Score: {score}', True, 'white')
    textRect = text.get_rect()
    textRect.topleft = (0, HEIGHT)
    WIN.fill('black')
    WIN.blit(text, textRect)

    WIN.blit(GRID,(0,0))
    draw_apple(WIN, apple)
    draw_snake(WIN, snake)
    pygame.display.update()
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] and not snake.getAngle()==np.pi and not snake.getAngle()==0 and not already_pressed:
        already_pressed=True
        snake.setAngle(np.pi)
    if keys[pygame.K_d] and not snake.getAngle()==np.pi and not snake.getAngle()==0 and not already_pressed:
        already_pressed=True
        snake.setAngle(0)
    if keys[pygame.K_w] and not np.abs(snake.getAngle())==np.pi/2 and not already_pressed:
        already_pressed=True
        snake.setAngle(np.pi/2)
    if keys[pygame.K_s] and not np.abs(snake.getAngle())==np.pi/2 and not already_pressed:
        already_pressed=True
        snake.setAngle(-np.pi/2)

    foodtime = False

    if (snake.getSpeed()*tick_counter)%FPS == 0:   # motverka FPS men fånga pressed keys
        already_pressed = False

        if np.all(np.round(apple.getCoords(),2) == np.round(snake.getCoords(),2)):  # Round för att bli kvitt små konstiga beräkningsfel, 30.750000000000004 != 30.75
            foodtime = True
            apple.move(random_coordinates(snake))
            score += 1

        snake.move(eaten_apple = foodtime)

        x,y = snake.getCoords()
        if not (0 <= x < WIDTH and 0 <= y < HEIGHT):  # Om snake utanför rutnätet
            print('hej',y)
            snake.teleport(x*(not 0 <= y < HEIGHT) + WIDTH*(round(x) < 0),y*(not 0 <= x < WIDTH) + (HEIGHT-GRID_SQUARE_SIZE)*(round(y) < 0))
            print(snake.getCoords())

    if game_over(snake):
        WIN.blit(game_over_text, game_over_textRect)
        pygame.display.update()
        break
        

# print(HEIGHT)
# print(WIDTH)

time.sleep(5)


pygame.quit