import pygame
import random

from pygame.locals import(
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,

)

#Not Safe to Change
size = 25
gridsize = 20

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player,self).__init__()
        self.length = 5
        self.surf = pygame.image.load("sprite2.png").convert()
        self.surf.set_colorkey((255,255,255),RLEACCEL)
        self.rect = self.surf.get_rect()

    def rotate(self, dir):
        self.surf = pygame.image.load("sprite2.png").convert()
        angle = 0
        if dir == 'down':
            angle=270
        elif dir == 'left':
            angle = 180
        elif dir == 'up':
            angle = 90
        self.surf = pygame.transform.rotate(self.surf,angle)

class Appel(pygame.sprite.Sprite):
    def __init__(self):
        super(Appel, self).__init__()
        self.surf = pygame.image.load("appel.png").convert()
        self.surf.set_colorkey((255,255,255),RLEACCEL)
        self.rect = self.surf.get_rect()
        self.x = random.randint(0,gridsize-1)
        self.y = random.randint(0,gridsize-1)

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
icon = pygame.image.load('sprite2.png')
pygame.display.set_icon(icon)
pygame.display.set_caption('snek')


screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])

player = Player()
clock = pygame.time.Clock()
running = True
dir = 'static'
headX = (SCREEN_WIDTH)/2.0
headY = (SCREEN_HEIGHT)/2.0
baseSpeed = 5

q = []
appelList = []

a = random.randint(0,255)
b = random.randint(0,255)
c = random.randint(0,255)
screen.fill((a,b,c))

boxSize = 500
xMargin = (SCREEN_WIDTH-boxSize)/2
yMargin = (SCREEN_HEIGHT-boxSize)/2

def text_objects(text, font):
    textSurface = font.render(text, True, (0,0,0))
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',20)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((SCREEN_WIDTH/2),(yMargin+boxSize+yMargin/2))
    screen.blit(TextSurf, TextRect)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_UP:
                if dir != 'down':
                    dir = 'up'
            elif event.key == K_DOWN:
                if dir != 'up':
                    dir = 'down'
            elif event.key == K_LEFT:
                if dir != 'right':
                    dir = 'left'
            elif event.key == K_RIGHT:
                if dir != 'left':
                    dir = 'right'


    screen.fill((a,b,c))
    a = a + random.randint(-1,1)
    b = b + random.randint(-1,1)
    c = c + random.randint(-1,1)
    if a < 0 or a > 255:
        a = random.randint(20,235)
    if b < 0 or b > 255:
        b = random.randint(20,235)
    if c < 0 or c > 255:
        c = random.randint(20,235)

    pygame.draw.rect(screen,(10,102,35),(xMargin,yMargin,boxSize,boxSize))
    for x in range(int(xMargin),int(SCREEN_WIDTH-xMargin),int(boxSize*1.0/gridsize)):
        pygame.draw.rect(screen,(26,201,73),(x,yMargin,1,boxSize))
    for y in range(int(yMargin),int(SCREEN_HEIGHT-yMargin),int(boxSize*1.0/gridsize)):
        pygame.draw.rect(screen,(26,201,73),(xMargin,y,boxSize,1))




    gridX = int((headX+size/2-xMargin)/(boxSize*1.0/gridsize))
    gridY = int((headY+size/2-yMargin)/(boxSize*1.0/gridsize))

    if len(appelList) == 0:
        appelList.append(Appel())
    for appel in appelList:
        if appel.x == gridX and appel.y == gridY:
            appelList.remove(appel)
            player.length = player.length + 1
        screen.blit(appel.surf, (int(appel.x*(boxSize*1.0/gridsize)+xMargin)+1,int(appel.y*(boxSize*1.0/gridsize)+yMargin)+1))

    if q.count((gridX,gridY))<1:
        q.append((gridX,gridY))

    if len(q)>player.length:
        q.pop(0)

    for x in q:
        pygame.draw.rect(screen,(139,232,163),(int(x[0]*(boxSize*1.0/gridsize)+xMargin),int(x[1]*(boxSize*1.0/gridsize)+yMargin),25,25))

    if headX<xMargin:
        headX = xMargin
    if headX > SCREEN_WIDTH-xMargin-size:
        headX = SCREEN_WIDTH-xMargin-size
    if headY <= yMargin:
        headY = yMargin
    if headY >=SCREEN_HEIGHT-yMargin-size:
        headY = SCREEN_HEIGHT-yMargin-size

    if dir == 'up':
        headX = gridX*(boxSize*1.0/gridsize)+xMargin
        headY = headY - baseSpeed
    elif dir == 'down':
        headX = gridX*(boxSize*1.0/gridsize)+xMargin
        headY = headY + baseSpeed
    elif dir == 'left':
        headY = gridY*(boxSize*1.0/gridsize)+yMargin
        headX = headX - baseSpeed
    elif dir == 'right':
        headY = gridY*(boxSize*1.0/gridsize)+yMargin
        headX = headX + baseSpeed


    screen.blit(player.surf,(int(headX),int(headY)))

    message_display("Length: "+ str(player.length))


    player.rotate(dir)

    pygame.display.flip()
    clock.tick(60)


pygame.quit()
