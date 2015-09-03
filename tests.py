# Copyright (c) 2013 by Joel Odom & Alex Odom, Marietta, GA All Rights Reserved

import monsters
import weapons
import food
import bombs

def run_tests(constants):
  monsters.run_tests(constants)
  weapons.run_tests(constants)
  food.run_tests(constants)
  bombs.run_tests(constants)
  print('Tests completed.')
