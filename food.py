# Copyright (c) 2013-2015 by Joel Odom & Alex Odom, Marietta, GA All Rights Reserved

import pygame


class Food:
  pass


class RottenApple(Food):
  def __init__(self):
    self.NAME = 'Rotten Apple'
    self.COST = 1
    self.HEALTH_HEAL = 1
    self.DESCRIPTION = ('A gross apple with worms in it (Heals '
      + str(self.HEALTH_HEAL) + ' health)')


class Apple(Food):
  def __init__(self):
    self.NAME = 'Apple'
    self.COST = 6
    self.HEALTH_HEAL = 3
    self.DESCRIPTION = ('A good cruchy snack to take along in your travels (Heals '
      + str(self.HEALTH_HEAL) + ' health)')


class Cake(Food):
  def __init__(self):
    self.NAME = 'Cake'
    self.COST = 12
    self.HEALTH_HEAL = 6
    self.DESCRIPTION = ('A perfect thing for a birthday treat (Heals '
      + str(self.HEALTH_HEAL) + ' health)')


def list_food():
  return ( RottenApple(), Apple(), Cake() )


#
# TESTS
#

def test_list_food():
  for food in list_food():
    assert len(food.NAME) > 0, 'missing NAME'
    assert food.COST > 0, 'missing COST'
    assert food.HEALTH_HEAL > 0, 'missing HEALTH_HEAL'
    assert len(food.DESCRIPTION) > 0, 'missing DESCRIPTION'

def run_tests(constants):
  test_list_food()
