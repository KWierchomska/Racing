import os, sys, pygame, math
from pygame.locals import *
from loader import load_image
from random import randrange

#Map filenames.

map_files = []


#tilemap rotation, x90ccw
map_1_rot = [
          [1,1,0,1,1,0,1,1,1,3],
          [0,0,0,0,1,0,1,0,0,0],
          [0,1,2,1,0,2,1,2,0,0],
          [1,1,0,1,3,0,0,0,0,0],
          [1,0,0,0,0,0,1,1,0,3],
          [0,2,0,1,0,0,0,3,0,0],
          [0,0,0,1,3,0,0,1,3,0],
          [0,1,0,1,0,2,0,0,3,0],
          [0,0,2,1,3,0,0,2,1,3],
          [2,2,1,2,1,1,2,1,1,3]
            ]


class Map(pygame.sprite.Sprite):
    def __init__(self, tile_map, y, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = map_files[tile_map]
        self.rect = self.image.get_rect()

        self.x = x
        self.y = y

#Realign the map
    def update(self, cam_x, cam_y):
        self.rect.topleft = self.x - cam_x, self.y - cam_y