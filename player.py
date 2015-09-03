# Copyright (c) 2013 by Joel Odom & Alex Odom, Marietta, GA All Rights Reserved

import pygame
import colors
import sounds
import food


class Player:
  def __init__(self, constants):
    self.constants = constants
    self.MAX_HEALTH = 100
    self.health = 100
    self.x = 0
    self.y = 0
    self.facing = 2 # south

    # for testing only, give the player one of every food item
    self.food = []
    self.food.extend(food.list_food())

  def draw(self, surface):
    pygame.draw.rect(surface, colors.SOLID_BLUE,
      (self.constants.CELL_WIDTH*self.x + self.constants.WALL_WIDTH,
      self.constants.CELL_HEIGHT*self.y + self.constants.WALL_WIDTH,
      self.constants.CELL_WIDTH - 2*self.constants.WALL_WIDTH,
      self.constants.CELL_HEIGHT - 2*self.constants.WALL_WIDTH), 0)

  def handle_monster_collision(self, monster):
    sounds.PLAYER_HIT_SOUND.play()
    self.health = self.health - monster.DAMAGE
