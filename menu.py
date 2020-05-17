import pygame
import os
import car_customization
import level1
import sys
import pygame_classes
<<<<<<< HEAD
=======
from multiprocessing import Pool
>>>>>>> a14be3d5d0958f55388b0ef3f6932b0636124fc0

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Game Initialization
pygame.init()

# Center the Game Application
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Game Resolution
screen_width = int(pygame.display.Info().current_w)
screen_height = int(pygame.display.Info().current_h)
screen = pygame.display.set_mode((screen_width, screen_height))

# Game Fonts
font = "font.ttf"

# Game Framerate
clock = pygame.time.Clock()
FPS = 30


# Main Menu
def main_menu():
    menu = True
<<<<<<< HEAD
=======
    processes = ('server.py', 'process_helper.py')
>>>>>>> a14be3d5d0958f55388b0ef3f6932b0636124fc0
    texts = ["START  YOUR  RACE", "TWO PLAYERS MODE", "CUSTOMIZE  YOUR  CAR", "QUIT"]
    i = 0
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if i > 0:
                        i -= 1
                    else:
                        i = len(texts) - 1
                elif event.key == pygame.K_DOWN:
                    if i < len(texts) - 1:
                        i += 1
                    else:
                        i = 0
                if event.key == pygame.K_RETURN:
                    if i == 0:
                        level1.main()
                    elif i == 1:
                        print("You chose game mode for 2 players")
<<<<<<< HEAD
                        os.system('python {}'.format('two_players_mode.py'))
=======
                        pool = Pool(processes=4)
                        pool.map(run_process, processes)
>>>>>>> a14be3d5d0958f55388b0ef3f6932b0636124fc0
                    elif i == 2:
                        car_customization.customize_car()
                    elif i == 3:
                        pygame.quit()
                        quit()

        screen.fill((0, 0, 0))
        img = pygame.image.load("Images/menu.png").convert()
        img = pygame.transform.scale(img, (screen_width, screen_height))
        screen.blit(img, (0, 0))

        # Main Menu Text
        title = pygame_classes.text_format("Racing game", font, 150, red)
        title_rect = title.get_rect()
        screen.blit(title, (screen_width / 2 - (title_rect[2] / 2), screen_height / 6))  # / 8

        for text_index in range(len(texts)):
            col = white if text_index == i else black
            text = pygame_classes.show_text(texts[text_index], font, 100, col)
            text_rect = text.get_rect()
            screen.blit(text, (screen_width / 2 - (text_rect[2] / 2), (text_index + 3) * screen_height / 8))

        pygame.display.update()
        clock.tick(FPS)

        pygame.display.set_caption("Racing Game - main menu ")
        pygame.display.flip()


main_menu()
pygame.quit()
sys.exit(0)
