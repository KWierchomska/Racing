from random import randint

import mode
import pygame
import sys

from pygame.locals import *

import bounds
import camera
import maps
import player
import timeout
import tracks
import race_win
# Import game modules.
from loader import load_image
from car_customization import change_color

CENTER_W = -1
CENTER_H = -1


# Main function.
def main():
    # initialize objects.
    pygame.init()

    screen = pygame.display.set_mode((pygame.display.Info().current_w,
                                      pygame.display.Info().current_h),
                                     pygame.FULLSCREEN)

    background = pygame.Surface(screen.get_size())
    background = background.convert_alpha()
    background.fill((39, 174, 96))

    CENTER_W = int(pygame.display.Info().current_w / 2)
    CENTER_H = int(pygame.display.Info().current_h / 2)

    green_valueG = 174
    geen_valueW = 192
    clock = pygame.time.Clock()
    running = True
    font = pygame.font.Font(None, 50)
    car = player.Player(change_color())
    cam = camera.Camera()
    target = mode.Finish(8, 9)
    bound_alert = bounds.Alert()
    time_alert = timeout.Alert()
    win_alert = race_win.Win()

    # create sprite groups.

    map_tile = ['sand0.png', 'grass1.png', 'grass2.png', 'grass3.png', 'grass4.png', 'grass5.png', 'grass6.png',
                'race.png', 'tree.png', 'tribune.png', 'grass.png', 'band.png']
    # Map to tile.

    # tilemap.
    map_1 = [
        [11, 9, 3, 3, 4, 3, 3, 2, 9, 11],
        [11, 4, 3, 2, 1, 7, 7, 5, 2, 11],
        [11, 1, 7, 1, 1, 7, 7, 8, 1, 11],
        [11, 1, 7, 7, 1, 7, 7, 4, 6, 11],
        [11, 1, 7, 7, 1, 7, 7, 1, 7, 11],
        [11, 5, 3, 3, 6, 7, 7, 1, 7, 11],
        [11, 4, 3, 3, 2, 4, 3, 6, 7, 11],
        [11, 1, 7, 7, 5, 6, 8, 8, 7, 11],
        [11, 5, 3, 3, 3, 2, 8, 8, 7, 11],
        [11, 10, 10, 8, 8, 5, 3, 3, 3, 11]
    ]

    map_s = pygame.sprite.Group()
    player_s = pygame.sprite.Group()
    tracks_s = pygame.sprite.Group()
    target_s = pygame.sprite.Group()
    timer_alert_s = pygame.sprite.Group()
    bound_alert_s = pygame.sprite.Group()
    bomb_s = pygame.sprite.Group()
    win_alert_s = pygame.sprite.Group()

    # generate tiles
    for tile_num in range(0, len(map_tile)):
        maps.map_files.append(load_image(map_tile[tile_num], False))
    for x in range(0, 10):
        for y in range(0, 10):
            map_s.add(maps.Map(map_1[x][y], x * 500, y * 500))

    for i in range(6):
        x = randint(0, 9)
        y = randint(0, 9)
        while map_1[x][y] != 1:
            x = randint(0, 9)
            y = randint(0, 9)
        bomb = mode.Bomb(y, x)
        bomb_s.add(bomb)

    # load tracks
    tracks.initialize()
    target_s.add(target)
    timer_alert_s.add(time_alert)
    bound_alert_s.add(bound_alert)
    win_alert_s.add(win_alert)

    player_s.add(car)

    cam.set_position(car.x, car.y)

    win = None

    while running:
        # Render loop.

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    car.reset()
                    target.reset()
                    bomb.reset()
                    win = None
                elif event.key == pygame.K_ESCAPE:
                    running = False
                    break

        # Check for key input. (KEYDOWN, trigger often)
        keys = pygame.key.get_pressed()
        if target.timeleft > 0 and win == None:
            if keys[K_LEFT]:
                car.steer_left()
            if keys[K_RIGHT]:
                car.steer_right()
            if keys[K_UP]:
                car.accelerate()
            else:
                car.soften()
            if keys[K_DOWN]:
                car.deaccelerate()

        cam.set_position(car.x, car.y)

        text_timer = font.render(
            'Timer: ' + str(int((target.timeleft / 60) / 60)) + ":" + str(int((target.timeleft / 60) % 60)), 1,
            (255, 255, 255))


        # Render Scene.
        screen.blit(background, (0, 0))

        map_s.update(cam.x, cam.y)
        map_s.draw(screen)

        # Conditional renders/effects
        if car.tracks:
            tracks_s.add(tracks.Track(cam.x + CENTER_W, cam.y + CENTER_H, car.dir))

        # Just render..
        tracks_s.update(cam.x, cam.y)
        tracks_s.draw(screen)

        player_s.update(cam.x, cam.y)
        player_s.draw(screen)

        target_s.update(cam.x, cam.y)
        target_s.draw(screen)

        bomb_s.update(cam.x, cam.y)
        bomb_s.draw(screen)

        # Conditional renders.
        if bounds.breaking(car.x + CENTER_W, car.y + CENTER_H) or car.border(
                screen.get_at((int(CENTER_W), int(CENTER_H))).g, green_valueG, geen_valueW):
            car.speed = 0
            win = False
            bound_alert_s.update()
            bound_alert_s.draw(screen)
        if target.timeleft == 0:
            timer_alert_s.draw(screen)
            win = False
            car.speed = 0

        screen.blit(text_timer, (CENTER_W - 600, CENTER_H - 300))
        pygame.display.flip()

        # Check collision!!
        if pygame.sprite.spritecollide(car, bomb_s, True):
            car.speed = 0
            win = False
            bound_alert_s.update() #TODO: not working
            bound_alert_s.draw(screen)

        if pygame.sprite.spritecollide(car, target_s, True):
            win = True
            car.speed = 0
            bound_alert_s.update() #TODO: not working too
            bound_alert_s.draw(screen)

        clock.tick(64)
