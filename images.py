# Copyright (c) 2013-2015 by Joel Odom & Alex Odom, Marietta, GA All Rights Reserved

import pygame

PLAYER = None

STAIRS_DOWN = None
STAIRS_UP = None

RAT = None
GHOST = None

def init():
  global PLAYER, STAIRS_DOWN, STAIRS_UP, RAT, GHOST, TIER_1_CHEST, TIER_1_LOCKED_CHEST
  global SCARED_INDICATOR
  PLAYER = pygame.image.load(r'resources\player.png')
  STAIRS_DOWN = pygame.image.load(r'resources\stairs_down.png')
  STAIRS_UP = pygame.image.load(r'resources\stairs_up.png')
  RAT = pygame.image.load(r'resources\rat.png')
  GHOST = pygame.image.load(r'resources\ghost.png')
  TIER_1_CHEST = pygame.image.load(r'resources\Teir_1Chest.png')
  TIER_1_LOCKED_CHEST = pygame.image.load(r'resources\Teir_1LockedChest.png')
  SCARED_INDICATOR = pygame.image.load(r'resources\scared.png')


def draw_image_in_cell(constants, surface, image, x, y):
  cell_width = constants.SCREEN_WIDTH//constants.MAZE_WIDTH
  cell_height = constants.SCREEN_HEIGHT//constants.MAZE_HEIGHT

  # scale the image
  scaled = pygame.transform.scale(image,
    (cell_width - 2*constants.WALL_WIDTH, cell_height - 2*constants.WALL_WIDTH))

  # blit to the destination
  surface.blit(scaled, (cell_width*x + constants.WALL_WIDTH, cell_height*y + constants.WALL_WIDTH))

def draw_indicator_in_cell(constants, surface, image, x, y): # for smaller overlay indicators
  cell_width = constants.SCREEN_WIDTH//constants.MAZE_WIDTH
  cell_height = constants.SCREEN_HEIGHT//constants.MAZE_HEIGHT

  # scale the image
  scaled = pygame.transform.scale(image, (round((cell_width - 2*constants.WALL_WIDTH)/2),
    round((cell_height - 2*constants.WALL_WIDTH)/2)))

  # blit to the destination
  surface.blit(scaled, (cell_width*x + constants.WALL_WIDTH + round(cell_width/4),
    cell_height*y + constants.WALL_WIDTH + round(cell_width/4)))
