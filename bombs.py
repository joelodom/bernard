# Copyright (c) 2013 by Joel Odom & Alex Odom, Marietta, GA All Rights Reserved

import pygame
import colors
import sounds


class Bomb:
  exploded = False

  def play_sound(self):
    self.SOUND.play()

  def draw(self, surface): # note that x and y must be bound
    pygame.draw.rect(surface, colors.SOLID_RED,
      (self.constants.CELL_WIDTH*self.x + self.constants.WALL_WIDTH,
      self.constants.CELL_HEIGHT*self.y + self.constants.WALL_WIDTH,
      self.constants.CELL_WIDTH - 2*self.constants.WALL_WIDTH,
      self.constants.CELL_HEIGHT - 2*self.constants.WALL_WIDTH), 0)


class CherryBomb(Bomb):
  NAME = 'Cherry Bomb'
  DESCRIPTION = 'Don\'t blow off your finger.'
  BLAST_RADIUS = 1
  MIN_LEVEL = 1
  time_remaining = 3

  def __init__(self, constants):
    self.SOUND = sounds.DYNAMITE_SOUND # TODO
    self.constants = constants


class Dynamite(Bomb):
  NAME = 'Dynamite'
  DESCRIPTION = 'Fire in the hole!'
  BLAST_RADIUS = 3
  MIN_LEVEL = 7
  time_remaining = 5

  def __init__(self, constants):
    self.SOUND = sounds.DYNAMITE_SOUND
    self.constants = constants


class AtomBomb(Bomb):
  NAME = 'Atom Bomb'
  DESCRIPTION = 'I am become Death, the destroyer of worlds.'
  BLAST_RADIUS = 10
  MIN_LEVEL = 20
  time_remaining = 20

  def __init__(self, constants):
    self.SOUND = sounds.ATOM_BOMB_SOUND
    self.constants = constants


def list_bombs(constants):
  return (CherryBomb(constants), (Dynamite(constants)), (AtomBomb(constants)))


#
# TESTS
#

def test_list_bombs(constants):
  for bomb in list_bombs(constants):
    assert bomb.BLAST_RADIUS > 0, 'missing BLAST_RADIUS'
    assert len(bomb.NAME) > 0, 'missing NAME'

def run_tests(constants):
  test_list_bombs(constants)
