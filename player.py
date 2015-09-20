# Copyright (c) 2013-2015 by Joel Odom & Alex Odom, Marietta, GA All Rights Reserved

import pygame
import colors
import sounds
import food
import images
import bombs


NO_SELECTED_ITEM = -1


class Player:
  def __init__(self, constants):
    self.constants = constants
    self.MAX_HEALTH = 100
    self.health = 100
    self.x = 0
    self.y = 0
    self.facing = 2 # south

    self.food = []
    self.selected_food = NO_SELECTED_ITEM

    self.bombs = []
    self.selected_bomb = NO_SELECTED_ITEM

    # for testing only, give the player some stuff
    self.food.extend(food.list_food())
    self.bombs.extend(bombs.list_bombs(constants))

  def draw(self, surface):
    images.draw_image_in_cell(self.constants, surface, images.PLAYER, self.x, self.y)

  def handle_monster_collision(self, monster):
    sounds.PLAYER_HIT_SOUND.play()
    self.health = self.health - monster.DAMAGE

  def get_selected_food(self):
    return self.food[self.selected_food] if self.selected_food != NO_SELECTED_ITEM else None

  def get_selected_bomb(self):
    return self.bombs[self.selected_bomb] if self.selected_bomb != NO_SELECTED_ITEM else None
