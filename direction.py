import pygame, math
from pygame.locals import *
from loader import load_image

PI = 3.14

#rotate the arrow.
def rot_center(image, rect, angle):
        """rotate an image while keeping its center"""
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image,rot_rect

