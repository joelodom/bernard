# Copyright (c) 2013-2015 by Joel Odom & Alex Odom, Marietta, GA All Rights Reserved

import random
import pygame
import colors

class Weapon:
  def __init__(self, constants):
    self.constants = constants
    self.charge = constants.MAX_WEAPON_CHARGE

  def draw(self, player, screen):
    beam_length_ns = self.BEAM_LENGTH*self.constants.CELL_HEIGHT
    beam_length_ew = self.BEAM_LENGTH*self.constants.CELL_WIDTH

    for i in range(self.NUMBER_OF_BOLTS):
      # start from center of cell
      start_point = (
        self.constants.CELL_WIDTH*player.x + self.constants.CELL_WIDTH//2,
        self.constants.CELL_HEIGHT*player.y + self.constants.CELL_HEIGHT//2)

      for j in range(self.BEAM_SEGMENTS):
        if player.facing == 0: # north
          end_point = (random.randint(start_point[0] - self.BEAM_WIDTH_STEP,
            start_point[0] + self.BEAM_WIDTH_STEP),
            start_point[1] - beam_length_ns//self.BEAM_SEGMENTS)
        elif player.facing == 1: # east
          end_point = (start_point[0] + beam_length_ew//self.BEAM_SEGMENTS,
            random.randint(start_point[1] - self.BEAM_WIDTH_STEP,
            start_point[1] + self.BEAM_WIDTH_STEP))
        elif player.facing == 2: # south
          end_point = (random.randint(start_point[0] - self.BEAM_WIDTH_STEP,
            start_point[0] + self.BEAM_WIDTH_STEP),
            start_point[1] + beam_length_ns//self.BEAM_SEGMENTS)
        else: # west
          end_point = (start_point[0] - beam_length_ew//self.BEAM_SEGMENTS,
            random.randint(start_point[1] - self.BEAM_WIDTH_STEP,
            start_point[1] + self.BEAM_WIDTH_STEP))

        pygame.draw.line(screen, colors.SOLID_CYAN, start_point, end_point,
          self.BEAM_WIDTH)
        start_point = end_point


class MiniBlaster(Weapon):
  def __init__(self, constants):
    super(MiniBlaster, self).__init__(constants)

    self.COST = 25
    self.NAME = 'Mini Blaster'
    self.DESCRIPTION = 'A weapon of underawing power.'
    self.BEAM_LENGTH = 1;
    self.BEAM_WIDTH_STEP = 5
    self.BEAM_SEGMENTS = 5
    self.BEAM_WIDTH = 1
    self.NUMBER_OF_BOLTS = 1
    self.DAMAGE = 4

class SuperMegaCannon(Weapon):
  def __init__(self, constants):
    super(SuperMegaCannon, self).__init__(constants)

    self.COST = 12500
    self.NAME = 'Super Mega Cannon'
    self.DESCRIPTION = 'A weapon of awesome power.'
    self.BEAM_LENGTH = 12;
    self.BEAM_WIDTH_STEP = 50
    self.BEAM_SEGMENTS = 10
    self.BEAM_WIDTH = 5
    self.NUMBER_OF_BOLTS = 5
    self.DAMAGE = 18

class MultiBlaster(Weapon):
  def __init__(self, constants):
    super(MultiBlaster, self).__init__(constants)

    self.COST = 0 # need to change if it can ever be bought
    self.NAME = 'Multi Blaster'
    self.DESCRIPTION = 'This wepon shoots two beams at once, making the scare time on monsters longer.'
    self.BEAM_LENGTH = 1;
    self.BEAM_WIDTH_STEP = 10
    self.BEAM_SEGMENTS = 5
    self.BEAM_WIDTH = 2
    self.NUMBER_OF_BOLTS = 2
    self.DAMAGE = 8

def list_weapons(constants):
  # returns a tuple with an instance of each weapon type
  return ( MiniBlaster(constants), SuperMegaCannon(constants), MultiBlaster(constants) )

#
# TESTS
#

def test_list_weapons(constants):
  # makes sure that every weapon has expected constants
  for weapon in list_weapons(constants):
    assert weapon.BEAM_LENGTH > 0, 'missing BEAM_LENGTH'
    assert weapon.BEAM_WIDTH_STEP > 0, 'missing BEAM_WIDTH_STEP'
    assert weapon.BEAM_SEGMENTS > 0, 'missing BEAM_SEGMENTS'
    assert weapon.BEAM_WIDTH > 0, 'missing BEAM_WIDTH'
    assert weapon.NUMBER_OF_BOLTS > 0, 'missing NUMBER_OF_BOLTS'
    assert weapon.charge > 0, 'missing charge'

def run_tests(constants):
  test_list_weapons(constants)
