import pygame
from pygame.locals import *
import pygame_classes
import car_customization
import level5

TRAFFIC_COUNT = 45
CENTER_W = -1
CENTER_H = -1


def main():
    pygame.init()

    screen = pygame.display.set_mode((pygame.display.Info().current_w,
                                      pygame.display.Info().current_h),
                                     pygame.FULLSCREEN)

    background = pygame.Surface(screen.get_size())
    background = background.convert_alpha()
    background.fill((39, 174, 96))

    CENTER_W = int(pygame.display.Info().current_w / 2)
    CENTER_H = int(pygame.display.Info().current_h / 2)

    green_valueW = 174
    clock = pygame.time.Clock()
    running = True
    font = pygame.font.Font(None, 50)
    car = pygame_classes.Player(car_customization.change_color())
    cam = pygame_classes.Camera()
    target = pygame_classes.Finish(8, 9)
    bound_alert = pygame_classes.BoundsAlert()
    time_alert = pygame_classes.TimeAlert()
    win_alert = pygame_classes.WinAlert()

    map_s = pygame.sprite.Group()
    player_s = pygame.sprite.Group()
    tracks_s = pygame.sprite.Group()
    target_s = pygame.sprite.Group()
    timer_alert_s = pygame.sprite.Group()
    bound_alert_s = pygame.sprite.Group()
    win_alert_s = pygame.sprite.Group()

    map_tile = ['sand0.png', 'sand1.png', 'sand2.png', 'sand3.png', 'sand4.png', 'sand5.png', 'sand6.png', 'race.png',
                'tree.png', 'tribune.png', 'grass.png', 'band.png']

    map = [
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
    pygame_classes.map_files.clear()
    for tile_num in range(0, len(map_tile)):
        pygame_classes.map_files.append(pygame_classes.load_image(map_tile[tile_num], False))
    for x in range(0, 10):
        for y in range(0, 10):
            map_s.add(pygame_classes.Map(map[x][y], x * 500, y * 500))

    pygame_classes.initialize_tracks()
    target_s.add(target)
    timer_alert_s.add(time_alert)
    bound_alert_s.add(bound_alert)
    win_alert_s.add(win_alert)
    player_s.add(car)
    cam.set_position(car.x, car.y)

    win = None
    collided = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    car.reset()
                    target.reset()
                    win = None
                    collided = False
                elif event.key == pygame.K_ESCAPE:
                    running = False
                    break

        keys = pygame.key.get_pressed()
        if target.time_left > 0 and win == None:
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
            'Timer: ' + str(int((target.time_left / 60) / 60)) + ":" + str(int((target.time_left / 60) % 60)), 1,
            (255, 255, 255))

        screen.blit(background, (0, 0))

        map_s.update(cam.x, cam.y)
        map_s.draw(screen)

        if car.tracks:
            tracks_s.add(pygame_classes.Track(cam.x + CENTER_W, cam.y + CENTER_H, car.dir))

        tracks_s.update(cam.x, cam.y)
        tracks_s.draw(screen)

        player_s.update(cam.x, cam.y)
        player_s.draw(screen)

        target_s.update(cam.x, cam.y)
        target_s.draw(screen)

        if pygame_classes.breaking(car.x + CENTER_W, car.y + CENTER_H) or car.border(
                screen.get_at((int(CENTER_W), int(CENTER_H))).g, green_valueW, green_valueW):
            car.speed = 0
            win = False
            bound_alert_s.update()
            bound_alert_s.draw(screen)
        if target.time_left == 0:
            timer_alert_s.draw(screen)
            car.speed = 0
            win = False
        if pygame.sprite.spritecollide(car, target_s, True):
            car.speed = 0
            win = True
            collided = True
        if collided:
            win_alert_s.draw(screen)
            pygame.time.delay(1000)
            level5.main()
            running = False

        screen.blit(text_timer, (CENTER_W - 600, CENTER_H - 300))
        pygame.display.flip()

        clock.tick(64)
