# Copyright (c) 2013-2015 by Joel Odom & Alex Odom, Marietta, GA All Rights Reserved


class Lantern:
  pass


class Candle(Lantern):
  def __init__(self, constants):
    self.NAME = 'Candle'
    self.RADIUS = 2
    self.DESCRIPTION = 'Don\'t blow it out...'
    self.MIN_LEVEL = 1


def list_lanterns(constants):
  return ( Candle(constants), )


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
