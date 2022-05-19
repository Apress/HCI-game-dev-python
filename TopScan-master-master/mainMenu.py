import random
import pygame
from pygame.locals import *

pygame.init()
pygame.mixer.music.load("Music/menuTrack.ogg")          # load the soundtrack
window = pygame.display.set_mode((0, 0), FULLSCREEN)    # creation of the game window

# window pictures
titleImg = pygame.image.load("Image/Window/title.png").convert_alpha()  

#
# background images
desert = pygame.image.load("Image/Background/desert.jpg").convert()

#
# text creation

font = pygame.font.SysFont("Arial", 32, bold = True)    # loads the font into memory

ngSurf = font.render("New Game", True, (255, 255, 255))         # renders the writing with the loaded font
toContSurf = font.render("Continue", True, (255, 255, 255))
saveSurf = font.render("Vuoi Salvare?", True, (255, 255, 255))
yesSurf = font.render("Yes", True, (255, 255, 255))
noSurf = font.render("No", True, (255, 255, 255))

# creation of groups containing textual sprites

text = pygame.sprite.Group() 
text2 = pygame.sprite.Group()

# creation of text sprites

ng = pygame.sprite.Sprite(text)
ng.image = ngSurf
ng.rect = ngSurf.get_rect()
ng.rect.topleft = (900, 600)
toContinue = pygame.sprite.Sprite(text)
toContinue.image = toContSurf
toContinue.rect = toContSurf.get_rect()
toContinue.rect.topleft = (900, 650)

save = pygame.sprite.Sprite(text2)
save.image = saveSurf
save.rect = saveSurf.get_rect()
save.rect.topleft = (900, 500)
yes = pygame.sprite.Sprite(text2)
yes.image = yesSurf
yes.rect = yesSurf.get_rect()
yes.rect.topleft = (950, 600)
no = pygame.sprite.Sprite(text2)
no.image = noSurf
no.rect = noSurf.get_rect()
no.rect.topleft = (950, 650)

