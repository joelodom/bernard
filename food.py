# Copyright (c) 2013 by Joel Odom & Alex Odom, Marietta, GA All Rights Reserved

import pygame


class Food:
  pass


class RottenApple(Food):
  def __init__(self):
    self.COST = 1
    self.NAME = 'Rotten Apple'
    self.DESCRIPTION = 'A gross apple with worms in it.'
    self.HEALTH_HEAL = 1


class Apple(Food):
  def __init__(self):
    self.COST = 6
    self.NAME = 'Apple'
    self.DESCRIPTION = 'A good cruchy snack to take along in your travels.'
    self.HEALTH_HEAL = 3


class Cake(Food):
  def __init__(self):
    self.COST = 12
    self.NAME = 'Cake'
    self.DESCRIPTION = 'A perfect thing for a birthday treat'
    self.HEALTH_HEAL = 6


def list_food():
  return ( RottenApple(), Apple(), Cake() )


#
# TESTS
#

def test_list_food():
  for food in list_food():
    assert food.HEALTH_HEAL > 0, 'missing HEALTH_HEAL'

def run_tests(constants):
  test_list_food()
