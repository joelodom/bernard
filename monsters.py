# Copyright (c) 2013 by Joel Odom & Alex Odom, Marietta, GA All Rights Reserved

import random
import pygame
import third_party.maze
import colors
import images


class Monster:
  def __init__(self, constants, avoid_x, avoid_y):
    self.constants = constants

    # defaults
    self.DAMAGE = 1
    self.COLOR = colors.SOLID_GREEN
    self.IMAGE = None

    # the monster will run away while it is scared
    self.scared_ticks = 0 # ticks remaining

    # set location randomly

    self.x = random.randint(0, self.constants.MAZE_WIDTH - 1)
    self.y = random.randint(0, self.constants.MAZE_HEIGHT - 1)

    while abs(self.x - avoid_x) <= self.constants.MONSTER_BUFFER_SIZE:
      self.x = random.randint(0, self.constants.MAZE_WIDTH - 1)
    while abs(self.y - avoid_y) <= self.constants.MONSTER_BUFFER_SIZE:
      self.y = random.randint(0, self.constants.MAZE_HEIGHT - 1)

  def may_move(self, maze, direction):
    return not maze.get_walls(self.x, self.y)[direction]


class Rat(Monster):
  def __init__(self, constants, avoid_x, avoid_y):
    super(Rat, self).__init__(constants, avoid_x, avoid_y)
    self.DAMAGE = 1
    self.IMAGE = images.RAT


class Ghost(Monster):
  def __init__(self, constants, avoid_x, avoid_y):
    super(Ghost, self).__init__(constants, avoid_x, avoid_y)
    self.DAMAGE = 2
    self.COLOR = colors.SOLID_WHITE

  def may_move(self, maze, direction):
    if direction == 0:
      return self.y > 0
    if direction == 1:
      return self.x < self.constants.MAZE_WIDTH - 1
    if direction == 2:
      return self.y < self.constants.MAZE_HEIGHT - 1
    # direction == 3
    return self.x > 0


def check_for_preferred_direction(maze, monster, player):
  # check north
  y = monster.y
  while not maze.get_walls(monster.x, y)[0]:
    y = y - 1
    if player.x == monster.x and player.y == y:
      return 0

  # check east
  x = monster.x
  while not maze.get_walls(x, monster.y)[1]:
    x = x + 1
    if player.x == x and player.y == monster.y:
      return 1

  # check south
  y = monster.y
  while not maze.get_walls(monster.x, y)[2]:
    y = y + 1
    if player.x == monster.x and player.y == y:
      return 2

  # check west
  x = monster.x
  while not maze.get_walls(x, monster.y)[3]:
    x = x - 1
    if player.x == x and player.y == monster.y:
      return 3

  return None


class MonstersInMaze:
  def __init__(self, constants, avoid_x, avoid_y):
    self.constants = constants

    # populate the maze with random monsters
    self.monsters = []
    while len(self.monsters) < self.constants.NUMBER_OF_MONSTERS:
      if random.randint(0, 2) == 0:
        self.monsters.append(Ghost(self.constants, avoid_x, avoid_y))
      else:
        self.monsters.append(Rat(self.constants, avoid_x, avoid_y))

  def draw(self, surface):
    cell_width = self.constants.SCREEN_WIDTH//self.constants.MAZE_WIDTH
    cell_height = self.constants.SCREEN_HEIGHT//self.constants.MAZE_HEIGHT

    for monster in self.monsters:
      if monster.IMAGE != None:
        images.draw_image_in_cell(self.constants, surface, monster.IMAGE, monster.x, monster.y)
      else: # draw as a solid color for now
        pygame.draw.rect(surface, monster.COLOR,
          (cell_width*monster.x + self.constants.WALL_WIDTH,
          cell_height*monster.y + self.constants.WALL_WIDTH,
          cell_width - 2*self.constants.WALL_WIDTH,
          cell_height - 2*self.constants.WALL_WIDTH), 0)

  def tick(self, maze, player, weapon_hit_squares):
    for monster in self.monsters:
      # check for weapon hit
      for square in weapon_hit_squares:
        if monster.x == square[0] and monster.y == square[1]:
          monster.scared_ticks = player.weapon.DAMAGE
          break
      else:
        if monster.scared_ticks > 0:
          monster.scared_ticks = monster.scared_ticks - 1

      # 0 = North, 1 = East, 2 = South, 3 = West
      preferred_direction = check_for_preferred_direction(maze, monster, player)

      # determine directions to try

      if preferred_direction == None:
        directions_to_try = [0, 1, 2, 3]
        random.shuffle(directions_to_try)
      else:
        if monster.scared_ticks > 0:
          # run away if scared
          if preferred_direction == 0:
            directions_to_try = [1, 3]
            random.shuffle(directions_to_try)
            directions_to_try.insert(0, 2)
          elif preferred_direction == 1:
            directions_to_try = [0, 2]
            random.shuffle(directions_to_try)
            directions_to_try.insert(0, 3)
          elif preferred_direction == 2:
            directions_to_try = [0, 2]
            random.shuffle(directions_to_try)
            directions_to_try.insert(0, 0)
          else:
            directions_to_try = [0, 2]
            random.shuffle(directions_to_try)
            directions_to_try.insert(0, 1)
        else: # not scared
          directions_to_try = [preferred_direction]

      # move

      while len(directions_to_try) > 0:
        direction = directions_to_try.pop(0)

        if monster.may_move(maze, direction):
          if direction == 0:
            monster.y = monster.y - 1
            if player.x == monster.x and player.y == monster.y:
              player.handle_monster_collision(monster)
              monster.y = monster.y + 1 # don't go through player
          elif direction == 1:
            monster.x = monster.x + 1
            if player.x == monster.x and player.y == monster.y:
              player.handle_monster_collision(monster)
              monster.x = monster.x - 1 # don't go through player
          elif direction == 2:
            monster.y = monster.y + 1
            if player.x == monster.x and player.y == monster.y:
              player.handle_monster_collision(monster)
              monster.y = monster.y - 1 # don't go through player
          else: # direction == 3
            monster.x = monster.x - 1
            if player.x == monster.x and player.y == monster.y:
              player.handle_monster_collision(monster)
              monster.x = monster.x + 1 # don't go through player
          break # move successful

  def get_monsters_at(self, x, y):
    monsters = []
    for monster in self.monsters:
      if monster.x == x and monster.y == y:
        monsters.append(monster)
    return monsters


#
# TESTS
#

def test_monster_count(constants):
  maze = third_party.maze.Maze(
    width = constants.MAZE_WIDTH, height = constants.MAZE_HEIGHT)
  monsters_in_maze = MonstersInMaze(constants, 0, 0)
  assert len(monsters_in_maze.monsters) == constants.NUMBER_OF_MONSTERS, (
    'monster count failed')

def test_moster_buffer(constants):
  maze = third_party.maze.Maze(
    width = constants.MAZE_WIDTH, height = constants.MAZE_HEIGHT)
  AVOID_X = 15
  AVOID_Y = 15
  monsters_in_maze = MonstersInMaze(constants, AVOID_X, AVOID_Y)
  for monster in monsters_in_maze.monsters:
    assert abs(monster.x - AVOID_X) > constants.MONSTER_BUFFER_SIZE, (
      'monster buffer test failed')
    assert abs(monster.y - AVOID_Y) > constants.MONSTER_BUFFER_SIZE, (
      'monster buffer test failed')

def test_monster_parameters(constants):
  maze = third_party.maze.Maze(
    width = constants.MAZE_WIDTH, height = constants.MAZE_HEIGHT)
  monsters_in_maze = MonstersInMaze(constants, 0, 0)
  for monster in monsters_in_maze.monsters:
    assert monster.DAMAGE > 0, ('bad monster DAMAGE')

def run_tests(constants):
  test_monster_count(constants)
  test_moster_buffer(constants)
  test_monster_parameters(constants)
