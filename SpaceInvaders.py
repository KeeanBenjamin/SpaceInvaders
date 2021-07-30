# Space Invaders Game

# Import the pygame package and a bit more...
import pygame, sys, random
from pygame.locals import *

pygame.init()

# set up the window.
# These are globals (they're used pretty much everywhere)
hSize = 1024
vSize = 512
windowSurface = pygame.display.set_mode((hSize, vSize), 0, 32)

# If a rectangle goes out of bounds, make it go back in a bit
def fixOutOfBounds(aRect):
    if aRect.left < 0:
        aRect.left = 0
    elif aRect.right > hSize:
        aRect.right = hSize
    if aRect.top < 0:
        aRect.top = 0
    elif aRect.bottom > vSize:
        aRect.bottom = vSize
    return aRect

# This class represents a generic sprite
# It is derived from the "Sprite" class that is built into Pygame
class mySprite(pygame.sprite.Sprite):
    # The code that says how to set up the first instance of player (pass in a location)
    def __init__(self, imgFile, xStart=0, yStart=0, speed=0):
        # Call the parent class (Sprite) constructor
        super().__init__()

        #  The image for this sprite is passed into the constructor. Scale the image to a 32x32
        self.image = pygame.transform.scale(imgFile, (32, 32))
        # Get the rectangle corresponding to the image
        self.rect = self.image.get_rect(center=(xStart, yStart))

        # Set the start location and speed according to what is being passed in
        self.xStart, self.yStart, self.speed = xStart, yStart, speed

    # Shooter will move according to U/D/L/R
    def moveKeyboardUDLR(self, pressed):
        self.rect.x = mouseX

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.Surface([4, 8])
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y -= 5

class enemyBullet(pygame.sprite.Sprite):
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.Surface([4, 8])
        self.image.fill(RED)

        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y += 3

# ------------------------------------------------
class enemySprite(pygame.sprite.Sprite):
    # The code that says how to set up the first instance of player (pass in a location)
    def __init__(self, imgFile, xStart=0, yStart=0, xspeed=0, yspeed=0):
        # Call the parent class (Sprite) constructor
        super().__init__()

        #  The image for this sprite is passed into the constructor. Scale the image to a 32x32
        self.image = pygame.transform.scale(imgFile, (32, 32))
        # Get the rectangle corresponding to the image
        self.rect = self.image.get_rect(center=(xStart, yStart))

        # Set the start location and speed according to what is being passed in
        self.xStart, self.yStart, self.xspeed, self.yspeed = xStart, yStart, xspeed, yspeed

    # Pick what direction it moves
    def move(self):
        self.rect.x += self.xspeed
        self.rect.y += self.yspeed
        if self.rect.left < 0 or self.rect.right > hSize:
            self.xspeed *= -1
        if self.rect.top < 0 or self.rect.bottom > vSize:
           self.yspeed *= -1
        self.rect = fixOutOfBounds(self.rect)

    def collide(self, enemysprite2):
        if self.rect.colliderect(enemysprite2.rect):
            self.xspeed *= -1
            self.yspeed *= 1
            # enemysprite2.rect.xSpeed*=-2
            # enemysprite2.rect.ySpeed*=-2

# Set a caption for the display window
pygame.display.set_caption('Space Invaders Game!')

# set up the colors - Each of these are RGB settings between 0 and 255
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
TEAL = (86,237,253)

# Set up a font for later use
basicFont = pygame.font.SysFont(None, 48)

# Make sure this image is in the same directory as your .py, or give it a directory path (careful, since
# path may change...)
shooterIMG = pygame.image.load('shooter.png').convert_alpha()

# create shooter - Pass in image and initial location (bottom center)
shooter = mySprite(shooterIMG, hSize // 2, 28 * vSize // 32, 5)

# Make a list of every sprite and add in the shooter
all_sprites_list = pygame.sprite.Group()
all_sprites_list.add(shooter)
bullet_list = pygame.sprite.Group()
enemy_list = pygame.sprite.Group()
enemy_bullet_list = pygame.sprite.Group()
shooter_list = pygame.sprite.Group()
shooter_list.add(shooter)

# ------------------------------------------------
start = -2
score = 0
shots = 85
highscore = 0
lives = 3
killed = 0

goombaIMG = pygame.image.load('invaderPixel.png').convert_alpha()
goombaIMG2 = pygame.image.load('invaderPixel2.png').convert_alpha()
gList = []
xPos = hSize - 100
yPos = vSize - 520

for i in range(84):
    xSpeed = 1
    if i % 14 == 0:
        yPos += (vSize / 11)
        xPos = hSize - (hSize / 10)
    if (i >= 14 and i < 28) or (i >= 42 and i < 56) or (i >= 70):
        xSpeed = -1
    xPos -= (hSize / 18)
    ySpeed = 0

    if i < 42:
        gList.append(enemySprite(goombaIMG, xPos, yPos, xSpeed, ySpeed))
    elif i >= 43:
        gList.append(enemySprite(goombaIMG2, xPos, yPos, xSpeed, ySpeed))
for g in gList:
    all_sprites_list.add(g)
    enemy_list.add(g)

# ------------------------------------------------
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
pygame.key.set_repeat(50,300)


while True:
    clock.tick(30)
    for event in pygame.event.get():
        (mouseX, mouseY) = pygame.mouse.get_pos()
        # If the event is quit, exit.
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
                bullet = Bullet()
                bullet.rect.x = shooter.rect.x
                bullet.rect.y = shooter.rect.y
                shots -= 1
                all_sprites_list.add(bullet)
                bullet_list.add(bullet)
        elif event.type != QUIT:
            enemybullet = enemyBullet()
            enemybullet.rect.x = random.randint(100, hSize)
            enemybullet.rect.y = random.randint(1, vSize // 2)
            all_sprites_list.add(enemybullet)
            enemy_bullet_list.add(enemybullet)
    all_sprites_list.update()

    # Mechanics for each bullet
    for bullet in bullet_list:
        # See if bullet hits enemy
        ememy_hit_list = pygame.sprite.spritecollide(bullet,enemy_list,True)

        # for each hit remove the bullet and add to score
        for e in ememy_hit_list:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)
            killed += 1
            if score <= 10:
                score += 10
            if score > 10:
                score *= 1.2

        # remove bullet if it flies up off the screen
        if bullet.rect.y < -10:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)

    for enemybullet in enemy_bullet_list:
        #see if enemybullet hits shooter
        shooter_hit_list = pygame.sprite.spritecollide(enemybullet,shooter_list,True)
        # For each hit remove the bullet and subtract a life
        for s in shooter_hit_list:
            enemy_bullet_list.remove(enemybullet)
            all_sprites_list.remove(enemybullet)
            lives -= 1
            # This automatically adds the next shooter after you are hit
            shooter_list.add(shooter)
            all_sprites_list.add(shooter)
        # Remove bullet if it flies off the screen
        if enemybullet.rect.y > vSize:
            enemy_bullet_list.remove(enemybullet)
            all_sprites_list.remove(enemybullet)

    # Get the list of all keys that are pressed
    pressed = pygame.key.get_pressed()

    # Keep processing events if nobody has won or lost
    # Move shooter according to Left/Right (UDLR)
    shooter.moveKeyboardUDLR(pressed)

    # ------------------------------------------------
    # Make enemies move
    for g in gList:
        g.move()

    for g in gList:
        for g2 in gList:
            if g != (g2):
                if g2.collide(g):
                    xSpeed = 1
    score = int(score)

    if start == -2 and shots != 0:
        windowSurface.fill(BLACK)
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        textsurface6 = myfont.render("Game: Space Invaders", False, TEAL)
        windowSurface.blit(textsurface6, (hSize // 3, vSize // 12))
        textsurface3 = myfont.render("RULES: You have 3 lives and 85 shots, destroy all enemy ships.", False, RED)
        windowSurface.blit(textsurface3, (hSize // 15, vSize // 4))
        textsurface5 = myfont.render("The more ships you shoot, the more points you earn.", False, RED)
        windowSurface.blit(textsurface5, (hSize // 6, vSize // 3))
        textsurface7 = myfont.render("Controls: Use Left and Right arrows to move your ship.", False, BLUE)
        windowSurface.blit(textsurface7, (hSize // 6, vSize // 2.2))
        textsurface8 = myfont.render("Attack: Press the Spacebar to shoot at enemy ships.", False, BLUE)
        windowSurface.blit(textsurface8, (hSize // 5.5, vSize // 1.8))
        textsurface8 = myfont.render("THE FATE OF THE UNIVERSE IS IN YOUR HANDS!", False, WHITE)
        windowSurface.blit(textsurface8, (hSize // 6, vSize // 1.4))
        textsurface4 = myfont.render("Press Mouse to play!!", False, RED)
        windowSurface.blit(textsurface4, (hSize // 3, vSize // 1.2))
        pygame.display.update()
        if event.type == MOUSEBUTTONDOWN:
            start = 0

    if shots == 0 or lives == 0:
        start = -1
        windowSurface.fill(BLUE)
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        textsurface3 = myfont.render("Game Over!!!", False, WHITE)
        textsurface4 = myfont.render("Your Score:", False, WHITE)
        textsurface5 = myfont.render("High Score:", False, WHITE)
        textsurface6 = myfont.render(str(score), False, WHITE)
        textsurface7 = myfont.render(str(highscore), False, WHITE)
        windowSurface.blit(textsurface3, (hSize // 2.5, vSize // 3.5))
        windowSurface.blit(textsurface4, (hSize // 2.7, vSize // 2.3))
        windowSurface.blit(textsurface5, (hSize // 2.7, vSize // 2))
        windowSurface.blit(textsurface6, (hSize // 1.85, vSize // 2.3))
        windowSurface.blit(textsurface7, (hSize // 1.85, vSize // 2))
        textsurface8 = myfont.render("Press Mouse to play!!", False, WHITE)
        windowSurface.blit(textsurface8, (hSize // 3, vSize // 1.45))
        if score > highscore:
            highscore = score
        if event.type == MOUSEBUTTONDOWN:
            start = 0
            shots = 85
            score = 0
            lives = 3
            killed = 0
            for g in gList:
                all_sprites_list.add(g)
                enemy_list.add(g)
        pygame.display.update()

    if killed == 84 or killed == 85 or killed == 83:
        start = -1
        windowSurface.fill(BLUE)
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        textsurface3 = myfont.render("Congratulations, you saved the world!!", False, WHITE)
        textsurface4 = myfont.render("Your Score:", False, WHITE)
        textsurface5 = myfont.render("High Score:", False, WHITE)
        textsurface6 = myfont.render(str(score), False, WHITE)
        textsurface7 = myfont.render(str(highscore), False, WHITE)
        windowSurface.blit(textsurface3, (hSize // 4, vSize // 3.5))
        windowSurface.blit(textsurface4, (hSize // 2.7, vSize // 2.3))
        windowSurface.blit(textsurface5, (hSize // 2.7, vSize // 2))
        windowSurface.blit(textsurface6, (hSize // 1.85, vSize // 2.3))
        windowSurface.blit(textsurface7, (hSize // 1.85, vSize // 2))
        textsurface8 = myfont.render("Press Mouse to play!!", False, WHITE)
        windowSurface.blit(textsurface8, (hSize // 3, vSize // 1.45))
        if score > highscore:
            highscore = score
        if event.type == MOUSEBUTTONDOWN:
            start = 0
            shots = 85
            score = 0
            lives = 3
            killed = 0
            for g in gList:
                all_sprites_list.add(g)
                enemy_list.add(g)
        pygame.display.update()

    if start != -1 and start != -2 and shots!= 0 and lives != 0:
        windowSurface.fill(BLACK)
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        textsurface = myfont.render(str(score), False, WHITE)
        textsurface2 = myfont.render(str(highscore), False, WHITE)
        textsurface3 = myfont.render(str(shots), False, WHITE)
        livestext = myfont.render(str(lives), False, WHITE)
        textsurface10 = myfont.render("Score:", False, WHITE)
        textsurface20 = myfont.render("HighScore:", False, WHITE)
        textsurface30 = myfont.render("Shots:", False, WHITE)
        textSurface49 = myfont.render("Lives: ",False,WHITE)
        windowSurface.blit(textsurface, (hSize // 2.35, vSize // 1.1))
        windowSurface.blit(textsurface2, (hSize // 6, vSize //1.1))
        windowSurface.blit(textsurface3, (hSize // 1.43, vSize // 1.1))
        windowSurface.blit(livestext, (hSize // 1.1, vSize // 1.1))
        windowSurface.blit(textsurface10, (hSize // 3, vSize // 1.1))
        windowSurface.blit(textsurface20, (hSize // 100, vSize // 1.1))
        windowSurface.blit(textsurface30, (hSize // 1.65, vSize // 1.1))
        windowSurface.blit(textSurface49, (hSize // 1.2, vSize // 1.1))
        if score > highscore:
            highscore = score
        # Draw all sprites
        all_sprites_list.draw(windowSurface)
        pygame.display.update()