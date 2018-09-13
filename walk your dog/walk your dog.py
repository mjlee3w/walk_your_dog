# walk your dog!
#
# by MJLee

import pygame, random, time
pygame.init()
pygame.mixer.init()

screenWidth = 500
screenHeight = 312

win = pygame.display.set_mode((screenWidth,screenHeight))

pygame.display.set_caption("Walk Your Dog!")

# music
pygame.mixer.music.load('Ragamama.mp3')
pygame.mixer.music.play(-1)
barkSnd = pygame.mixer.Sound('bark.wav')
pantSnd = pygame.mixer.Sound('panting.wav')
eatSnd = pygame.mixer.Sound('eating.wav')

# upload sprite char (dog)
walkRight = [pygame.image.load('S_R1.png'), pygame.image.load('S_R2.png'), pygame.image.load('S_R3.png'), pygame.image.load('S_R4.png'), pygame.image.load('S_R5.png'), pygame.image.load('S_R6.png')]
walkLeft = [pygame.image.load('S_L1.png'), pygame.image.load('S_L2.png'), pygame.image.load('S_L3.png'), pygame.image.load('S_L4.png'), pygame.image.load('S_L5.png'), pygame.image.load('S_L6.png')]
bg = pygame.image.load('background.jpg')
barkLeft = [pygame.image.load('S_BL1.png'), pygame.image.load('S_BL2.png'), pygame.image.load('S_BL3.png'), pygame.image.load('S_BL1.png'), pygame.image.load('S_BL2.png'), pygame.image.load('S_BL3.png')]
barkRight = [pygame.image.load('S_BR1.png'), pygame.image.load('S_BR2.png'), pygame.image.load('S_BR3.png'), pygame.image.load('S_BR1.png'), pygame.image.load('S_BR2.png'), pygame.image.load('S_BR3.png')]
char = [pygame.image.load('S_BL2.png'), pygame.image.load('S_BR2.png')] # Left and Right stance

# bird sprite
fly = [pygame.image.load('bird1.png'), pygame.image.load('bird2.png'), pygame.image.load('bird1.png'), pygame.image.load('bird2.png'), pygame.image.load('bird1.png'), pygame.image.load('bird2.png')]

# init
clock = pygame.time.Clock()

class dog(object):
    def __init__(self, x, y, width, height):
        # dog image
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        # dog actions
        self.vel = 5
        self.isJump = False
        self.jumpCount = 7
        self.left = False
        self.right = False
        self.up = False
        self.walkCount = 0
        self.standing = True

    def draw(self,win):
        if self.walkCount + 1 >= 18:
            self.walkCount = 0

        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
        # not walk = standing or barking
        else:
            if self.right:
                if self.up:
                    win.blit(barkRight[self.walkCount//3], (self.x,self.y))
                    self.walkCount += 1
                    barkSnd.play()
                else:
                    win.blit(char[1], (self.x,self.y))
            else:
                if self.up:
                    win.blit(barkLeft[self.walkCount//3], (self.x,self.y))
                    self.walkCount += 1
                    barkSnd.play()
                else:
                    win.blit(char[0], (self.x,self.y))
                    
class bird(object):
    def __init__(self, x, y, width, height):
        # bird image
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        # bird actions
        self.vel = 2
        self.walkCount = 0

    def draw(self, win):
        if self.walkCount + 1 >= 18:
            self.walkCount = 0

        win.blit(fly[self.walkCount//3], (self.x, self.y))
        self.walkCount += 1

class food(object):
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vel = 10

    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


# redrawing game window
def redrawGameWindow():
    win.blit(bg, (0,0))
    d.draw(win)
    bir.draw(win)
    for pellet in pellets:
        pellet.draw(win)
    pygame.display.update()

# bird fly funct
def birdFly():
    if d.up:
        bir.x += (bir.vel + 7)
    else:
        bir.x += bir.vel
    if bir.x > screenWidth:
        bir.x = 0

# main loop
d = dog(50, 250, 87, 54)
bir = bird(0, 90, 30, 30)
pellets = []
run = True
while run:
    # delay
    clock.tick(18)
    
    # quit action
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    for pellet in pellets:
        if 0 < pellet.y < screenHeight-20:
            pellet.y += pellet.vel
            
        if d.x < pellet.x < d.x + d.height:
            pellets.pop(pellets.index(pellet))
            eatSnd.play()
        

    # dog pet (mouse)
    [xMouse, yMouse] = pygame.mouse.get_pos()
    if d.x+d.width > xMouse > d.x and d.y+d.height > yMouse > d.y:
        pantSnd.play()
    
    # keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and d.x > 0:
        d.x -= d.vel
        d.left = True
        d.right = False
        d.up = False
        d.standing = False
    elif keys[pygame.K_RIGHT] and d.x < (screenWidth - d.width):
        d.x += d.vel
        d.right = True
        d.left = False
        d.up = False
        d.standing = False
    elif keys[pygame.K_UP]:
        d.up = True
        d.standing = True
    else:
        d.standing = True
        d.up = False
        d.walkCount = 0
        
    # jump init
    if not(d.isJump):
        if keys[pygame.K_SPACE]:
            d.isJump = True
            d.right = False
            d.left = False
            d.walkCount = 0
    # jump
    else:
        if d.jumpCount >= -7:
            neg = 1
            if d.jumpCount < 0:
                neg = -1
            d.y -= neg*0.5*(d.jumpCount ** 2)
            d.jumpCount -= 1
        else:
            d.isJump = False
            d.jumpCount = 7

    
    # dog feed
    randX = random.randint(20, screenWidth-20)
    if keys[pygame.K_DOWN]:
        if len(pellets) < 5:
            pellets.append(food(randX, 200, 6, (139,69,19)))
            

    # bird flying
    birdFly()

    redrawGameWindow()
    
pygame.mixer.music.stop()    
pygame.quit()
