# Copyright (c) 2013-2015 by Joel Odom & Alex Odom, Marietta, GA All Rights Reserved


class Lantern:
  pass


class Candle(Lantern):
  def __init__(self, constants):
    self.NAME = 'Candle'
    self.RADIUS = 1
    self.DESCRIPTION = 'Don\'t blow it out.'
    self.MIN_LEVEL = 1

class MiniFlashlight(Lantern):
  def __init__(self, constants):
    self.NAME = 'Mini Flashlight'
    self.RADIUS = 2
    self.DESCRIPTION = 'Batteries not included.'
    self.MIN_LEVEL = 3

class BigFlashlight(Lantern):
  def __init__(self, constants):
    self.NAME = 'Big Flashlight'
    self.RADIUS = 3
    self.DESCRIPTION = 'A light with a little more distance.'
    self.MIN_LEVEL = 8

class CampLantern(Lantern):
  def __init__(self, constants):
    self.NAME = 'Camp Lantern'
    self.RADIUS = 4
    self.DESCRIPTION = 'A very bright light.'
    self.MIN_LEVEL = 15

class HugeLantern(Lantern):
  def __init__(self, constants):
    self.NAME = 'Huge Lantern'
    self.RADIUS = 5
    self.DESCRIPTION = 'A sun in a bottle.'
    self.MIN_LEVEL = 20

#For development
'''class FullMap(Lantern):
  def __init__(self, constants):
    self.NAME = 'Full Map'
    self.RADIUS = 10000
    self.DESCRIPTION = 'Well, I guess you have this now.'
    self.MIN_LEVEL = 1'''


def list_lanterns(constants):
  return (Candle(constants), MiniFlashlight(constants), BigFlashlight(constants),
           CampLantern(constants), HugeLantern(constants))


#
# TESTS
#

def test_list_lanterns(constants):
  for lantern in list_lanterns(constants):
    assert len(lantern.NAME) > 0, 'missing NAME'
    assert lantern.RADIUS > 0, 'missing RADIUS'
    assert len(lantern.DESCRIPTION) > 0, 'missing DESCRIPTION'
    assert lantern.MIN_LEVEL > 0, 'missing MIN_LEVEL'

def run_tests(constants):
  test_list_lanterns(constants)
