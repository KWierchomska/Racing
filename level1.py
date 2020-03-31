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
import level2
# Import game modules.
from loader import load_image
from car_customization import change_color

TRAFFIC_COUNT = 45
CENTER_W = -1
CENTER_H = -1


def collision(car): #TODO slower bounce off
    x = car.x
    y = car.y
    if x <= 700 and 500 <= y <= 3400:
        car.impact()
        car.x += 75
    elif 1000 <= x <= 2000 and 500 <= y <= 3400:
        car.impact()
        car.x -= 75
    elif y <= 3500 and 1000 <= x <= 3100:
        car.impact()
        car.y += 75
    elif y >= 3800 and 1000 <= x <= 3100:
        car.impact()
        car.y -= 75
    elif 3200 >= x >= 3000 and 0 <= y <= 3500:
        car.impact()
        car.x += 75
    elif x >= 3550 and 0 <= y <= 3500:
        car.impact()
        car.x -= 75
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

    clock = pygame.time.Clock()
    running = True
    font = pygame.font.Font(None, 24)
    car = player.Player(change_color())
    car.dir = 180
    car.steer_left()
    cam = camera.Camera()
    target = mode.Finish(8, 1) #TODO: not working
    bound_alert = bounds.Alert()
    time_alert = timeout.Alert()
    # create sprite groups.
    map_s = pygame.sprite.Group()
    player_s = pygame.sprite.Group()
    tracks_s = pygame.sprite.Group()
    target_s = pygame.sprite.Group()
    timer_alert_s = pygame.sprite.Group()
    bound_alert_s = pygame.sprite.Group()

    map_tile = ['asphalt0.png', 'asphalt1.png', 'asphalt2.png', 'asphalt3.png', 'asphalt4.png', 'race.png', 'tree.png',
                'tribune.png', 'grass.png', 'band.png']
    # Map to tile.

    # tilemap.
    map_1 = [
        [5, 8, 5, 6, 4, 8, 8, 8, 8, 8],
        [5, 8, 5, 6, 7, 7, 7, 7, 0, 5],
        [5, 8, 5, 1, 5, 3, 3, 5, 1, 5],
        [8, 8, 5, 1, 5, 9, 9, 5, 1, 5],
        [8, 8, 5, 1, 5, 3, 3, 5, 1, 5],
        [8, 8, 5, 1, 5, 8, 7, 5, 1, 5],
        [5, 6, 5, 1, 8, 8, 2, 8, 1, 5],
        [5, 6, 5, 1, 7, 7, 7, 7, 1, 5],
        [5, 6, 5, 2, 3, 3, 3, 3, 4, 9],
        [5, 6, 5, 8, 8, 8, 8, 8, 8, 9]
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
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    car.reset()
                    car.dir=180
                    car.steer_left()
                    target.reset()
                elif event.key == pygame.K_ESCAPE:
                    running = False
                    break

        # Check for key input. (KEYDOWN, trigger often)

        keys = pygame.key.get_pressed()
        if target.timeleft > 0:
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

        # Show text data. TODO:text is not appearing on screen
        text_fps = font.render('FPS: ' + str(int(clock.get_fps())), 1, (255, 255, 255))
        textpos_fps = text_fps.get_rect(centery=25, centerx=60)

        text_score = font.render('Score: ' + str(target.score), 1, (255, 255, 255))
        textpos_score = text_fps.get_rect(centery=45, centerx=60)

        text_timer = font.render(
            'Timer: ' + str(int((target.timeleft / 60) / 60)) + ":" + str(int((target.timeleft / 60) % 60)), 1,
            (255, 255, 255))
        textpos_timer = text_fps.get_rect(centery=65, centerx=60)

        # Render Scene.
        screen.blit(background, (0, 0))

        # cam.set_pos(car.x, car.y)

        map_s.update(cam.x, cam.y)
        map_s.draw(screen)

        # Conditional renders/effects

        collision(car)
        if car.tracks:
            tracks_s.add(tracks.Track(cam.x + CENTER_W, cam.y + CENTER_H, car.dir))

        # Just render..
        tracks_s.update(cam.x, cam.y)
        tracks_s.draw(screen)

        player_s.update(cam.x, cam.y)
        player_s.draw(screen)

        target_s.update(cam.x, cam.y)
        target_s.draw(screen)

        # Conditional renders.
        if bounds.breaking(car.x + CENTER_W, car.y + CENTER_H):
            bound_alert_s.update()
            bound_alert_s.draw(screen)
        if target.timeleft == 0:
            timer_alert_s.draw(screen)
            car.speed = 0
            text_score = font.render('Final Score: ' + str(target.score), 1, (224, 16, 16))
            textpos_score = text_fps.get_rect(centery=CENTER_H + 56, centerx=CENTER_W - 20)

        # Blit Blit..
        screen.blit(text_fps, textpos_fps)
        screen.blit(text_score, textpos_score)
        screen.blit(text_timer, textpos_timer)
        pygame.display.flip()

        # Check collision!!

        if pygame.sprite.spritecollide(car, target_s, True): #TODO: sth not working after collision
            car.speed = 0
            pygame.time.delay(2000)
            level2.main()

        clock.tick(64)


