import pygame
from pygame.locals import *
import pygame_classes
import car_customization

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

    blue_valueB=187
    blue_valueW=238

    crashes_limit=5

    clock = pygame.time.Clock()
    running = True
    font = pygame.font.Font(None, 24)
    car = pygame_classes.Player(car_customization.change_color())
    cam = pygame_classes.Camera()
    target = pygame_classes.Finish(9, 7)
    bound_alert = pygame_classes.BoundsAlert()
    time_alert = pygame_classes.TimeAlert()
    # create sprite groups.
    map_s = pygame.sprite.Group()
    player_s = pygame.sprite.Group()
    tracks_s = pygame.sprite.Group()
    target_s = pygame.sprite.Group()
    timer_alert_s = pygame.sprite.Group()
    bound_alert_s = pygame.sprite.Group()



    map_tile = ['mud1.png', 'mud2.png', 'mud3.png', 'mud4.png', 'mud5.png', 'mud6.png', 'mud7.png', 'race.png', 'tree.png', 'tribune.png', 'grass.png']
    # Map to tile.

    # tilemap.
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

    # generate tiles
    for tile_num in range(0, len(map_tile)):
        pygame_classes.map_files.append(pygame_classes.load_image(map_tile[tile_num], False))
    for x in range(0, 10):
        for y in range(0, 10):
            map_s.add(pygame_classes.Map(map[x][y], x * 500, y * 500))

    # load tracks
    pygame_classes.initialize_tracks()
    # load finish
    target_s.add(target)
    # load alerts
    timer_alert_s.add(time_alert)
    bound_alert_s.add(bound_alert)

    player_s.add(car)

    cam.set_position(car.x, car.y)

    win = None
    current_crashes_number=0

    while running:
        # Render loop.

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    car.reset()
                    target.reset()
                    current_crashes_number=0
                elif event.key == pygame.K_ESCAPE:
                    running = False
                    break

        # Check for key input. (KEYDOWN, trigger often)
        keys = pygame.key.get_pressed()
        if target.time_left > 0:
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

        font = pygame.font.Font(None, 50)
        text_timer = font.render(
            'Timer: ' + str(int((target.time_left / 60) / 60)) + ":" + str(int((target.time_left / 60) % 60)), 1,
            (255, 255, 255))
        text_crashes_limit=font.render("Actual limit of crashes: " +str(crashes_limit-current_crashes_number), 1, (255,255,255))

        # Render Scene.
        screen.blit(background, (0, 0))

        # cam.set_pos(car.x, car.y)

        map_s.update(cam.x, cam.y)
        map_s.draw(screen)

        # Conditional renders/effects
        if (car.tracks):
            tracks_s.add(pygame_classes.Track(cam.x + CENTER_W, cam.y + CENTER_H, car.dir))

        # Just render..
        tracks_s.update(cam.x, cam.y)
        tracks_s.draw(screen)

        player_s.update(cam.x, cam.y)
        player_s.draw(screen)

        target_s.update(cam.x, cam.y)
        target_s.draw(screen)

        # Conditional renders.
        if pygame_classes.breaking(car.x + CENTER_W, car.y + CENTER_H) or car.border(screen.get_at((int(CENTER_W ), int(CENTER_H ))).b, blue_valueB, blue_valueW):
            if current_crashes_number == crashes_limit:
                car.speed = 0
                win = False
                bound_alert_s.update()
                bound_alert_s.draw(screen)
            else:
                # while not car.border(screen.get_at((int(CENTER_W ), int(CENTER_H ))).b, 177, 187):
                #     car.deaccelerate()
                car.speed=0
                if car.border(screen.get_at((int(CENTER_W-15), int(CENTER_H))).r, 177, 187) and not pygame_classes.breaking(car.x + CENTER_W-15, car.y + CENTER_H):
                    car.x=car.x-40
                    current_crashes_number += 1
                elif car.border(screen.get_at((int(CENTER_W+15), int(CENTER_H))).r, 177, 187) and not pygame_classes.breaking(car.x + CENTER_W+15, car.y + CENTER_H):
                    car.x=car.x+40
                    current_crashes_number += 1
                elif car.border(screen.get_at((int(CENTER_W), int(CENTER_H-15))).r, 177, 187) and not pygame_classes.breaking(car.x + CENTER_W, car.y + CENTER_H-15):
                    car.y=car.y-40
                    current_crashes_number += 1
                elif car.border(screen.get_at((int(CENTER_W), int(CENTER_H+15))).r, 177, 187) and not pygame_classes.breaking(car.x + CENTER_W, car.y + CENTER_H+15):
                    car.y=car.y+40
                    current_crashes_number += 1

        if (target.time_left == 0):
            timer_alert_s.draw(screen)
            car.speed = 0
            win = False


        # Blit Blit..
        screen.blit(text_timer, (CENTER_W - 700, CENTER_H - 500))
        screen.blit(text_crashes_limit, (CENTER_W - 700, CENTER_H - 450))
        pygame.display.flip()

        # Check collision!!

        if pygame.sprite.spritecollide(car, target_s, True):
            car.speed = 0
            win = True
            timer_alert_s.draw(screen)

        clock.tick(64)
