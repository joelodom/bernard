# Copyright (c) 2013-2015 by Joel Odom & Alex Odom, Marietta, GA All Rights Reserved

import pygame
import colors
import sounds
import food
import images
import bombs
import lanterns
import weapons


class Player:
  def __init__(self, constants):
    self.constants = constants
    self.MAX_HEALTH = 100
    self.health = self.MAX_HEALTH
    self.x = 0
    self.y = 0
    self.facing = 2 # south

    self.food = []
    self.selected_food = None

    self.bombs = []
    self.selected_bomb = None

    #Turn on for development only
    #self.lantern = lanterns.FullMap(constants)
    self.lantern = lanterns.Candle(constants) # a starter lantern
    self.weapon = weapons.MiniBlaster(constants)

  def draw(self, surface):
    images.draw_image_in_cell(self.constants, surface, images.PLAYER, self.x, self.y)

  def handle_monster_collision(self, monster):
    sounds.PLAYER_HIT_SOUND.play()
    self.health = self.health - monster.DAMAGE

  def use_selected_bomb(self):
    if self.selected_bomb != None:
      self.bombs.remove(self.selected_bomb)
      self.selected_bomb = self.bombs[0] if len(self.bombs) > 0 else None

  def use_selected_food(self):
    if self.selected_food != None:
      self.food.remove(self.selected_food)
      self.increase_health(self.selected_food.HEALTH_HEAL)
      self.selected_food = self.food[0] if len(self.food) > 0 else None

  def increase_health(self, amount):
    self.health += amount
    if self.health > self.MAX_HEALTH:
      self.health = self.MAX_HEALTH

  def give_items(self, items):
    for item in items:
      if isinstance(item, food.Food):
        self.food.append(item)
        if self.selected_food == None and len(self.food) > 0:
          self.selected_food = self.food[0]
      elif isinstance(item, bombs.Bomb):
        self.bombs.append(item)
        if self.selected_bomb == None and len(self.bombs) >0:
          self.selected_bomb = self.bombs[0]
      elif isinstance(item, lanterns.Lantern):
        # automatically upgrade lantern for now
        if item.RADIUS > self.lantern.RADIUS:
          self.lantern = item
