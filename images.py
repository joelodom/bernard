# Copyright (c) 2013 by Joel Odom & Alex Odom, Marietta, GA All Rights Reserved

import pygame


STAIRS_DOWN = None
STAIRS_UP = None

RAT = None

def init():
  global STAIRS_DOWN, STAIRS_UP, RAT
  STAIRS_DOWN = pygame.image.load(r'resources\stairs_down.png')
  STAIRS_UP = pygame.image.load(r'resources\stairs_up.png')
  RAT = pygame.image.load(r'resources\rat.png')


def draw_image_in_cell(constants, surface, image, x, y):
  cell_width = constants.SCREEN_WIDTH//constants.MAZE_WIDTH
  cell_height = constants.SCREEN_HEIGHT//constants.MAZE_HEIGHT

  # scale the image
  scaled = pygame.transform.scale(image,
    (cell_width - 2*constants.WALL_WIDTH, cell_height - 2*constants.WALL_WIDTH))

  # blit to the destination
  surface.blit(scaled, (cell_width*x + constants.WALL_WIDTH, cell_height*y + constants.WALL_WIDTH))
