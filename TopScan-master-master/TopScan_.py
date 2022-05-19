import random
import pygame
import math
from pygame.locals import *

FPS = 40                    # frames per second
POWERUPTIME = 7000          # duration of power up speed
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# inizializzazione
pygame.init()
pygame.mixer.init()
random.seed()

window = pygame.display.set_mode((0, 0), FULLSCREEN)    # crea finestra di gioco
pygame.display.set_caption("TopScan")
clock = pygame.time.Clock()                             # gestisce FPS del gioco
pygame.mixer.music.load("Music/menuTrack.ogg")          # carica la colonna sonora

#fonts = pygame.font.match_font("arial")

def updateScreen():
    # the function updates the constant changes to the screen
    pygame.display.flip()
    clock.tick(FPS)

def updateGameScreen(background):
    """ the function rebuilds the entire game window.
            - background: the background image of the play area
    """
    window.blit(title, ((20, 20)))
    window.blit(border, ((window.get_width() - 820) /1.2, (window.get_height() - 620) /1.5))
    border.fill(YELLOW)
    border.blit(screen, (10, 10))
    title.blit(titleImg, (0, 0))
    screen.blit(background, (0, 0))

def drawLives(surface, x, y, lives, image):
    """ the function draws the player's lives on the playing area.
        - surface: the window where to draw lives
        - x, y: where to paste the background
        - lives: the player's lives
    """


    for i in range(lives):
        image = pygame.transform.smoothscale(image, (30, 30))
        imageRect = image.get_rect()
        imageRect.right = x
        imageRect.bottom = y - 50 * i
        surface.blit(image, imageRect)

def drawText(surface, text, size, x, y, color, flag):           
    """ the function draws the text.
            - surface: the surface on which to draw the text
            - text: the text to insert
            - size: the size of the text
            - x, y: the location to paste the text
            - color: the color of the text
            - flag: set to True places the boss's name referring to a different angle of the rect
    """
    font = pygame.font.SysFont("Arial", size, bold = True)
    textSurface = font.render(text, True, color)
    textRect = textSurface.get_rect()
    if flag:
        textRect.topright = (x, y)     
    else:
        textRect.topleft = (x, y)
    surface.blit(textSurface, textRect)

def drawTextLikeSprite(surface, group, text, size, x, y, color):
    """ the function draws the text implementing it as a sprite..
            - surface: the surface on which to draw the text
            - group: the sprite group to add the text sprite to
            - text: the text to insert
            - size: the size of the text
            - x, y: the position of the rect of the image
            - color: the color of the text

            - textSprite: the function returns the sprite containing the inserted text
    """
    font = pygame.font.SysFont("Arial", size, bold = True)
    textSurface = font.render(text, True, color)
    textSprite = pygame.sprite.Sprite(group)
    textSprite.image = textSurface
    textSprite.rect = textSurface.get_rect()
    textSprite.rect.topleft = (x, y)

    return textSprite

def drawShield(surface, x, y, percentage, image, flag, maxLife, name = "none"):     
    """ the function draws the chosen value using two rectangles, outlineRect and fillRect.
            - surface: the surface on which to draw the bar
            - x, y: the position to draw the bar
            - percentage: the quantity to represent
            - flag: set to True it writes the name of the boss next to the bar, while set to False it draws the image of the shield next to the bar
            - name: the name of the boss
            - maxLife: the maximum life of the boss
    """
    if flag:                
        drawText(surface, name, 36, x - 20, y - 12, WHITE, True)
    else:
        image = pygame.transform.scale(image, (20, 20))
        surface.blit(image, (x - 30, y))

    if percentage < 0:                                                     
        percentage = 0
    length = 200
    height = 20
    fill = (percentage / maxLife) * length
    outlineRect = pygame.Rect(x, y, length, height)
    fillRect = pygame.Rect(x, y, fill, height)
    pygame.draw.rect(surface, RED, fillRect)
    pygame.draw.rect(surface, WHITE, outlineRect, 4)

def updateDex(list, entry):
    """ the function updates the list of defeated enemies.
            - list: the list containing the names of the enemies
            - entry: the instances of the enemy
    """
    
    window.fill(BLACK)

    diz = {"Invader" : 0, "Roller" : 1, "Rare" : 2, "Gorgodusa" : 3, "Golem" : 7, "Bidramon" : 11}

    list[diz[entry]] = entry

    drawText(window, "EnemyDex", 32, 100, 200, WHITE, False)    
    for i in range(12):
        drawText(window, list[i], 32, 160, 250 + i*40, WHITE, False)
    '''
        if entry == "Invader":
            drawText(window, list[0], 32, 160, 300, BLACK, False)
            list[0] = entry
            drawText(window, list[0], 32, 160, 300, WHITE, False)
        elif entry == "Roller":
            drawText(window, list[1], 32, 160, 350, BLACK, False)
            list[1] = entry
            drawText(window, list[1], 32, 160, 350, WHITE, False)
        elif entry == "Rare":
            drawText(window, list[2], 32, 160, 400, BLACK, False)
            list[2] = entry
            drawText(window, list[2], 32, 160, 400, WHITE, False)
        elif entry == "Gorgodusa" or entry == "Golem" or entry == "Bidramon":
            drawText(window, list[3], 32, 160, 450, BLACK, False)
            list[3] = entry
            drawText(window, list[3], 32, 160, 450, WHITE, False)
    '''
def usePowerUp(power, player):
    """ the function represents the effect of the different power ups.
            - power: the power up obtained by the player
            - player: the player to apply the changes to
    """
    if power.type == "shield":          # strengthens the player's shield
        if player.shield < 100:
            player.shield += 20
            if player.shield > 100:
                player.shield = 100

    elif power.type == "speed":         # increases the player's speed
        player.velx = 10
        player.faster = True
        player.speedTimer = pygame.time.get_ticks()

    elif power.type == "extra":         # adds a life to the player if these are less than 5
        if player.lives < 5:
            player.lives += 1

    elif power.type == "toxic":         # it takes a life from the player if there are more than 1
        if player.lives > 1:
            player.lives -= 1

    elif power.type == "newGun":        # increases the number of bullets fired at the same time by the player
        player.numBull += 1

class Player(pygame.sprite.Sprite):
    """ the class represents the player as a sprite and determines:
            - image: image
            - rect: the rect and its position in the game window
            - vel: the speed of movement on the x and y axis
            - shield: the shield available to the player. Shield == 0 results in the loss of a life
            - lives: the lives available to the player. Lives == 0 results in the loss of the game
            - maxLife: the maximum life of the player
            - numBull: the number of bullets that the player can use at the same time
            - maxNumBull: the maximum number of bullets present on the screen at the same time
            - numTwoShot, numThreeShot: the available number of shots with numBull == 2 and numBull> = 3 respectively
            - shootDelay, lastShot: determine when a new bullet can be created
            - hidden, hideTimer: the vanishing / appearing effect that follows the loss of a player's life
            - faster, speedTimer: determine the time of use of the power up speed
    """
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()
        self.rect.midbottom = (400, 580)
        self.velx = 5
        self.vely = 0
        self.shield = 100
        self.lives = 3
        self.maxLife = 100
        self.numBull = 1
        self.maxNumBull = 5
        self.numTwoShot = 0
        self.numThreeShot = 0
        self.shootDelay = 400
        self.lastShot = pygame.time.get_ticks()
        self.hidden = False
        self.hideTimer = pygame.time.get_ticks()
        self.faster = False
        self.speedTimer = pygame.time.get_ticks()

    def update(self):
        """ the feature constantly updates the player on the screen:
                - the first control adjusts the newGun power up, decreasing numBull after 5 boosted hits
                - the second control adjusts the player's disappear / appearance effect
                - the third control adjusts the power up speed by restoring the player's speed to the original value
                - the fourth control regulates the movement of the player according to the key pressed
        """
        if self.numBull == 3 and self.numThreeShot > 5:
            self.numBull = 1
            self.numThreeShot = 0
        elif self.numBull == 2 and self.numTwoShot > 5:
            self.numBull = 1
            self.numTwoShot = 0
        
        if self.hidden and pygame.time.get_ticks() - self.hideTimer > 500:
            self.hidden = False
            self.rect.topleft = (320, 500)
            self.shield = 100

        if self.faster and pygame.time.get_ticks() - self.speedTimer > POWERUPTIME:
            self.faster = False
            self.velx = 5

        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a] or keystate[pygame.K_LEFT]:
            if self.velx > 0:
                self.velx *= -1
            self.rect.x += self.velx
        elif keystate[pygame.K_d] or keystate[pygame.K_RIGHT]:
            if self.velx < 0:
                self.velx *= -1
            self.rect.x += self.velx
        if self.rect.right > screen.get_width():
            self.rect.right = screen.get_width()
        elif self.rect.left < 0:
            self.rect.left = 0
    
    def hide(self):
        # the function adjusts the disappearance / appearance effect of the player
        self.hidden = True
        self.hideTimer = pygame.time.get_ticks()
        self.rect.center = (2000, 2000)

    def shoot(self, image):
        """
the function adjusts the creation of the next bullet after the one just generated and the number of bullets created at the same time
        """
        global allSprites, bullets
        
        now = pygame.time.get_ticks()
        if now - self.lastShot > self.shootDelay:
            self.lastShot = now
            if self.numBull == 1:
                self.shootDelay = 400
                bullet = Bullet(self.rect.centerx, self.rect.top, image)
                allSprites.add(bullet)
                bullets.add(bullet)
            if self.numBull == 2:
                self.shootDelay = 200
                bullet1 = Bullet(self.rect.left, self.rect.centery, image)
                bullet2 = Bullet(self.rect.right, self.rect.centery, image)
                allSprites.add(bullet1)
                allSprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                self.numTwoShot += 1
            if self.numBull >= 3:
                self.shootDelay = 100
                bullet1 = Bullet(self.rect.left, self.rect.centery, image)
                bullet2 = Bullet(self.rect.right, self.rect.centery, image)
                bullet3 = Bullet(self.rect.centerx, self.rect.top, image)
                allSprites.add(bullet1)
                allSprites.add(bullet2)
                allSprites.add(bullet3)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(bullet3)
                self.numThreeShot += 1

class Obstacles(pygame.sprite.Sprite):
    """
the class represents the obstacle generated by the boss during the level and determines:
        - image: image
        - rect: the rect and its position in the game window
        - vely: the speed on the y axis
        - owner: the boss who created the obstacle
        - dangerous: set to False prevents the obstacle from damaging the player
        - damage: the damage dealt by the obstacle to the player
        - damageDelay: the time between one damage and the next of the obstacle
        - timeToNewDamage: the time it takes for the obstacle to damage the player again
        - flag: set to True indicates that the obstacle is coming back
    """
    def __init__(self, position, image, vely, damage, damageDelay, owner):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()
        self.rect.centerx = position[0]
        self.rect.top = position[1]
        self.vely = vely
        self.owner = owner
        self.dangerous = True
        self.damage = damage
        self.damageDelay = damageDelay
        self.timeToNewDamage = pygame.time.get_ticks()
        self.back = False

    def update(self):
        # the function constantly updates the position of the obstacle on the screen, eliminating it when it exits the screen

        if self.owner == "Gorgodusa":
            if self.rect.y <= 300:
                self.back = True
                self.vely = 1
            elif self.rect.top > screen.get_height() + 20:
                self.kill()

            if not self.back:
                self.rect.y -= self.vely
            else:
                self.rect.y += self.vely

        elif self.owner == "Golem" or self.owner == "Bidramon":
            self.rect.y += self.vely
            if self.rect.top > screen.get_height():
                self.kill()
    
    def hitPlayer(self):
        # the function manages the damage inflicted by the obstacle to the player. After inflicting one, the obstacle loses that ability for a few seconds.

        self.dangerous = False
        now = pygame.time.get_ticks()

        if now - self.timeToNewDamage > self.damageDelay:
            self.dangerous = True

class Bullet(pygame.sprite.Sprite):
    """ the class represents the bullet as a sprite and determines:
            - image: image
            - rect: the rect and its position in the game window
            - vel: the velocity of the bullet on the y axis
            - bossDamage: the damage dealt by the bullet to bosses
    """
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.vely = -10
        self.bossDamage = 40

    def update(self):
        # the function constantly updates the position of the bullet on the screen, eliminating it as it exits the top side
        self.rect.y += self.vely
        if self.rect.bottom < 0:
            self.kill()

class EnemyBullet(pygame.sprite.Sprite):
    """ the class represents the enemy bullet as a sprite and determines:
            - vel: the speed of the bullet
            - damage: the damage dealt by the bullet to the player
    """
    def __init__(self, x, y, image, vel, direction, damage):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.direction = direction
        self.velx = vel[0]
        self.vely = vel[1]
        self.damage = damage
        self.sinAxis = x
        self.gap = random.randrange(50, 150, 10)
        
    def update(self):        
        # the function constantly updates the position of the bullet on the screen, eliminating it as it exits the top side
        if self.direction == "center":
            self.rect.y += self.vely
        elif self.direction == "right":
            self.rect.x += self.velx
            self.rect.y += self.vely
        elif self.direction == "left":
            self.rect.x += self.velx
            self.rect.y += self.vely
        elif self.direction == "sin":
            self.rect.y += self.vely
            self.rect.x = self.sinAxis + math.sin(self.rect.y*math.pi*screen.get_height()/100/(screen.get_height() - self.image.get_height()))*self.gap
            if self.rect.x < self.sinAxis + 5 and self.rect.x > self.sinAxis - 5:
                self.gap = random.randrange(50, 150, 10)

        if self.rect.bottom < 0:
            self.kill()

class Power(pygame.sprite.Sprite):
    """ the class represents the power up as a sprite and determines:
            - image: image
            - rect: the rect and its position in the game window
            - vel: the velocity of the bullet on the y axis
            - type: the type of power up among those on the list
    """     
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(["shield", "speed", "extra", "toxic", "newGun"])
        self.image = pygame.transform.smoothscale(poweImage[self.type], (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.vely = 5

    def update(self):
        # the function constantly updates the position of the power up on the screen, eliminating it when it comes out from the bottom side
        self.rect.y += self.vely
        if self.rect.top > screen.get_height():
            self.kill()

class Enemy(pygame.sprite.Sprite):
    """ the class represents the prototype of the enemy that will be extended into different types and determines:
            - image: image
            - rect: the rect and its position in the game window
            - name: the name
            - vel: the speed of movement on the x and y axis
            - dex: set to False indicates an enemy not yet eliminated and therefore not yet discovered
            - lives: the lives. Lives == 0 results in the disappearance of the enemy
            - damage: damage dealt to the player's shield by the enemy
            - score: the score obtained by the player on eliminating the enemy
    """
    def __init__(self, image, position, name, lives, damage, score):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()
        self.rect.bottomleft = position
        self.name = "none"
        self.velx = 0
        self.vely = 0
        self.lives = lives
        self.damage = damage
        self.score = score

    def update(self):
        # the feature constantly updates the enemy's position on the screen, eliminating it when it exits from the underside
        self.rect.x += self.velx
        self.rect.y += self.vely
        if self.rect.top > screen.get_height():
            self.kill()

class Invader(Enemy):
    """ the class extends Enemy and represents enemy 1 of the first level, determining:
            - vel: the speed of movement on the x and y axis
            - position:the location of the spawn point
            - name: the name

        inherits from Enemy:
            - lives
            - damage
            - score
    """
    def __init__(self, image, position, vel, lives, damage, score, name = "none"):
        super().__init__(image, position, name, lives, damage, score)
        self.velx = vel[0]
        self.vely = vel[1]
        self.name = "Invader"
                
class Rollers(Enemy):
    """ the class extends Enemy and represents enemy 2 of the first level, determining:
            - vel: the speed of movement on the x and y axis
            - position: the location of the spawn point
            - name: The name
            - offset: used to control left and right side bounce

        eredita da Enemy:
            - lives
            - damage
            - score
    """
    def __init__(self, image, position, vel, lives, damage, score, offset, name = "none"):
        super().__init__(image, position, name, lives, damage, score)
        self.velx = vel[0]
        self.vely = vel[1]
        self.name = "Roller"
        self.offset = offset

    def update(self):
        # the feature constantly updates the enemy's position on the screen, eliminating it when it exits from the underside. Rollers move diagonally from one side of the playing area to the other, bouncing off those sides
        if self.velx > 0:
            self.rect.x += self.velx
            self.rect.y = self.rect.x/4 + self.offset
            if self.rect.right > screen.get_width():
                self.velx *= -1
                self.offset += 355
        elif self.velx < 0:
            self.rect.x += self.velx
            self.rect.y = -self.rect.x/4 + self.offset
            if self.rect.left < 0:
                self.velx *= -1

        if self.rect.top > screen.get_height():
            self.kill()

class Rare(Enemy):
    """ the class extends Enemy and represents the special enemy of the first level, determining:
            - vel: the speed of movement on the x and y axis depending on the position of its spawn point
            - position: the location of the spawn point
            - name: the name

        inherits from Enemy:
            - lives
            - score
    """
    def __init__(self, image, position, lives, score, damage = 0, name = "none"):
        super().__init__(image, position, name, damage, lives, score)
        self.velx = position[1] / 10
        self.name = "Rare"

    def update(self):
        # the feature constantly updates the enemy's position on the screen, eliminating it as it exits from the left and right side
        self.rect.x += self.velx
        if self.rect.left > screen.get_width() + 100 or self.rect.right < -100:
            self.kill()

class Boss(pygame.sprite.Sprite):
    """ the class represents the prototype of the end-of-level boss as a sprite and determines:
            - image: image
            - rect: the rect and its position in the game window
            - lives: the life available to the boss. Lives == 0 results in passing the level
            - damage: the damage dealt by the boss to the player
            - score: the score obtained by the player upon eliminating the boss
            - vel: the speed of movement on the x and y axis
            - dex: set to False indicates an enemy not yet eliminated and therefore not yet discovered
            - split: used by Bidramon to indicate its division
            - lastShot: the tick where the boss throws the bullet
            - lastObstacles: the tick in which the boss launches the secondary attack
            - existsObstacles: set to True indicates the presence of an obstacle on the screen
            - obstaclesDelay: the time elapsed between one secondary attack and the next
    """
    def __init__(self, image, position, name, lives, maxLife, damage, score, vel):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()
        self.rect.midleft = position
        self.name = name
        self.lives = lives
        self.maxLife = maxLife
        self.damage = damage
        self.score = score
        self.velx = vel[0]
        self.vely = vel[1]
        self.split = False
        self.lastShot = pygame.time.get_ticks()
        self.lastObstacles = pygame.time.get_ticks()
        self.existsObstacles = False
        self.obstaclesDelay = 50000
        
    def update(self):
        #
        # the feature constantly updates the position of the boss on the screen
        self.rect.x += self.velx
        self.rect.y += self.vely

    def hit(self):
        # the function manages the boss's reaction to hits
        pass

    def shoot(self):
        # the function handles the main boss attack
        pass

    def obstaclesAtk(self):
        # the function manages the attack with which the boss creates an environmental obstacle
        pass

class Gorgodusa(Boss):
    def __init__(self, image, position, lives, maxLife, damage, score, vel, name = "Gorgodusa"):
        super().__init__(image, position, name, lives, maxLife, damage, score, vel)
        self.name = name
        self.centerImg = pygame.transform.scale(self.image, (20, 20))
        self.leftImg = pygame.transform.rotate(self.centerImg, 45)
        self.rightImg = pygame.transform.rotate(self.centerImg, -45)
        self.shotDelay = 1500
        self.resistence = 10
        
    def update(self):
        global obstacles

        now = pygame.time.get_ticks()

        if now - self.lastShot > self.shotDelay:
            self.shoot()
        elif now - self.lastObstacles > self.obstaclesDelay and len(obstacles) == 0:
            self.obstaclesAtk()

        self.rect.x += self.velx
        self.rect.y += self.vely

        if self.rect.left < 0:
            self.rect.left = 0
            self.velx *= -1
        elif self.rect.right > screen.get_width():
            self.rect.right = screen.get_width()
            self.velx *= -1
    
    def hit(self):
        # soft damage
        if self.lives == 310:
            self.shotDelay = 1500
        
        # hard damage
        elif self.lives == 220:
            self.obstaclesAtk()
            self.obstaclesDelay = 4000
        
        # critical damage
        elif self.lives == 100:
            self.shotDelay = 800
            player.velx = 2

    def shoot(self):        
        self.lastShot = pygame.time.get_ticks()

        centerBullet = EnemyBullet(self.rect.centerx, self.rect.bottom, self.centerImg, (0, 3), "center", 20)
        eBullets.add(centerBullet)
        rightBullet = EnemyBullet(self.rect.centerx, self.rect.bottom, self.rightImg, (1, 3), "right", 20)
        eBullets.add(rightBullet)
        leftBullet = EnemyBullet(self.rect.centerx, self.rect.bottom, self.leftImg, (-1, 3), "left", 20)
        eBullets.add(leftBullet)

    def obstaclesAtk(self):
        self.lastObstacles = pygame.time.get_ticks()

        climbImg = pygame.image.load("Image/Obstacles/climbing.png").convert_alpha()
        climb1 = Obstacles((random.randrange(0, screen.get_width()), screen.get_height() - 100), climbImg, 10, 20, 2000, "Gorgodusa")
        obstacles.add(climb1)
        climb2 = Obstacles((random.randrange(0, screen.get_width()), screen.get_height() - 100), climbImg, 10, 20, 2000, "Gorgodusa")
        obstacles.add(climb2)

class Golem(Boss):
    def __init__(self, image, position, lives, maxLife, damage, score, vel, name = "Golem"):
        super().__init__(image, position, name, lives, maxLife, damage, score, vel)
        self.name = name
        self.position = position
        self.set = self.position[1]
        self.inversion = 1
        self.right = True
        self.counter = 0        
        self.fall = 100
        self.molt = 2
        self.shotDelay = 1000
        self.resistence = 20
        self.numBull = 10
        self.rockImg = pygame.transform.scale(self.image, (20, 20))

    def update(self):
        global obstacles

        now = pygame.time.get_ticks()
        
        if now - self.lastShot > self.shotDelay:
            self.shoot()
        elif now - self.lastObstacles > self.obstaclesDelay and len(obstacles) == 0:
            self.obstaclesAtk()

        if self.rect.left < 0:
            self.rect.left = 0
            self.velx *= -1
            self.right = True
        elif self.rect.right > screen.get_width():
            self.rect.right = screen.get_width()
            self.velx *= -1
            self.right = False

        self.rect.x += self.velx
        self.rect.y = self.set - self.molt * self.counter * self.inversion
        self.counter += self.velx

        if self.rect.y <= self.position[1] - 100:
            self.set = self.position[1] - 99
            if self.right:
                self.inversion = -1
            else:
                self.inversion = 1
            self.counter = 0
        elif self.rect.y >= self.position[1] + self.fall:
            self.set = self.position[1] + self.fall - 1
            if self.right:
                self.inversion = 1
            else:
                self.inversion = -1
            self.counter = 0
    
    def hit(self):

        # soft damage
        if self.lives == 400:
            self.numBull = 12

        # hard damage
        elif self.lives == 200:
            self.resistence = 30
            self.obstaclesAtk()
            self.obstaclesDelay = 5000
        
        # critical damage
        elif self.lives == 100:
            self.numBull = random.randrange(10, 16, 2)
            self.fall = 400
            self.molt = 4
    
    def shoot(self):
        global eBullets
        
        self.lastShot = pygame.time.get_ticks()
        self.shotDelay = 4000

        for i in range(self.numBull):
            rock = EnemyBullet(random.randrange(0, screen.get_width() - self.rockImg.get_width() + 1), -1, self.rockImg, (0, random.randrange(2, 6)), "center", 30)
            eBullets.add(rock)

    def obstaclesAtk(self):
        self.lastObstacles = pygame.time.get_ticks()

        meteorImg = pygame.image.load("Image/Obstacles/meteor.png").convert_alpha()
        meteor1 = Obstacles((random.randrange(0 + meteorImg.get_width(), screen.get_width() - meteorImg.get_width()), -meteorImg.get_height()), meteorImg, 5, 40, 1000, "Golem")
        obstacles.add(meteor1)

class Bidramon(Boss):
    def __init__(self, image, position, lives, maxLife, damage, score, vel, name = "Bidramon"):
        super().__init__(image, position, name, lives, maxLife, damage, score, vel)
        self.name = name
        self.position = position
        self.split = False
        self.shotDelay = 1500
        self.resistence = 20
        self.tornadoImg = pygame.transform.scale(self.image, (20, 20))

    def update(self):   
        now = pygame.time.get_ticks()

        if now - self.lastShot > self.shotDelay:
            self.shoot()
        elif now - self.lastObstacles > self.obstaclesDelay and len(obstacles) == 0:
            self.obstaclesAtk()

        if self.rect.left < 0 and self.velx < 0:
            self.rect.left = 0
            self.velx *= -1
        elif self.rect.right > screen.get_width() and self.velx > 0:
            self.rect.right = screen.get_width()
            self.velx *= -1

        self.rect.x += self.velx

        if self.velx > 0:
            self.rect.y = self.position[1] + math.sin(self.rect.x*math.pi*screen.get_width()/100/(screen.get_width() - self.image.get_width()))*50
        elif self.velx < 0:
            self.rect.y = self.position[1] - math.sin(self.rect.x*math.pi*screen.get_width()/100/(screen.get_width() - self.image.get_width()))*50
    
    def hit(self):

        # soft damage
        if self.lives == 500:
            self.shotDelay = 1400
        
        # medium damage
        elif self.lives == 400:
            self.shotDelay = 1200

        # hard damage
        elif self.lives == 300:
            self.obstaclesAtk()
            self.obstaclesDelay = 6000

        # critical damage
        elif self.lives == 200:
            self.kill()
            self.split = True
    
    def shoot(self):
        global eBullets
        
        self.lastShot = pygame.time.get_ticks()
        
        tornado = EnemyBullet(random.randrange(0, screen.get_width() - self.tornadoImg.get_width() + 1), self.rect.bottom, self.tornadoImg, (0, random.randrange(2, 8)), "sin", 30)
        eBullets.add(tornado)

    def obstaclesAtk(self):
        self.lastObstacles = pygame.time.get_ticks()

        iceImg = pygame.image.load("Image/Obstacles/ice.png").convert_alpha()
        space1 = 0
        spawnXList = [iceImg.get_width(), screen.get_width()/2, screen.get_width()]
        spawnX = random.choice(spawnXList)

        if spawnX == iceImg.get_width():
            spawnY = 1
        elif spawnX == screen.get_width():
            spawnY = -1
        elif spawnX == screen.get_width()/2:
            spawnYList = [-1, 1]
            spawnY = random.choice(spawnYList)

        for i in range(10):
            ice = Obstacles((spawnX + space1*spawnY, -100 -iceImg.get_height() - space1), iceImg, 3, 20, 2000, "Bidramon")
            obstacles.add(ice)
            space1 += 50
            
def saved(group, level, background):
    """ the function offers the possibility to save the progress achieved by the player in a text file.
            - group: used for the restart function
            - level: the current level that will be reported in the save file
            - background: used by the updateGameScreen function
    """
    restart(group, player, True)
    updateGameScreen(background)
        
    drawText(window, "Save?", 32, 1020, 510, WHITE, False)
    yes = drawTextLikeSprite(window, text, "  Yes", 32, 1050, 570, WHITE)
    no = drawTextLikeSprite(window, text, "  No", 32, 1050, 620, WHITE)
    
    done = False
    while not done:                    # the cycle will end when the player has decided whether to save or not
                
        # ciclo degli eventi
        for ev in pygame.event.get():
            if ev.type == MOUSEBUTTONDOWN and ev.button == 1:
                click = ev.pos
                if yes.rect.collidepoint(click):
                    level += 1
                    savedata = open("savedata.txt", "w")
                    savedata.write("Level: {}".format(level) + "\n" + "Score: {}".format(score))
                    savedata.close()
                elif no.rect.collidepoint(click):
                    level += 1
                win = False
                levels(level)

        group[4].draw(window)             # print the save commands in the game area
        updateScreen()

def restart(group, player, flag):
    """ the function reinitializes the level thus allowing a new game.
            - group: list of groups of sprites to be emptied
            - player: the player to be reset by returning lives, shield and numBull to their initial values
            - flag: set to True indicates the restart after passing a level
    """ 
    for list in group:
        for obj in list:
            if obj != player:
                obj.kill()
    
    player.velx = 5

    pygame.time.set_timer(USEREVENT + 1, 0)
    pygame.time.set_timer(USEREVENT + 2, 0)
    pygame.time.set_timer(USEREVENT + 3, 0)
    pygame.time.set_timer(USEREVENT + 4, 0)


    if not flag:
        player.lives = 3
        player.shield = 100
        player.numBull = 1

def showGOScreen(score, group, player, background):
    """ the function accesses the game over screen.
            - score: il punteggio raggiunto dal giocatore viene stampato nell'area di gioco
            - group, player: list of groups to be emptied
            - background: used by the updateGameScreen function
    """  
    updateGameScreen(background)
    restart(group, player, False)

    drawText(window, "GAME OVER", 64, 660, 300, WHITE, False)
    drawText(window, "Press any key to return to the home menu", 18, 670, 500, WHITE, False)
    drawText(window, "Score: {}".format(score), 48, 735, 400, WHITE, False)

    waiting = True
    while waiting:                      # the cycle waits for the player to press a button
        updateScreen()
        # cycle of events
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT or ev.type == KEYDOWN and ev.key == K_ESCAPE:
                pygame.quit()
            if ev.type == pygame.KEYDOWN:
                waiting = False
                    
def mainMenu():
    """ the function accesses the initial menu
    """ 
    global level, score

    background = pygame.image.load("Image/Background/desert.jpg").convert()
    pygame.mixer.music.play(-1)                                                 # start the soundtrack

    game = True
    while game:

        # cycle of events
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT or ev.type == KEYDOWN and ev.key == K_ESCAPE:
                pygame.quit()

            elif ev.type == MOUSEBUTTONDOWN and ev.button == 1:
                click = ev.pos                                      # coordinates of the pointer
                if newGame.rect.collidepoint(click):
                    score = 0
                    level = 1
                    levels(level)
                elif toContinue.rect.collidepoint(click):
                    str = ""
                    savedata = open("savedata.txt", "r")            # access the save file to obtain the player's level and score
                    capture = savedata.readline()
                    for char in range(len(capture)):
                        if capture[char].isdecimal() == True:
                            str = str + capture[char]
                    level = int(str)
                    str = ""
                    capture = savedata.readline()
                    for char in range(len(capture)):
                        if capture[char].isdecimal() == True:
                            str = str + capture[char]
                    score = int(str)
                    savedata.close()
                    levels(level)

        updateScreen()
        updateGameScreen(background)
        
        newGame = drawTextLikeSprite(screen, text, "New Game", 32, 1000, 570, WHITE)
        toContinue = drawTextLikeSprite(screen, text, "Continue", 32, 1000, 620, WHITE)
        text.draw(window)

def levels(level):

    global score
   
    window.fill(BLACK)
    pygame.display.flip()

    bulletImg = pygame.image.load("Image/Player/bullet.png").convert_alpha()
    ciao = pygame.image.load("Image/Enemies/enemyShip.png").convert_alpha()

    bossImg = pygame.image.load("Image/Boss/bear.png").convert_alpha()
    bossImg2 = pygame.image.load("Image/Boss/buffalo.png").convert_alpha()
    bossImg3 = pygame.image.load("Image/Boss/sloth.png").convert_alpha()

    win = None
    enemy1 = None
    enemy2 = None
    spEnemy = None
    boss = None
    bossImg = None
    done = False        # regulates the game cycle
    existsBoss = False

    
    drawText(window, "EnemyDex", 32, 100, 200, WHITE, False)
    for i in range(12):
        drawText(window, enemyDex[i], 32, 160, 250 + i*40, WHITE, False)


    #
    # contain the instructions necessary to generate the current level
    if level == 1:
        numEnemy1 = 0
        numEnemy2 = 0
        numSpEnemy = 0
        background = pygame.image.load("Image/Background/space.png").convert()
        bossImg = pygame.image.load("Image/Boss/bear.png").convert_alpha()
        enemy1Img = pygame.image.load("Image/Enemies/enemyShip.png").convert_alpha()
        enemy2Img = pygame.image.load("Image/Enemies/enemyRoll.png").convert_alpha()
        spEnemyImg = pygame.image.load("Image/Enemies/enemyShip.png").convert_alpha() 

        pygame.time.set_timer(USEREVENT + 1, random.randrange(400, 1500))
        pygame.time.set_timer(USEREVENT + 5, random.randrange(15000, 25000))
    
    elif level == 2:
        numEnemy1 = 0
        numEnemy2 = 0
        numSpEnemy = 0
        background = pygame.image.load("Image/Background/space.png").convert()
        bossImg = pygame.image.load("Image/Boss/bear.png").convert_alpha()
        enemy1Img = pygame.image.load("Image/Enemies/enemyShip.png").convert_alpha()
        enemy2Img = pygame.image.load("Image/Enemies/enemyRoll.png").convert_alpha()
        spEnemyImg = pygame.image.load("Image/Enemies/enemyShip.png").convert_alpha()

        pygame.time.set_timer(USEREVENT + 1, random.randrange(400, 1500))

    elif level == 3:
        numEnemy1 = 0
        numEnemy2 = 0
        numSpEnemy = 0
        background = pygame.image.load("Image/Background/space.png").convert()
        bossImg = pygame.image.load("Image/Boss/bear.png").convert_alpha()
        enemy1Img = pygame.image.load("Image/Enemies/enemyShip.png").convert_alpha()
        enemy2Img = pygame.image.load("Image/Enemies/enemyRoll.png").convert_alpha()
        spEnemyImg = pygame.image.load("Image/Enemies/enemyShip.png").convert_alpha()

        pygame.time.set_timer(USEREVENT + 1, random.randrange(400, 1500))

    # Game cycle
    while not done:
        # cycle of events
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT or ev.type == KEYDOWN and ev.key == K_ESCAPE:
                pygame.quit()
            elif ev.type == pygame.KEYDOWN and ev.key == K_SPACE and len(bullets) < player.maxNumBull:
                player.shoot(bulletImg)
                
            # events dedicated to the generation of enemies in each level
            elif ev.type == USEREVENT + 1:
                if level == 1:
                    if numEnemy1 < 10:
                        pygame.time.set_timer(USEREVENT + 1, random.randrange(700, 1000))
                        invader = Invader(enemy1Img, (random.randrange(0, screen.get_width() - 98 + 1), -1), (0, 4), 1, 10, 10)
                        allEnemies.add(invader)
                        numEnemy1 += 1
                
                    elif numEnemy1 == 10:
                        pygame.time.set_timer(USEREVENT + 1, 0)
                        pygame.time.set_timer(USEREVENT + 2, 1500)
                        numEnemy1 = 0

            elif ev.type == USEREVENT + 2:
                if level == 1:
                    if numEnemy2 < 14:
                        pygame.time.set_timer(USEREVENT + 2, random.randrange(2000, 3000))
                        rollers1 = Rollers(enemy2Img, (0, -1), (4, 0), 2, 20, 20, 0)
                        allEnemies.add(rollers1)
                        numEnemy2 += 1
                        rollers2 = Rollers(enemy2Img, (screen.get_width() - 98 + 1, -1), (4, 0), 2, 20, 20, -180)
                        allEnemies.add(rollers2)
                        numEnemy2 += 1
               
                    elif numEnemy2 == 14:
                        pygame.time.set_timer(USEREVENT + 2, 0)
                        pygame.time.set_timer(USEREVENT + 3, 8000)
                        numEnemy2 = 0

            elif ev.type == USEREVENT + 3:
                if level == 1:
                    if numEnemy1 < 10:
                        pygame.time.set_timer(USEREVENT + 3, random.randrange(900, 1200))
                        invader = Invader(enemy1Img, (random.randrange(0, screen.get_width() - 98 + 1), -1), (0, 4), 2, 30, 20)
                        allEnemies.add(invader)
                        numEnemy1 += 1
                
                    elif numEnemy1 == 10:
                        pygame.time.set_timer(USEREVENT + 3, 0)
                        pygame.time.set_timer(USEREVENT + 4, 7000)
           
            elif ev.type == USEREVENT + 4:
                if level == 1:
                    if not existsBoss:
                        boss = Gorgodusa(bossImg, (400, 75), 400, 400, 30, 150, (5, 0), "Gorgodusa")
                        bosses.add(boss)
                        existsBoss = True
                elif level == 2:
                    if not existsBoss:
                        boss = Golem(bossImg2, (400, 75), 500, 500, 30, 250, (3, 0), "Golem")
                        bosses.add(boss)
                        existsBoss = True
                elif level == 3:
                    if not existsBoss:
                        boss = Bidramon(bossImg3, (400, 75), 600, 600, 30, 400, (5, 0), "Bidramon")
                        bosses.add(boss)
                        existsBoss = True

            elif ev.type == USEREVENT + 5:
                if level == 1:
                    rare = Rare(pygame.image.load("Image/Enemies/enemyShip.png").convert_alpha(), (-1, random.randrange(ciao.get_height(), screen.get_width()/2, 10)), 1, 150)
                    allEnemies.add(rare)
                    pygame.time.set_timer(USEREVENT + 5, random.randrange(25000, 35000))

        # movement and collision of enemies
        hits = pygame.sprite.groupcollide(allEnemies, bullets, False, True)
        for hit in hits:
            hit.lives -= 1
            if hit.lives <= 0:
                updateDex(enemyDex, hit.name)
                score += hit.score
                hit.kill()
                if random.random() > 0.1:
                    power = Power(hit.rect.center)
                    allSprites.add(power)
                    powers.add(power)

        hits = pygame.sprite.groupcollide(eBullets, bullets, False, True)
        for hit in hits:
            hit.kill()
        
        hits = pygame.sprite.spritecollide(player, allEnemies, False)
        for hit in hits:
            score += hit.score
            updateDex(enemyDex, hit.name)
            hit.kill()
            player.shield -= 20
            if player.shield <= 0:
                player.shield = 0
                player.lives -= 1
                if player.lives == 0:
                    done = True
                    win = False
                player.hide()

        hits = pygame.sprite.spritecollide(player, eBullets, False)
        for hit in hits:
            hit.kill()
            player.shield -= hit.damage
            if player.shield <= 0:
                player.shield = 0
                player.lives -= 1
                if player.lives == 0:
                    done = True
                    win = False
                player.hide()

        hits = pygame.sprite.spritecollide(player, powers, True)
        for hit in hits:
            usePowerUp(hit, player)
        
        hits = pygame.sprite.spritecollide(player, bosses, False)
        for hit in hits:
            player.shield -= hit.damage
            if player.shield <= 0:
                player.shield = 0
                player.lives -= 1
                if player.lives == 0:
                    done = True
                    win = False
                player.hide()

            hit.lives -= player.shield/2
            if hit.lives <= 0:
                hit.kill()
                done = True
                win = True

        hits = pygame.sprite.spritecollide(player, obstacles, False)
        for hit in hits:
            if hit.dangerous:
                hit.hitPlayer()
                player.shield -= hit.damage
                hit.timeToNewDamage = pygame.time.get_ticks()
                if player.shield <= 0:
                    player.shield = 0
                    player.lives -= 1
                    if player.lives == 0:
                        done = True
                        win = False
                    player.hide()

        pygame.sprite.groupcollide(bullets, obstacles, True, False)

        if existsBoss:
            space2 = 0
            if boss.split:
                bidramon1 = Bidramon(boss.image, (200, 75), 100, 100, 30, 200, (5, 0), "Bidramon1")
                bidramon1.resistence = 30
                bidramon1.shotDelay = 1000
                bosses.add(bidramon1)
                bidramon2 = Bidramon(boss.image, (600, 75), 100, 100, 30, 200, (5, 0), "Bidramon2")
                bidramon2.resistence = 30
                bidramon2.shotDelay = 1000
                bosses.add(bidramon2)

            for boss in bosses:
                hits = pygame.sprite.spritecollide(boss, bullets, True)
                for hit in hits:
                    boss.lives -= (hit.bossDamage - boss.resistence)
                    boss.hit()
                    if boss.lives <= 0:
                        score += boss.score
                        updateDex(enemyDex, boss.name)
                        boss.kill()
                        done = True
                        win = True
                
                drawShield(screen, 580, 40 + space2, boss.lives, pygame.image.load("Image/Enemies/enemyShip.png").convert_alpha(), True, boss.maxLife, boss.name)
                space2 += 50

        #
        # screen update
        drawLives(screen, 780, 580, player.lives, playerImg)
        drawShield(screen, 40, 558, player.shield, pygame.image.load("Image/Player/shield.png").convert_alpha(), False, player.maxLife)
        drawText(screen, "Score: {}".format(score), 32, 50, 50, WHITE, False)
        allSprites.draw(screen)
        allEnemies.draw(screen)
        eBullets.draw(screen)
        bosses.draw(screen)
        obstacles.draw(screen)
        
        allSprites.update()
        allEnemies.update()
        obstacles.update()
        eBullets.update()
        bosses.update()
        updateGameScreen(background)
        updateScreen()

        if win == True:
            saved((allEnemies, allSprites, bosses, eBullets, text, obstacles), level, background)
        
        elif win == False:
            showGOScreen(score, (allEnemies, allSprites, eBullets, bosses, obstacles), player, background)

# SPAST

# risorse grafiche
titleImg = pygame.image.load("Image/Window/title.png").convert_alpha()      # titolo of Game

playerImg = pygame.image.load("Image/Player/player.png").convert_alpha()

mainMenuImage = pygame.image.load("Image/Background/desert.jpg").convert()         # main menu screen

# textual resources
command = ["Controls:", "  D - Move to Right", "  A - Move to Left", "  SPACE - Fire!", "ESC - Quit"] # lista dei comandi di gioco
for i in range(5):
    drawText(window, command[i], 32, 20, 250 + i*50, WHITE, False)

enemyDex = ["---", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---"]
    
# Varriable
level = 1                   # Game level
score = 0                   # Game score

# creation of the game window
screen = pygame.Surface((800, 600))     # Play area
border = pygame.Surface((820, 620))     # edge
title = pygame.Surface((342, 128))      # title area

#
# creating containers for sprites
allSprites = pygame.sprite.Group()
allEnemies = pygame.sprite.Group()

text = pygame.sprite.Group()
bosses = pygame.sprite.Group()
powers = pygame.sprite.Group()
bullets = pygame.sprite.Group()
eBullets = pygame.sprite.Group()
obstacles = pygame.sprite.Group()

#
# power up creation
poweImage = {}                                                                          
poweImage["speed"] = pygame.image.load("Image/Player/speed.png").convert_alpha()
poweImage["shield"] = pygame.image.load("Image/Player/shield.png").convert_alpha()
poweImage["extra"] = pygame.image.load("Image/Player/extraLife.png").convert_alpha()
poweImage["toxic"] = pygame.image.load("Image/Player/toxic.png").convert_alpha()
poweImage["newGun"] = pygame.image.load("Image/Player/newGun.png").convert_alpha()

# Game cycle
updateGameScreen(mainMenuImage)

player = Player(playerImg)              # player creation
allSprites.add(player)

mainMenu()
