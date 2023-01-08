# Copyright (c) 2013 by Joel Odom & Alex Odom, Marietta, GA All Rights Reserved

import pygame
import food
import sys
import weapons
import colors

BORDER_WIDTH = 10


class Store:
  def __init__(self, constants):
    self.constants = constants
    self.items = food.list_food(constants) + weapons.list_weapons(constants)
    self.selected_item = 0
    self.selection_box_topleftx = BORDER_WIDTH
    self.selection_box_toplefty = BORDER_WIDTH + 7


  def seize(self):
    # draw the store
    surface = pygame.display.get_surface()

    # handle events
    while True:
      self.draw(surface)
      pygame.display.update()

      event = pygame.event.wait()

      if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
        return

      elif (event.type == pygame.KEYUP and event.key == pygame.K_DOWN
        and self.selected_item < len(self.items) - 1):
        self.selected_item = self.selected_item + 1

      elif (event.type == pygame.KEYUP and event.key == pygame.K_UP
        and self.selected_item > 0):
        self.selected_item = self.selected_item - 1


  def draw(self, surface):
    pygame.draw.rect(surface, colors.SOLID_BLACK, (0, 0,
      self.constants.SCREEN_WIDTH, self.constants.SCREEN_HEIGHT), 0)

    pygame.draw.rect(surface, colors.SOLID_GRAY, (0, 0,
      self.constants.SCREEN_WIDTH, self.constants.SCREEN_HEIGHT), BORDER_WIDTH)

    item_number = 0
    place_item_text_y = 20
    place_item_text_x = 20
    store_font = pygame.font.SysFont("monospace", 20)

    for item in self.items:

      product = '%s. %s - $%s' % (item_number + 1, item.NAME, item.COST)
      product_desciption = item.DESCRIPTION

      product_text = store_font.render(product, True, colors.SOLID_WHITE)
      (width, height) = store_font.size(product)
      surface.blit(product_text, (place_item_text_x, place_item_text_y))

      box_top = place_item_text_y - 6
      place_item_text_y = place_item_text_y + int(0.8 * height)

      product_desciption_text = store_font.render(
        product_desciption, True, colors.SOLID_WHITE)
      surface.blit(
        product_desciption_text, (place_item_text_x, place_item_text_y))

      place_item_text_y = place_item_text_y + int(1.9 * height)

      if item_number == self.selected_item:
        pygame.draw.rect(surface, colors.SOLID_GRAY,
          (place_item_text_x - 4, box_top,
           self.constants.SCREEN_WIDTH - 30, 2.0*height), 5)

      item_number = item_number + 1
