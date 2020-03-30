import pygame
import os
import level3
import level1
import level2
from car_customization import customize_car
import sys

# Game Initialization
pygame.init()

# Center the Game Application
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Game Resolution
screen_width=pygame.display.Info().current_w
screen_height=pygame.display.Info().current_h
screen = pygame.display.set_mode((screen_width, screen_height))

def text_format(message, textFont, textSize, textColor):
    newFont=pygame.font.Font(textFont, textSize)
    newText=newFont.render(message, 0, textColor)

    return newText


# Colors
white=(255, 255, 255)
black=(0, 0, 0)
gray=(50, 50, 50)
red=(255, 0, 0)
green=(0, 255, 0)
blue=(0, 0, 255)
yellow=(255, 255, 0)

# Game Fonts
font = "font.ttf"


# Game Framerate
clock = pygame.time.Clock()
FPS=30

# Main Menu
def main_menu():

    menu=True
    selected="start"

    while menu:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP and selected=="change":
                    selected="start"
                elif event.key==pygame.K_UP and selected=="quit":
                    selected="change"
                elif event.key==pygame.K_DOWN and selected=="start":
                    selected="change"
                elif event.key==pygame.K_DOWN and selected=="change":
                    selected="quit"
                if event.key==pygame.K_RETURN:
                    if selected=="start":
                        level2.main()
                    if selected=="change":
                       customize_car()
                    if selected=="quit":
                        pygame.quit()
                        quit()



        # Main Menu UI
        screen.fill((0, 0, 0))
        img = pygame.image.load("Images/menu.png").convert()
        img = pygame.transform.scale(img, (screen_width, screen_height))
        screen.blit(img, (0, 0))
        title=text_format("Racing game", font, 180, red)
        if selected=="start":
            text_start=text_format("START  YOUR  RACE", font,100 , white)
        else:
            text_start = text_format("START  YOUR  RACE", font, 100, black)
        if selected=="change":
            text_change=text_format("CUSTOMIZE  YOUR  CAR", font,100 , white)
        else:
            text_change = text_format("CUSTOMIZE  YOUR  CAR", font, 100, black)
        if selected=="quit":
            text_quit=text_format("QUIT", font, 100, white)
        else:
            text_quit = text_format("QUIT", font, 100, black)

        title_rect=title.get_rect()
        start_rect=text_start.get_rect()
        change_rect=text_change.get_rect()
        quit_rect=text_quit.get_rect()

        # Main Menu Text
        screen.blit(title, (screen_width/2 - (title_rect[2]/2), 50))
        screen.blit(text_start, (screen_width/2 - (start_rect[2]/2), 300))
        screen.blit(text_change, (screen_width / 2 - (change_rect[2] / 2), 450))
        screen.blit(text_quit, (screen_width/2 - (quit_rect[2]/2), 600))
        pygame.display.update()
        clock.tick(FPS)
        pygame.display.set_caption("Racing Game - main menu ")

        pygame.display.flip()

#Initialize the Game
main_menu()
pygame.quit()
sys.exit(0)
quit()
