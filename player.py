# Copyright (c) 2013-2015 by Joel Odom & Alex Odom, Marietta, GA All Rights Reserved

import pygame
import colors
import sounds
import food
import images
import bombs


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

    # for testing only, give the player one of every bomb
    self.bombs = []
    self.bombs.extend(bombs.list_bombs(constants))

  def draw(self, surface):
    images.draw_image_in_cell(self.constants, surface, images.PLAYER, self.x, self.y)

  def handle_monster_collision(self, monster):
    sounds.PLAYER_HIT_SOUND.play()
    self.health = self.health - monster.DAMAGE
