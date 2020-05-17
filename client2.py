import pygame
<<<<<<< HEAD
=======
import tkinter as tk
from pygame.locals import *
>>>>>>> a14be3d5d0958f55388b0ef3f6932b0636124fc0
import pygame_classes
from network import Network
import os

CENTER_W = -1
CENTER_H = -1


def main():
<<<<<<< HEAD
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (640, 0)
    pygame.init()
    screen = pygame.display.set_mode(
        (int(pygame.display.Info().current_w / 3), int(pygame.display.Info().current_h / 2)))
=======
    root = tk.Tk()
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (int(root.winfo_screenwidth()/2), 0)
    pygame.init()
    screen = pygame.display.set_mode((int(pygame.display.
                                          Info().current_w / 2),
                                      int(pygame.display.Info().current_h)))

>>>>>>> a14be3d5d0958f55388b0ef3f6932b0636124fc0
    background = pygame.Surface(screen.get_size())
    background = background.convert_alpha()
    background.fill((39, 174, 96))

    CENTER_W = int(pygame.display.Info().current_w / 2)
    CENTER_H = int(pygame.display.Info().current_h / 2)

    GREEN = 174

    clock = pygame.time.Clock()
    running = True

    network = Network()
    players = network.get_players()
    car = pygame_classes.from_state(players[1])
    car2 = pygame_classes.from_state(players[0])
    cam = pygame_classes.Camera()
    cup = pygame_classes.Cup(3, 9)
    bound_alert = pygame_classes.BoundsAlert()
<<<<<<< HEAD
    win_alert = pygame_classes.WinAlert()

    map_s = pygame.sprite.Group()
    cup_s = pygame.sprite.Group()
=======
    # time_alert = pygame_classes.TimeAlert()
    win_alert = pygame_classes.WinAlert()

    map_s = pygame.sprite.Group()
    player_s = pygame.sprite.Group()
    tracks_s = pygame.sprite.Group()
    target_s = pygame.sprite.Group()
    # timer_alert_s = pygame.sprite.Group()
>>>>>>> a14be3d5d0958f55388b0ef3f6932b0636124fc0
    bound_alert_s = pygame.sprite.Group()
    win_alert_s = pygame.sprite.Group()

    map_tile = ['sand8.png', 'sand1.png', 'sand2.png', 'sand3.png', 'sand4.png', 'sand5.png', 'sand6.png', 'grass.png',
                'tribune.png', 'tree.png']

    map = [
        [7, 2, 3, 3, 3, 4, 7, 2, 3, 4],
        [7, 1, 7, 7, 7, 1, 7, 1, 7, 1],
        [8, 7, 8, 8, 7, 1, 7, 1, 7, 1],
        [2, 3, 3, 4, 9, 1, 7, 1, 7, 1],
        [1, 2, 3, 6, 9, 1, 8, 1, 7, 1],
        [1, 1, 8, 8, 7, 5, 3, 6, 9, 1],
        [1, 5, 3, 3, 4, 7, 7, 7, 9, 1],
        [1, 7, 7, 7, 1, 7, 9, 9, 7, 1],
        [1, 8, 8, 8, 5, 3, 3, 3, 3, 6],
        [5, 3, 3, 0, 7, 7, 7, 7, 7, 7]
    ]

    pygame_classes.map_files.clear()

    for tile_num in range(0, len(map_tile)):
        pygame_classes.map_files.append(pygame_classes.load_image(map_tile[tile_num], False))
    for x in range(0, 10):
        for y in range(0, 10):
            map_s.add(pygame_classes.Map(map[x][y], x * 500, y * 500))

    pygame_classes.initialize_tracks()
<<<<<<< HEAD
    cup_s.add(cup)
=======
    target_s.add(target)
    # timer_alert_s.add(time_alert)
>>>>>>> a14be3d5d0958f55388b0ef3f6932b0636124fc0
    bound_alert_s.add(bound_alert)
    win_alert_s.add(win_alert)
    cam.set_position(car.x, car.y)

    is_out_of_road = False
    win = False
    while running:
<<<<<<< HEAD
        players = network.receive()
        car = pygame_classes.from_state(players[1])
        # Reset
        # if car.x == 320 and car.y == 270:
        #     is_out_of_road = False
        #     win = False

        car.rect.topleft = 320, 270
        car2 = pygame_classes.from_state(players[0])

        car.steer_left()
=======

        car2 = pygame_classes.from_state(network.send(car.get_state()))
>>>>>>> a14be3d5d0958f55388b0ef3f6932b0636124fc0
        car2.steer_left()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break

        cam.set_position(car.x, car.y)

<<<<<<< HEAD
=======
        # text_timer = font.render(
        #     'Timer: ' + str(int((target.time_left / 60) / 60)) + ":" + str(int((target.time_left / 60) % 60)), 1,
        #     (255, 255, 255))

>>>>>>> a14be3d5d0958f55388b0ef3f6932b0636124fc0
        screen.blit(background, (0, 0))

        map_s.update(cam.x, cam.y)
        map_s.draw(screen)

        cup_s.update(cam.x, cam.y)
        cup_s.draw(screen)

        car.update(cam.x, cam.y)
        car.draw2(screen)

        car2.update2(cam.x, cam.y)
        car2.draw2(screen)

<<<<<<< HEAD
=======
        target_s.update(cam.x, cam.y)
        target_s.draw(screen)

        if pygame.sprite.collide_rect(car2, car):
            car.x = car.x + car.rect.width


>>>>>>> a14be3d5d0958f55388b0ef3f6932b0636124fc0
        if pygame_classes.breaking(car.x + CENTER_W, car.y + CENTER_H) or car.border(
                screen.get_at((int(CENTER_W), int(CENTER_H))).g, GREEN, GREEN):
            car.speed = 0
            is_out_of_road = True
            bound_alert_s.draw(screen)

<<<<<<< HEAD
        if pygame.sprite.spritecollide(car, cup_s, True):
=======
        # if target.time_left == 0:
        #     timer_alert_s.draw(screen)
        #     car.speed = 0
        #     win = False

        if pygame.sprite.spritecollide(car, target_s, True):
>>>>>>> a14be3d5d0958f55388b0ef3f6932b0636124fc0
            car.speed = 0
            win = True

        if win:
            win_alert_s.draw(screen)

<<<<<<< HEAD
        flags = [is_out_of_road, win]
        network.send_border(flags)

=======

        # screen.blit(text_timer, (CENTER_W - 200, CENTER_H - 200))
>>>>>>> a14be3d5d0958f55388b0ef3f6932b0636124fc0
        pygame.display.flip()

        clock.tick(64)


main()
