import os, sys, pygame, math
from pygame.locals import *
from enum import Enum

# Text formatting
def text_format(message, textFont, textSize, textColor):
    newFont = pygame.font.Font(textFont, textSize)
    newText = newFont.render(message, 0, textColor)
    return newText

def showText(text, font, size, color):
    return text_format(text, font, size, color)

# Load an image.
def load_image(file, transparent=True):
    print("Loading " + file + " ..")
    fullname = os.path.join('Images', file)
    image = pygame.image.load(fullname)
    if transparent:
        image = image.convert()
        color_key = image.get_at((0, 0))
        image.set_colorkey(color_key, RLEACCEL)
    else:
        image = image.convert_alpha()
    return image


BOUND_MIN = 0
BOUND_MAX = 500 * 10
NOTE_HALF_X = 211  # TODO: check this coordinates
NOTE_HALF_Y = 112


# Check if car is outside bounds
def breaking(car_x, car_y):
    if car_x < BOUND_MIN or car_x > BOUND_MAX:
        return True
    if car_y < BOUND_MIN or car_y > BOUND_MAX:
        return True
    return False


# Display alert
class BoundsAlert(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('crash.png')
        self.rect = self.image.get_rect()
        self.x = int(pygame.display.Info().current_w / 2) - NOTE_HALF_X
        self.y = int(pygame.display.Info().current_h / 2) - NOTE_HALF_Y
        self.rect.topleft = self.x, self.y


class Camera:
    def __init__(self):
        self.x = 5000
        self.y = 5000

    def set_position(self, x, y):
        self.x = x
        self.y = y


# Rotate an image while keeping it center
def rot_center(image, rect, angle):
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect(center=rect.center)
    return rot_image, rot_rect


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


PENALTY_COOL = 180
FLAG_SCORE = 15
CRASH_PENALTY = -2
HALF_TILE = 250
FULL_TILE = 500
COUNTDOWN_FULL = 3600
COUNTDOWN_EXTEND = 750


# Class for placing trophy and game timer
class Finish(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('trophy.png', False)
        self.rect = self.image.get_rect()
        self.x = x * FULL_TILE + HALF_TILE
        self.y = y * FULL_TILE + HALF_TILE
        self.rect.topleft = self.x, self.y
        self.time_left = COUNTDOWN_FULL

    def reset(self):
        self.time_left = COUNTDOWN_FULL

    def update(self, cam_x, cam_y):
        self.rect.topleft = self.x - cam_x, self.y - cam_y
        if (self.time_left > 0):
            self.time_left -= 1


# Class for bombs
class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('bomb.png', False)
        self.rect = self.image.get_rect()
        self.x = x * FULL_TILE + HALF_TILE
        self.y = y * FULL_TILE + HALF_TILE
        self.rect.topleft = self.x, self.y
        self.time_left = COUNTDOWN_FULL

    def reset(self):
        self.time_left = COUNTDOWN_FULL

    def update(self, cam_x, cam_y):
        self.rect.topleft = self.x - cam_x, self.y - cam_y


# Initialize, load the tracks image.
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
        self.x = car_x + 25  # -95
        self.y = car_y + 15
        self.rect.topleft = self.x, self.y

    def update(self, cam_x, cam_y):
        self.rect.topleft = self.x - cam_x, self.y - cam_y
        self.lifetime = self.lifetime - 1
        if self.lifetime < 1:
            pygame.sprite.Sprite.kill(self)


GRASS_SPEED = 0.715
# GRASS_GREEN = 187
CENTER_X = -1
CENTER_Y = -1


# Class for player's car
class Player(pygame.sprite.Sprite):
    def __init__(self, color):
        pygame.sprite.Sprite.__init__(self)
        CENTER_X = int(pygame.display.Info().current_w / 2) +20  # -100
        CENTER_Y = int(pygame.display.Info().current_h / 2)
        self.x = CENTER_X
        self.y = CENTER_Y
        self.image = load_image(color)
        self.rect = self.image.get_rect()
        self.image_orig = self.image
        self.screen = pygame.display.get_surface()
        self.area = self.screen.get_rect()
        self.rect.topleft = self.x, self.y
        self.dir = 0
        self.speed = 0.0
        self.max_speed = 20 #11.5
        self.min_speed = -5#-1.85
        self.acceleration = 0.2 #0.095
        self.deacceleration = 2
        self.softening = 0.04
        self.steering = 1.60
        self.tracks = False

    # Reset the car.
    def reset(self):
        self.x = int(pygame.display.Info().current_w / 2) +20  # -100
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
    def grass(self, value, RGB_value1, RGB_value2):
        if value == RGB_value1 or value == RGB_value2:
            if self.speed - self.deacceleration > GRASS_SPEED * 2:
                self.speed = self.speed - self.deacceleration * 2
                self.emit_tracks()

    # Check if car is on track
    def border(self, value, RGB_value1, RGB_value2):
        if value == RGB_value1 or value == RGB_value2:
            self.speed = 0
            return True
        return False

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

    # fix this function
    def update(self, last_x, last_y):
        self.x = self.x + self.speed * math.cos(math.radians(270 - self.dir))
        self.y = self.y + self.speed * math.sin(math.radians(270 - self.dir))
        self.reset_tracks()


# Alert fot time up
class TimeAlert(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('time_up.png')
        self.rect = self.image.get_rect()
        self.x = int(pygame.display.Info().current_w / 2) - NOTE_HALF_X
        self.y = int(pygame.display.Info().current_h / 2) - NOTE_HALF_Y
        self.rect.topleft = self.x, self.y


class WinAlert(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('winner.png')
        self.rect = self.image.get_rect()
        self.x = int(pygame.display.Info().current_w / 2) - NOTE_HALF_X
        self.y = int(pygame.display.Info().current_h / 2) - NOTE_HALF_Y
        self.rect.topleft = self.x, self.y

class Color(Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    ORANGE = (255, 165, 0)
