from random import randint
import pygame
from pygame.locals import *
import pygame_classes
import car_customization
import level5


def main():
    screen = pygame.display.set_mode((pygame.display.Info().current_w,
                                      pygame.display.Info().current_h),
                                     pygame.FULLSCREEN)

    background = pygame.Surface(screen.get_size())
    background = background.convert_alpha()
    background.fill((39, 174, 96))

    CENTER_W = int(pygame.display.Info().current_w / 2)
    CENTER_H = int(pygame.display.Info().current_h / 2)

    BARRIER_WHITE = 238
    BARRIER_RED = 23
    ROAD_BRIGHT_COLOR = 203
    ROAD_DARK_COLOR = 194
    GRASS = 174

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 50)

    car = pygame_classes.Player(car_customization.change_color(), CENTER_W, CENTER_H)
    cam = pygame_classes.Camera()
    car.dir = 180
    car.steer_left()
    car.x -= 200
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
    hole_s = pygame.sprite.Group()
    diamond_s = pygame.sprite.Group()

    map_tile = ['asphalt0.png', 'asphalt1.png', 'asphalt2.png', 'asphalt3.png', 'asphalt4.png', 'asphalt5.png',
                'asphalt6.png', 'grass.png', 'tribune.png']

    map = [
        [5, 3, 3, 3, 3, 3, 3, 3, 3, 6],
        [1, 7, 8, 7, 8, 7, 1, 8, 8, 1],
        [1, 5, 6, 1, 7, 7, 5, 3, 3, 4],
        [1, 1, 1, 1, 7, 7, 1, 7, 8, 8],
        [1, 1, 1, 1, 7, 7, 1, 8, 8, 8],
        [1, 1, 1, 1, 7, 8, 2, 3, 3, 6],
        [1, 1, 1, 1, 7, 7, 7, 8, 8, 1],
        [1, 1, 1, 1, 7, 8, 5, 3, 3, 4],
        [2, 4, 1, 1, 7, 8, 1, 7, 7, 7],
        [7, 7, 2, 4, 7, 7, 2, 3, 3, 7]
    ]
    pygame_classes.map_files.clear()
    for tile_num in range(0, len(map_tile)):
        pygame_classes.map_files.append(pygame_classes.load_image(map_tile[tile_num], False))
    for x in range(0, 10):
        for y in range(0, 10):
            map_s.add(pygame_classes.Map(map[x][y], x * 500, y * 500))

    for i in range(12):
        x = randint(0, 9)
        y = randint(0, 9)
        while map[x][y] == 7 or map[x][y] == 8:
            x = randint(0, 9)
            y = randint(0, 9)
        if i < 6:
            hole = pygame_classes.Hole(y, x)
            hole_s.add(hole)
        else:
            diamond = pygame_classes.Diamond(y, x)
            diamond_s.add(diamond)

    pygame_classes.initialize_tracks()
    target_s.add(target)
    timer_alert_s.add(time_alert)
    bound_alert_s.add(bound_alert)
    win_alert_s.add(win_alert)
    player_s.add(car)
    cam.set_position(car.x, car.y)

    win = None
    collided = False
    running = True
    BONUS_POINTS = 10
    PENALTY_POINTS = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    car.reset()
                    car.dir = 180
                    car.steer_left()
                    car.x -= 200
                    target.reset()
                    win = None
                    collided = False
                    BONUS_POINTS = 10
                    PENALTY_POINTS = 0
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
        text_score = font.render("Score: " + str(BONUS_POINTS + PENALTY_POINTS), 1, (255, 255, 255))

        screen.blit(background, (0, 0))

        map_s.update(cam.x, cam.y)
        map_s.draw(screen)

        car.slow_down_on_grass(screen.get_at((int(CENTER_W - 5), int(CENTER_H - 5))).g, GRASS)

        if car.tracks:
            tracks_s.add(pygame_classes.Track(cam.x + CENTER_W, cam.y + CENTER_H, car.dir))

        tracks_s.update(cam.x, cam.y)
        tracks_s.draw(screen)

        target_s.update(cam.x, cam.y)
        target_s.draw(screen)

        hole_s.update(cam.x, cam.y)
        hole_s.draw(screen)

        diamond_s.update(cam.x, cam.y)
        diamond_s.draw(screen)

        player_s.update(cam.x, cam.y)
        player_s.draw(screen)

        if car.is_collision(screen, BARRIER_RED, BARRIER_WHITE):
            car.speed = 0
            if car.is_out_of_road(screen.get_at((car.rect.left + car.rect.width, car.rect.top - car.rect.height)).b,
                                  ROAD_BRIGHT_COLOR, ROAD_DARK_COLOR):
                car.x = car.x + car.rect.width
                car.y = car.y - 0.5 * car.rect.height
            elif car.is_out_of_road(screen.get_at((car.rect.right - car.rect.width, car.rect.top - car.rect.height)).b,
                                    ROAD_BRIGHT_COLOR, ROAD_DARK_COLOR):
                car.x = car.x - car.rect.width
                car.y = car.y - 0.5 * car.rect.height
            elif car.is_out_of_road(
                    screen.get_at((car.rect.left + car.rect.width, car.rect.bottom + car.rect.height)).b,
                    ROAD_BRIGHT_COLOR, ROAD_DARK_COLOR):
                car.x = car.x + car.rect.width
                car.y = car.y + car.rect.height
            elif car.is_out_of_road(
                    screen.get_at((car.rect.right - car.rect.width, car.rect.bottom + car.rect.height)).b,
                    ROAD_BRIGHT_COLOR, ROAD_DARK_COLOR):
                car.x = car.x - car.rect.width
                car.y = car.y + car.rect.height

        if pygame.sprite.spritecollide(car, hole_s, True, pygame.sprite.collide_mask):
            PENALTY_POINTS = PENALTY_POINTS + hole.penalty

        if pygame.sprite.spritecollide(car, diamond_s, True, pygame.sprite.collide_mask):
            BONUS_POINTS = BONUS_POINTS + diamond.prize

        if target.time_left == 0:
            timer_alert_s.draw(screen)
            car.speed = 0
            win = False

        if BONUS_POINTS + PENALTY_POINTS <= 0:
            car.speed = 0
            win = False
            bound_alert_s.update()
            bound_alert_s.draw(screen)

        if pygame.sprite.spritecollide(car, target_s, True):
            car.speed = 0
            win = True
            collided = True

        if collided:
            win_alert_s.draw(screen)
            running = False

        screen.blit(text_timer, (CENTER_W - 600, CENTER_H - 300))
        screen.blit(text_score, (CENTER_W - 600, CENTER_H - 240))
        pygame.display.flip()

        clock.tick(64)

    pygame.time.wait(1000)
    level5.main()
