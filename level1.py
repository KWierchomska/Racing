import pygame
from pygame.locals import *
import time
import pygame_classes
import car_customization
import level2
import level3

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
    # Initialize objects.
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
    car.dir = 180
    car.steer_left()
    cam = pygame_classes.Camera()
    target = pygame_classes.Finish(8, 1)
    bound_alert = pygame_classes.BoundsAlert()
    time_alert = pygame_classes.TimeAlert()
    win_alert = pygame_classes.WinAlert()
    # Create sprite groups.
    map_s = pygame.sprite.Group()
    player_s = pygame.sprite.Group()
    tracks_s = pygame.sprite.Group()
    target_s = pygame.sprite.Group()
    timer_alert_s = pygame.sprite.Group()
    bound_alert_s = pygame.sprite.Group()
    win_alert_s = pygame.sprite.Group()

    map_tile = ['asphalt0.png', 'asphalt1.png', 'asphalt2.png', 'asphalt3.png', 'asphalt4.png', 'race.png', 'tree.png',
                'tribune.png', 'grass.png', 'band.png']
    # Map to tile.

    # Tilemap
    map = [
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
    pygame_classes.map_files.clear()

    # Generate tiles
    for tile_num in range(0, len(map_tile)):
        pygame_classes.map_files.append(pygame_classes.load_image(map_tile[tile_num], False))
    for x in range(0, 10):
        for y in range(0, 10):
            map_s.add(pygame_classes.Map(map[x][y], x * 500, y * 500))

    # Load tracks
    pygame_classes.initialize_tracks()
    # Load finish
    target_s.add(target)
    # Load alerts
    timer_alert_s.add(time_alert)
    bound_alert_s.add(bound_alert)
    win_alert_s.add(win_alert)
    # Load car
    player_s.add(car)
    # Load camera
    cam.set_position(car.x, car.y)
    # Conditions for winning race and collisions
    win = None
    collided = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    car.reset()
                    car.dir = 180
                    car.steer_left()
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

        # Render Scene.
        screen.blit(background, (0, 0))

        map_s.update(cam.x, cam.y)
        map_s.draw(screen)

        # Conditional renders/effects
        collision(car)
        car.grass(screen.get_at((int(CENTER_W - 5), int(CENTER_H - 5))).g, green_valueW, green_valueW)
        if car.tracks:
            tracks_s.add(pygame_classes.Track(cam.x + CENTER_W, cam.y + CENTER_H, car.dir))

        # Just render
        tracks_s.update(cam.x, cam.y)
        tracks_s.draw(screen)

        player_s.update(cam.x, cam.y)
        player_s.draw(screen)

        target_s.update(cam.x, cam.y)
        target_s.draw(screen)

        # Conditional renders
        if pygame_classes.breaking(car.x + CENTER_W, car.y + CENTER_H):
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
            time.sleep(1)
            win_alert_s.draw(screen) #TODO: not showing due to sleep
            level3.main()
            running = False

        # Blit
        screen.blit(text_timer, (CENTER_W - 600, CENTER_H - 300))
        pygame.display.flip()

        clock.tick(64)
