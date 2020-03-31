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
# Import game modules.
from loader import load_image
from car_customization import change_color

TRAFFIC_COUNT = 45
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

    green_valueG = 182
    geen_valueW = 238
    clock = pygame.time.Clock()
    running = True
    font = pygame.font.Font(None, 50)
    car = player.Player(change_color())
    cam = camera.Camera()
    target = mode.Finish(8, 9)
    bound_alert = bounds.Alert()
    time_alert = timeout.Alert()
    # create sprite groups.
    map_s = pygame.sprite.Group()
    player_s = pygame.sprite.Group()
    tracks_s = pygame.sprite.Group()
    target_s = pygame.sprite.Group()
    timer_alert_s = pygame.sprite.Group()
    bound_alert_s = pygame.sprite.Group()

    map_tile = ['sand0.png', 'sand1.png', 'sand2.png', 'sand3.png', 'sand4.png', 'sand5.png', 'sand6.png', 'race.png',
                'tree.png', 'tribune.png', 'grass.png', 'band.png']
    # Map to tile.

    # tilemap.
    map_1 = [
        [11, 10, 10, 2, 4, 10, 8, 10, 10, 11],
        [11, 8, 10, 1, 1, 7, 7, 7, 7, 11],
        [11, 10, 8, 1, 5, 3, 3, 3, 4, 11],
        [11, 8, 10, 10, 10, 9, 9, 9, 1, 11],
        [8, 10, 8, 10, 2, 3, 3, 3, 6, 8],
        [8, 9, 9, 9, 1, 8, 7, 7, 7, 8],
        [11, 2, 3, 3, 6, 8, 2, 3, 4, 11],
        [11, 1, 7, 7, 7, 7, 1, 10, 1, 11],
        [11, 5, 3, 3, 3, 3, 6, 10, 1, 11],
        [11, 10, 10, 8, 8, 10, 10, 10, 0, 11]
    ]

    # generate tiles
    for tile_num in range(0, len(map_tile)):
        maps.map_files.append(load_image(map_tile[tile_num], False))
    for x in range(0, 10):
        for y in range(0, 10):
            map_s.add(maps.Map(map_1[x][y], x * 500, y * 500))

    # load tracks
    tracks.initialize()
    # load finish
    target_s.add(target)
    # load alerts
    timer_alert_s.add(time_alert)
    bound_alert_s.add(bound_alert)

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
        if (car.tracks):
            tracks_s.add(tracks.Track(cam.x + CENTER_W, cam.y + CENTER_H, car.dir))

        # Just render..
        tracks_s.update(cam.x, cam.y)
        tracks_s.draw(screen)

        player_s.update(cam.x, cam.y)
        player_s.draw(screen)

        target_s.update(cam.x, cam.y)
        target_s.draw(screen)

        # Conditional renders.
        if bounds.breaking(car.x + CENTER_W, car.y + CENTER_H) or car.border(
                screen.get_at((int(CENTER_W), int(CENTER_H))).g, green_valueG, geen_valueW):
            car.speed = 0
            win = False
            bound_alert_s.update()
            bound_alert_s.draw(screen)
        if (target.timeleft == 0):
            timer_alert_s.draw(screen)
            car.speed = 0
            win = False

        screen.blit(text_timer, (CENTER_W - 600, CENTER_H - 300))
        pygame.display.flip()

        # Check collision!!

        if pygame.sprite.spritecollide(car, target_s, True):
            car.speed = 0
            win = True
            timer_alert_s.draw(screen)

        clock.tick(64)
