import os, pygame, math
from pygame.locals import *


# Text formatting
def text_format(message, text_font, text_size, text_color):
    new_font = pygame.font.Font(text_font, text_size)
    new_text = new_font.render(message, 0, text_color)
    return new_text


# Load an image.
def load_image(file, transparent=True):
    fullname = os.path.join('Images', file)
    image = pygame.image.load(fullname)
    if transparent:
        image = image.convert()
        color_key = image.get_at((0, 0))
        image.set_colorkey(color_key, RLEACCEL)
    else:
        image = image.convert_alpha()
    return image


# Rotate an image while keeping it center
def rot_center(image, rect, angle):
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect(center=rect.center)
    return rot_image, rot_rect


BOUND_MIN = 0
BOUND_MAX = 500 * 10


class Camera:
    def __init__(self):
        self.x = 5000
        self.y = 5000

    def set_position(self, x, y):
        self.x = x
        self.y = y


map_files = []


class Map(pygame.sprite.Sprite):

    def __init__(self, tile_map, y, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = map_files[tile_map]
        self.rect = self.image.get_rect()

        self.x = x
        self.y = y

    # Realign the map
    def update(self, cam_x, cam_y):
        self.rect.topleft = self.x - cam_x, self.y - cam_y


HALF_TILE = 250
FULL_TILE = 500
COUNTDOWN = 3600


# Class for placing trophy and game timer
class Finish(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('trophy.png', False)
        self.rect = self.image.get_rect()
        self.x = x * FULL_TILE + HALF_TILE
        self.y = y * FULL_TILE + HALF_TILE
        self.rect.topleft = self.x, self.y
        self.time_left = COUNTDOWN

    def reset(self):
        self.time_left = COUNTDOWN

    def update(self, cam_x, cam_y):
        self.rect.topleft = self.x - cam_x, self.y - cam_y
        if self.time_left > 0:
            self.time_left -= 1


# Class for placing trophy for 2 players mode
class Cup(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('trophy.png', False)
        self.rect = self.image.get_rect()
        self.x = x * FULL_TILE + HALF_TILE
        self.y = y * FULL_TILE + HALF_TILE
        self.rect.topleft = self.x, self.y

    def update(self, cam_x, cam_y):
        self.rect.topleft = self.x - cam_x, self.y - cam_y


# Class for bombs
class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('bomb.png', False)
        self.rect = self.image.get_rect()
        self.x = x * FULL_TILE + HALF_TILE
        self.y = y * FULL_TILE + HALF_TILE
        self.rect.topleft = self.x, self.y
        self.time_left = COUNTDOWN

    def reset(self):
        self.time_left = COUNTDOWN

    def update(self, cam_x, cam_y):
        self.rect.topleft = self.x - cam_x, self.y - cam_y


# Class for holes
class Hole(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('hole.png', False)
        self.rect = self.image.get_rect()
        self.x = x * FULL_TILE + HALF_TILE
        self.y = y * FULL_TILE + HALF_TILE
        self.rect.topleft = self.x, self.y
        self.penalty = -5

    def reset(self):
        self.time_left = COUNTDOWN

    def update(self, cam_x, cam_y):
        self.rect.topleft = self.x - cam_x, self.y - cam_y


# Class for diamonds
class Diamond(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('diamond.png', False)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image, 50)
        self.x = x * FULL_TILE + HALF_TILE
        self.y = y * FULL_TILE + HALF_TILE
        self.rect.topleft = self.x, self.y
        self.prize = 5

    def reset(self):
        self.time_left = COUNTDOWN

    def update(self, cam_x, cam_y):
        self.rect.topleft = self.x - cam_x, self.y - cam_y


# Initialize, load the tracks image
def initialize_tracks():
    global tracks_img
    tracks_img = load_image('tracks.png', False)


# Class for car's tracks
class Track(pygame.sprite.Sprite):
    def __init__(self, car_x, car_y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = rot_center(tracks_img, tracks_img.get_rect(), angle)
        self.lifetime = 100
        self.screen = pygame.display.get_surface()
        self.x = car_x + 2
        self.y = car_y + 15
        self.rect.topleft = self.x, self.y

    def update(self, cam_x, cam_y):
        self.rect.topleft = self.x - cam_x, self.y - cam_y
        self.lifetime = self.lifetime - 1
        if self.lifetime < 1:
            pygame.sprite.Sprite.kill(self)


GRASS_SPEED = 0.715


# Class for player's car
class Player(pygame.sprite.Sprite):
    def __init__(self,
                 color,
                 x=450,
                 y=250,
                 dir=0,
                 speed=0.0,
                 max_speed=20,
                 min_speed=-5,
                 acceleration=0.2,
                 deacceleration=2,
                 softening=0.04,
                 steering=1.60,
                 tracks=False):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.x = x
        self.y = y
        self.image = load_image(self.color)
        self.rect = self.image.get_rect()
        self.image_orig = self.image
        self.screen = pygame.display.get_surface()
        self.rect.topleft = self.x, self.y
        self.dir = dir
        self.speed = speed
        self.max_speed = max_speed
        self.min_speed = min_speed
        self.acceleration = acceleration
        self.deacceleration = deacceleration
        self.softening = softening
        self.steering = steering
        self.tracks = tracks

    # Reset the car.
    def reset(self):
        self.x = int(pygame.display.Info().current_w / 2)
        self.y = int(pygame.display.Info().current_h / 2)
        self.speed = 0.0
        self.dir = 0
        self.image, self.rect = rot_center(self.image_orig, self.rect, self.dir)
        self.rect.topleft = self.x, self.y

    # Emit tracks
    def emit_tracks(self):
        self.tracks = True

    # Do not emit tracks
    def reset_tracks(self):
        self.tracks = False

    # If the car is on grass, decrease speed and emit tracks.
    def slow_down_on_grass(self, value, color):
        if value == color:
            if self.speed - self.deacceleration > GRASS_SPEED * 2:
                self.speed = self.speed - self.deacceleration * 2
                self.emit_tracks()

    # Check if car is out of road
    def is_out_of_road(self, value, color1, color2):
        if value == color1 or value == color2:
            self.speed = 0
            return True
        return False

    # Check if any of car's sides are out of road
    def is_collision(self, screen, color1, color2):
        return self.is_out_of_road(screen.get_at(self.rect.topleft).b, color1, color2) or self.is_out_of_road(
            screen.get_at(self.rect.topright).b, color1, color2) \
               or self.is_out_of_road(screen.get_at(self.rect.bottomright).b, color1, color2) or self.is_out_of_road(
            screen.get_at(self.rect.bottomleft).b, color1, color2)

    # Push back on impact
    def impact(self):
        if self.speed > 0:
            self.speed = self.min_speed

    def soften(self):
        if self.speed > 0:
            self.speed -= self.softening
        if self.speed < 0:
            self.speed += self.softening

    # Accelerate the vehicle
    def accelerate(self):
        if self.speed < self.max_speed:
            self.speed = self.speed + self.acceleration
            if self.speed < self.max_speed / 3:
                self.emit_tracks()

    # Deaccelerate.
    def deaccelerate(self):
        if self.speed > self.min_speed:
            self.speed = self.speed - self.deacceleration
            self.emit_tracks()

    # Steer.
    def steer_left(self):
        self.dir = self.dir + self.steering
        if self.dir > 360:
            self.dir = 0
        if self.speed > self.max_speed / 2:
            self.emit_tracks()
        self.image, self.rect = rot_center(self.image_orig, self.rect, self.dir)

    # Steer.
    def steer_right(self):
        self.dir = self.dir - self.steering
        if self.dir < 0:
            self.dir = 360
        if self.speed > self.max_speed / 2:
            self.emit_tracks()
        self.image, self.rect = rot_center(self.image_orig, self.rect, self.dir)

    def update(self, last_x, last_y):
        self.x = self.x + self.speed * math.cos(math.radians(270 - self.dir))
        self.y = self.y + self.speed * math.sin(math.radians(270 - self.dir))
        self.reset_tracks()

    # Update for second car in two players mode
    def update_additional_car(self, cam_x, cam_y):
        self.x = self.x + self.speed * math.cos(math.radians(270 - self.dir))
        self.y = self.y + self.speed * math.sin(math.radians(270 - self.dir))
        self.rect.topleft = self.x - cam_x + 320, self.y - cam_y + 270

    # Draw for second car in two players mode
    def draw_additional_car(self, surface):
        self = surface.blit(self.image, self.rect.topleft)

    # Get state for sending car
    def get_state(self):
        return {'x': self.x,
                'y': self.y,
                'color': self.color,
                "dir": self.dir,
                "speed": self.speed,
                "max_speed": self.max_speed,
                "min_speed": self.min_speed,
                "acceleration": self.acceleration,
                "deacceleration": self.deacceleration,
                "softening": self.softening,
                "steering": self.steering,
                "tracks": self.tracks}


# Check if car is outside bounds
def is_out_of_map(car_x, car_y):
    if car_x < BOUND_MIN or car_x > BOUND_MAX:
        return True
    if car_y < BOUND_MIN or car_y > BOUND_MAX:
        return True
    return False


# Build car from received state
def from_state(state):
    return Player(color=state['color'],
                  x=state['x'],
                  y=state['y'],
                  dir=state['dir'],
                  speed=state['speed'],
                  max_speed=state['max_speed'],
                  min_speed=state['min_speed'],
                  acceleration=state['acceleration'],
                  deacceleration=state['deacceleration'],
                  softening=state['softening'],
                  steering=state['steering'],
                  tracks=state['tracks'])


ALERT_X = 350
ALERT_Y = 150


# Alert for bounds
class BoundsAlert(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('crash.png')
        self.rect = self.image.get_rect()
        self.x = int(pygame.display.Info().current_w / 2) - ALERT_X
        self.y = int(pygame.display.Info().current_h / 2) - ALERT_Y
        self.rect.topleft = self.x, self.y


# Alert for time
class TimeAlert(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('time_up.png')
        self.rect = self.image.get_rect()
        self.x = int(pygame.display.Info().current_w / 2) - ALERT_X
        self.y = int(pygame.display.Info().current_h / 2) - ALERT_Y
        self.rect.topleft = self.x, self.y


# Alert for win
class WinAlert(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('winner.png')
        self.rect = self.image.get_rect()
        self.x = int(pygame.display.Info().current_w / 2) - ALERT_X
        self.y = int(pygame.display.Info().current_h / 2) - ALERT_Y
        self.rect.topleft = self.x, self.y
