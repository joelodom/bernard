# Copyright (c) 2013-2015 by Joel Odom & Alex Odom, Marietta, GA All Rights Reserved

import random
import images
import food
import bombs

TIER_1 = '1'
TIER_1_LOCKED = '1l'

class Chest:
  def __init__(self, constants):

    self.constants = constants

    self.TIER = random.choice(
      [TIER_1, TIER_1, TIER_1, TIER_1, TIER_1, TIER_1_LOCKED, TIER_1_LOCKED])

    if self.TIER == TIER_1:
      self.IMAGE = images.TIER_1_CHEST
    elif self.TIER == TIER_1_LOCKED:
      self.IMAGE = images.TIER_1_LOCKED_CHEST

    #
    # Chest contents require the following attributes: MIN_LEVEL
    # Additionally, the prototype constructor should take one parameter, constants.
    #

    self.contents = []
    possible_contents = []
    possible_contents.extend(food.list_food(constants))
    possible_contents.extend(bombs.list_bombs(constants))

    num_items = 0
    max_items = random.randint(1, 3) # one to three items per chest
    while num_items < max_items:
      item_prototype = random.choice(possible_contents)
      if item_prototype.MIN_LEVEL > constants.LEVEL:
        continue
      new_item = type(item_prototype)(constants)
      self.contents.append(new_item)
      num_items += 1


    # set location randomly, but avoid stairs
    # NOTE (maybe TODO): there could be multiple chests at the same location

    while True:
      self.x = random.randint(0, self.constants.MAZE_WIDTH - 1)
      self.y = random.randint(0, self.constants.MAZE_HEIGHT - 1)
      if self.x == 0 and self.y == 0:
        continue
      if self.x == self.constants.MAZE_WIDTH - 1 and self.y == self.constants.MAZE_HEIGHT - 1:
        continue
      break


class ChestsInMaze:
  def __init__(self, constants):
    self.constants = constants

    # populate the maze with random chest
    self.chests = []
    while len(self.chests) < self.constants.NUMBER_OF_CHESTS:
      self.chests.append(Chest(constants))


  def draw(self, surface):
    cell_width = self.constants.SCREEN_WIDTH//self.constants.MAZE_WIDTH
    cell_height = self.constants.SCREEN_HEIGHT//self.constants.MAZE_HEIGHT

    for chest in self.chests:
      images.draw_image_in_cell(self.constants, surface, chest.IMAGE, chest.x, chest.y)
