import pygame
from pygame.locals import *
import pygame_classes
import car_customization
import level3


def main():
    screen = pygame.display.set_mode((pygame.display.Info().current_w,
                                      pygame.display.Info().current_h),
                                     pygame.FULLSCREEN)

    background = pygame.Surface(screen.get_size())
    background = background.convert_alpha()
    background.fill((39, 174, 96))

    CENTER_W = int(pygame.display.Info().current_w / 2)
    CENTER_H = int(pygame.display.Info().current_h / 2)

    BARRIER_BLUE = 187
    BARRIER_WHITE = 238
    ROAD_BRIGHT_COLOR = 177
    ROAD_DARK_COLOR = 187
    GRASS = 174

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 50)

    car = pygame_classes.Player(car_customization.change_color(), CENTER_W, CENTER_H)
    car.x -= 200
    cam = pygame_classes.Camera()
    target = pygame_classes.Finish(9, 7)
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

    map_tile = ['mud1.png', 'mud2.png', 'mud3.png', 'mud4.png', 'mud5.png', 'mud6.png', 'mud7.png', 'race.png',
                'tree.png', 'tribune.png', 'grass.png']

    map = [
        [9, 9, 9, 2, 0, 0, 0, 0, 3, 8],
        [2, 0, 3, 1, 10, 10, 10, 10, 1, 8],
        [1, 10, 1, 1, 10, 2, 0, 3, 1, 8],
        [1, 10, 1, 10, 8, 1, 8, 1, 1, 8],
        [1, 10, 1, 8, 8, 1, 10, 1, 1, 8],
        [1, 10, 1, 10, 10, 1, 8, 4, 5, 9],
        [1, 10, 1, 10, 8, 1, 8, 8, 7, 10],
        [1, 10, 1, 8, 10, 1, 10, 8, 7, 6],
        [1, 10, 4, 0, 0, 5, 9, 9, 7, 1],
        [4, 0, 0, 0, 0, 0, 0, 0, 0, 5]
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
    current_crashes_number = 0
    crashes_limit = 5
    collided = False
    crash = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    car.reset()
                    car.x -= 200
                    target.reset()
                    current_crashes_number = 0
                    win = None
                    collided = False
                    crash = False
                elif event.key == pygame.K_ESCAPE:
                    running = False
                    break

        keys = pygame.key.get_pressed()
        if target.time_left > 0 and win is None:
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
        text_crashes_limit = font.render("Actual limit of crashes: " + str(crashes_limit - current_crashes_number), 1,
                                         (255, 255, 255))

        screen.blit(background, (0, 0))

        map_s.update(cam.x, cam.y)
        map_s.draw(screen)

        car.slow_down_on_grass(screen.get_at((int(CENTER_W - 5), int(CENTER_H - 5))).g, GRASS)

        if car.tracks:
            tracks_s.add(pygame_classes.Track(cam.x + CENTER_W, cam.y + CENTER_H, car.dir))

        tracks_s.update(cam.x, cam.y)
        tracks_s.draw(screen)

        player_s.update(cam.x, cam.y)
        player_s.draw(screen)

        target_s.update(cam.x, cam.y)
        target_s.draw(screen)

        if car.is_collision(screen, BARRIER_WHITE, BARRIER_BLUE):
            if current_crashes_number == crashes_limit:
                car.speed = 0
                win = False
                crash = True
            else:
                car.speed = 0
                if car.is_out_of_road(screen.get_at((car.rect.left + car.rect.width, car.rect.top - car.rect.height)).r,
                                      ROAD_BRIGHT_COLOR, ROAD_DARK_COLOR):
                    car.x = car.x + car.rect.width
                    car.y = car.y - 0.5 * car.rect.height
                elif car.is_out_of_road(
                        screen.get_at((car.rect.right - car.rect.width, car.rect.top - car.rect.height)).r,
                        ROAD_BRIGHT_COLOR, ROAD_DARK_COLOR):
                    car.x = car.x - car.rect.width
                    car.y = car.y - 0.5 * car.rect.height
                elif car.is_out_of_road(
                        screen.get_at((car.rect.left + car.rect.width, car.rect.bottom + car.rect.height)).r,
                        ROAD_BRIGHT_COLOR, ROAD_DARK_COLOR):
                    car.x = car.x + car.rect.width
                    car.y = car.y + car.rect.height
                elif car.is_out_of_road(
                        screen.get_at((car.rect.right - car.rect.width, car.rect.bottom + car.rect.height)).r,
                        ROAD_BRIGHT_COLOR, ROAD_DARK_COLOR):
                    car.x = car.x - car.rect.width
                    car.y = car.y + car.rect.height
                current_crashes_number += 1

        if crash:
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
            running = False

        screen.blit(text_timer, (CENTER_W - 600, CENTER_H - 300))
        screen.blit(text_crashes_limit, (CENTER_W - 600, CENTER_H - 240))
        pygame.display.flip()

        clock.tick(64)

    pygame.time.wait(1000)
    level3.main()
