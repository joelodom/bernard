# Copyright (c) 2013 by Joel Odom & Alex Odom, Marietta, GA All Rights Reserved

import pygame
import colors
import sounds


class Bomb:
  exploded = False

  def play_sound(self):
    self.SOUND.play()

  def draw(self, surface):
    pygame.draw.rect(surface, colors.SOLID_RED,
      (self.constants.CELL_WIDTH*self.x + self.constants.WALL_WIDTH,
      self.constants.CELL_HEIGHT*self.y + self.constants.WALL_WIDTH,
      self.constants.CELL_WIDTH - 2*self.constants.WALL_WIDTH,
      self.constants.CELL_HEIGHT - 2*self.constants.WALL_WIDTH), 0)


class Dynamite(Bomb):
  BLAST_RADIUS = 3
  time_remaining = 5

  def __init__(self, constants, x, y):
    self.SOUND = sounds.DYNAMITE_SOUND
    self.constants = constants
    self.x = x
    self.y = y


class AtomBomb(Bomb):
  BLAST_RADIUS = 10
  time_remaining = 20

  def __init__(self, constants, x, y):
    self.SOUND = sounds.ATOM_BOMB_SOUND
    self.constants = constants
    self.x = x
    self.y = y


def list_bombs(constants):
  return ((Dynamite(constants, 0, 0)), (AtomBomb(constants, 0, 0)))


#
# TESTS
#

def test_list_bombs(constants):
  for bomb in list_bombs(constants):
    assert bomb.BLAST_RADIUS > 0, 'missing BLAST_RADIUS'

def run_tests(constants):
  test_list_bombs(constants)
