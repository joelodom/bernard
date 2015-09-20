# Copyright (c) 2013-2015 by Joel Odom & Alex Odom, Marietta, GA All Rights Reserved

import pygame
import colors
import gui
import bernard


BORDER_WIDTH = 10


class Inventory:
  def __init__(self, player):
    self.player = player

    # add food list box
    self.list_box_food = gui.ListBox(10, 10, 200, 400, 'Food')
    for food_item in player.food:
      item = gui.ListBoxItem()
      item.TEXT = food_item.NAME
      self.list_box_food.add_item(item)

  def seize(self):
    surface = pygame.display.get_surface()
    need_redraw = True

    # handle events
    while True:
      if need_redraw:
        need_redraw = False
        self.draw(surface)
        pygame.display.update()

      event = pygame.event.wait()

      if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
        return # exit inventory screen

      elif event.type == pygame.KEYUP and event.key == pygame.K_UP:
        self.list_box_food.select_previous_item()
        need_redraw = True

      elif event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
        self.list_box_food.select_next_item()
        need_redraw = True

      # TODO: handle resize

      elif event.type == pygame.QUIT:
        bernard.exit_program()


  def draw(self, surface):
    # draw a background and a border
    (surface_width, surface_height) = surface.get_size()
    pygame.draw.rect(surface, colors.SOLID_BLACK, (0, 0, surface_width, surface_height), 0)
    pygame.draw.rect(surface, colors.SOLID_GRAY, (0, 0, surface_width, surface_height),
      BORDER_WIDTH)

    # draw controls
    self.list_box_food.draw(surface)
