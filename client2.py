import pygame
import tkinter as tk
from pygame.locals import *
import pygame_classes
from network import Network
import os

CENTER_W = -1
CENTER_H = -1


def main():
    root = tk.Tk()
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (int(root.winfo_screenwidth()/2), 0)
    pygame.init()
    screen = pygame.display.set_mode((int(pygame.display.
                                          Info().current_w / 2),
                                      int(pygame.display.Info().current_h)))

    background = pygame.Surface(screen.get_size())
    background = background.convert_alpha()
    background.fill((39, 174, 96))

    CENTER_W = int(pygame.display.Info().current_w / 2)
    CENTER_H = int(pygame.display.Info().current_h / 2)

    GREEN = 174
    black_car1 = 53
    black_car2 = 91

    clock = pygame.time.Clock()
    running = True
    font = pygame.font.Font(None, 50)

    network = Network()
    car = pygame_classes.from_state(network.get_player())
    cam = pygame_classes.Camera()
    target = pygame_classes.Finish(8, 9)
    bound_alert = pygame_classes.BoundsAlert()
    # time_alert = pygame_classes.TimeAlert()
    win_alert = pygame_classes.WinAlert()

    map_s = pygame.sprite.Group()
    player_s = pygame.sprite.Group()
    tracks_s = pygame.sprite.Group()
    target_s = pygame.sprite.Group()
    # timer_alert_s = pygame.sprite.Group()
    bound_alert_s = pygame.sprite.Group()
    win_alert_s = pygame.sprite.Group()

    """
    map_tile = ['mud7.png', 'mud1.png', 'mud2.png', 'mud3.png', 'mud4.png', 'mud5.png', 'mud6.png', 'race.png',
                'tree.png', 'tribune.png', 'grass.png', 'band.png']

    map = [
        [7, 3, 1, 1, 1, 4, 8, 8, 8, 11],
        [7, 2, 7, 3, 1, 6, 8, 8, 8, 11],
        [7, 2, 7, 2, 10, 10, 10, 8, 8, 11],
        [3, 6, 10, 10, 10, 3, 4, 8, 8, 11],
        [5, 1, 1, 1, 1, 6, 2, 8, 8, 11],
        [7, 9, 9, 9, 9, 9, 2, 8, 8, 11],
        [7, 3, 1, 4, 7, 7, 5, 4, 8, 11],
        [7, 2, 10, 5, 1, 1, 1, 6, 8, 11],
        [7, 5, 1, 1, 1, 1, 1, 1, 4, 11],
        [7, 9, 9, 9, 9, 9, 9, 9, 0, 11]
    ]
    """
    map_tile = ['mud7.png', 'mud1.png', 'mud2.png', 'mud3.png', 'mud4.png', 'mud5.png', 'mud6.png', 'race.png',
                'tree.png', 'tribune.png', 'grass.png', 'band.png']

    map = [
        [11, 3, 4, 10, 4, 10, 8, 10, 10, 11],
        [11, 2, 2, 3, 1, 1, 4, 7, 7, 11],
        [11, 10, 2, 2, 5, 3, 2, 3, 4, 11],
        [11, 8, 5, 6, 10, 9, 5, 4, 1, 11],
        [8, 10, 8, 10, 2, 3, 3, 3, 6, 8],
        [8, 9, 9, 9, 1, 8, 7, 7, 7, 8],
        [11, 2, 3, 3, 6, 8, 2, 3, 4, 11],
        [11, 1, 7, 7, 7, 7, 1, 10, 1, 11],
        [11, 5, 3, 3, 3, 3, 6, 10, 1, 11],
        [11, 10, 10, 8, 8, 10, 10, 10, 0, 11]
    ]

    pygame_classes.map_files.clear()

    for tile_num in range(0, len(map_tile)):
        pygame_classes.map_files.append(pygame_classes.load_image(map_tile[tile_num], False))
    for x in range(0, 10):
        for y in range(0, 10):
            map_s.add(pygame_classes.Map(map[x][y], x * 500, y * 500))

    pygame_classes.initialize_tracks()
    target_s.add(target)
    # timer_alert_s.add(time_alert)
    bound_alert_s.add(bound_alert)
    win_alert_s.add(win_alert)
    player_s.add(car)
    cam.set_position(car.x, car.y)

    win = None
    collided = False
    while running:

        car2 = pygame_classes.from_state(network.send(car.get_state()))
        car2.steer_left()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    car.reset()
                    car.x = 350
                    car.y = 250
                    target.reset()
                    win = None
                    collided = False
                elif event.key == pygame.K_ESCAPE:
                    running = False
                    break

        keys = pygame.key.get_pressed()
        if target.time_left > 0 and win == None:
            if keys[K_a]:
                car.steer_left()
            if keys[K_d]:
                car.steer_right()
            if keys[K_w]:
                car.accelerate()
            else:
                car.soften()
            if keys[K_s]:
                car.deaccelerate()


        cam.set_position(car.x, car.y)

        # text_timer = font.render(
        #     'Timer: ' + str(int((target.time_left / 60) / 60)) + ":" + str(int((target.time_left / 60) % 60)), 1,
        #     (255, 255, 255))

        screen.blit(background, (0, 0))

        map_s.update(cam.x, cam.y)
        map_s.draw(screen)

        car.grass(screen.get_at((int(CENTER_W - 5), int(CENTER_H - 5))).g, GREEN)

        if car.tracks:
            tracks_s.add(pygame_classes.Track(cam.x + CENTER_W, cam.y + CENTER_H, car.dir))

        tracks_s.update(cam.x, cam.y)
        tracks_s.draw(screen)

        player_s.update(cam.x, cam.y)
        player_s.draw(screen)

        car2.update2(cam.x, cam.y)
        car2.draw2(screen)

        target_s.update(cam.x, cam.y)
        target_s.draw(screen)

        if pygame.sprite.collide_rect(car2, car):
            car.x = car.x + car.rect.width


        if pygame_classes.breaking(car.x + CENTER_W, car.y + CENTER_H) or car.border(
                screen.get_at((int(CENTER_W), int(CENTER_H))).g, GREEN, GREEN):
            car.speed = 0
            win = False
            bound_alert_s.update()
            bound_alert_s.draw(screen)

        # if target.time_left == 0:
        #     timer_alert_s.draw(screen)
        #     car.speed = 0
        #     win = False

        if pygame.sprite.spritecollide(car, target_s, True):
            car.speed = 0
            win = True
            collided = True

        # if collided:
        #     win_alert_s.draw(screen)
        #     pygame.time.delay(1000)


        # screen.blit(text_timer, (CENTER_W - 200, CENTER_H - 200))
        pygame.display.flip()

        clock.tick(64)


main()
