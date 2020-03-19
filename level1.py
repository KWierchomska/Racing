import pygame, math, sys, time
from pygame.locals import *


def level1():
    pygame.init()
    screen = pygame.display.set_mode((1000, 562))
    # GAME CLOCK
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 75)
    win_condition = None
    t0 = time.time()


    class CarSprite(pygame.sprite.Sprite):
        MAX_FORWARD_SPEED = 10
        MAX_REVERSE_SPEED = 10
        ACCELERATION = 2
        TURN_SPEED = 10

        def __init__(self, image, position):
            pygame.sprite.Sprite.__init__(self)
            self.src_image = pygame.image.load(image)
            self.position = position
            self.speed = self.direction = 0
            self.k_left = self.k_right = self.k_down = self.k_up = 0

        def update(self, deltat):
            # SIMULATION
            self.speed += (self.k_up + self.k_down)
            if self.speed > self.MAX_FORWARD_SPEED:
                self.speed = self.MAX_FORWARD_SPEED
            if self.speed < -self.MAX_REVERSE_SPEED:
                self.speed = -self.MAX_REVERSE_SPEED
            self.direction += (self.k_right + self.k_left)
            x, y = (self.position)
            rad = self.direction * math.pi / 180
            x += -self.speed * math.sin(rad)
            y += -self.speed * math.cos(rad)
            #BOUNCE FROM BAND
            if y <= 280 and x >= 270:
                self.speed -= 2
                y += 40
            if x >= 880 and y >= 280:
                self.speed -= 2
                x -= 40
            if x <= 800 and y >= 400:
                self.speed -= 2
                x += 40
            if 130 <= x <= 800 and y >= 350:
                self.speed -= 2
                y -= 40
            if x <= 130 and y <= 280:
                self.speed -= 2
                x += 40
            if x >= 250 and y <= 280:
                self.speed -= 2
                x -= 40
            if y >= 562:
                y = 555
            self.position = (x, y)
            self.image = pygame.transform.rotate(self.src_image, self.direction)
            self.rect = self.image.get_rect()
            self.rect.center = self.position

    class WallSprite(pygame.sprite.Sprite):

        def __init__(self, image, position):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load(image)
            self.rect = self.image.get_rect()
            self.rect.center = position

    walls = [
        WallSprite('images/wall1.png', (631, 124)),
        WallSprite('images/wall2.png', (954, 406)),
        WallSprite('images/wall3.png', (59, 281)),
        WallSprite('images/wall4.png', (440, 478))
    ]
    walls_group = pygame.sprite.Group(*walls)

    class Trophy(pygame.sprite.Sprite):
        def __init__(self, position):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load('images/trophy.png')
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = position

        def draw(self, screen):
            screen.blit(self.image, self.rect)

    trophies = [Trophy((180, 0))]
    trophy_group = pygame.sprite.RenderPlain(*trophies)

    rect = screen.get_rect()
    car = CarSprite('images/car.png', (830, 500))
    car_group = pygame.sprite.RenderPlain(car)

    # THE GAME LOOP
    while True:
        # USER INPUT
        img = pygame.image.load("images/level1.png")
        screen.blit(img, (0, 0))
        t1 = time.time()
        dt = t1 - t0
        deltat = clock.tick(30)
        for event in pygame.event.get():
            if not hasattr(event, 'key'): continue
            down = event.type == KEYDOWN
            if win_condition == None:
                if event.key == K_RIGHT:
                    car.k_right = down * -5
                elif event.key == K_LEFT:
                    car.k_left = down * 5
                elif event.key == K_UP:
                    car.k_up = down * 2
                elif event.key == K_DOWN:
                    car.k_down = down * -2
                elif event.key == K_ESCAPE:
                    sys.exit(0)  # quit the game
            elif win_condition == True and event.key == K_SPACE:
                sys.exit(0);
            elif win_condition == False and event.key == K_SPACE:
                level1()
                t0 = t1
            elif event.key == K_ESCAPE:
                sys.exit(0)

            # COUNTDOWN TIMER
        seconds = round((20 - dt), 2)
        if win_condition == None:
            timer_text = font.render(str(seconds), True, (0, 0, 0))
            if seconds <= 0:
                win_condition = False
                timer_text = font.render("Time is up, press space to retry!", True, (0, 0, 0))

        # RENDERING
        car_group.update(deltat)
        '''collisions = pygame.sprite.groupcollide(car_group, walls_group, False, False, collided=None)
        if collisions != {}:
            win_condition = False
            timer_text = font.render("Crash! Press space to retry", True, (0, 0, 0))
            car.image = pygame.image.load('images/collision.png')
            seconds = 0
            car.MAX_FORWARD_SPEED = 0
            car.MAX_REVERSE_SPEED = 0
            car.k_right = 0
            car.k_left = 0'''

        trophy_collision = pygame.sprite.groupcollide(car_group, trophy_group, False, True)
        if trophy_collision != {}:
            seconds = seconds
            timer_text = font.render("Finished! Press Space to advance", True, (0, 0, 0))
            win_condition = True
            car.MAX_FORWARD_SPEED = 0
            car.MAX_REVERSE_SPEED = 0
            if win_condition == True:
                car.k_right = -5

        #walls_group.update(collisions)
        walls_group.draw(screen)
        car_group.draw(screen)
        trophy_group.draw(screen)
        # Counter Render
        screen.blit(timer_text, (20, 60))
        pygame.display.flip()