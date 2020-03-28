import pygame, math, sys, level1, time
from pygame.locals import *
"""
pygame.init()
screen = pygame.display.set_mode((1000, 562))
pygame.display.set_caption('Racing')
font = pygame.font.Font(None, 75)
text = font.render('Get ready for level 1', True, (255,255,255))
while True:
    screen.fill((0,0,0))
    img = pygame.image.load("images/menu.png")
    screen.blit(img, (0, 0))
    for event in pygame.event.get():
                if not hasattr(event, 'key'): continue
                if event.key == K_SPACE:
                    screen.fill((0, 0, 0))
                    screen.blit(text, (500 - text.get_width() // 2, 281 - text.get_height() // 2))
                    pygame.display.update()
                    pygame.time.delay(2000)
                    level1.level1()
                if event.key == K_ESCAPE:
                    sys.exit(0)
    pygame.display.flip() 
    """