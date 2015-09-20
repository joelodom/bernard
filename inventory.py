# Copyright (c) 2013-2015 by Joel Odom & Alex Odom, Marietta, GA All Rights Reserved

import pygame
import colors
import gui
import bernard


BORDER_WIDTH = 10
CONTROL_SPACING = 30

LIST_BOX_WIDTH = 200
LIST_BOX_HEIGHT = 200

class Inventory:
  def __init__(self, player):

    self.player = player

    # add food list box
    self.list_box_food = gui.ListBox(CONTROL_SPACING, 10, LIST_BOX_WIDTH, LIST_BOX_HEIGHT, 'Food')
    for food_item in player.food:
      item = gui.ListBoxItem(food_item.NAME, food_item.DESCRIPTION, food_item)
      self.list_box_food.add_item(item)

    # add bombs list box
    self.list_box_bombs = gui.ListBox(
      LIST_BOX_WIDTH + 2*CONTROL_SPACING, 10, LIST_BOX_WIDTH, LIST_BOX_HEIGHT, 'Bombs')
    for bomb in player.bombs:
      item = gui.ListBoxItem(bomb.NAME, bomb.DESCRIPTION, bomb)
      item.TEXT = bomb.NAME
      self.list_box_bombs.add_item(item)

    # focus on the food list box
    self.list_box_food.set_focus()
    self.focused_control = self.list_box_food

    # add the descriptive text box
    self.descriptive_text_box = gui.TextBox(CONTROL_SPACING, 300, 800, 50);

    # add the action text box
    self.action_text_box = gui.TextBox(CONTROL_SPACING, 400, 800, 50);


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
        self.focused_control.select_previous_item()
        need_redraw = True

      elif event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
        self.focused_control.select_next_item()
        need_redraw = True

      elif event.type == pygame.KEYUP and event.key == pygame.K_TAB:
        if self.focused_control == self.list_box_food:
          self.list_box_food.set_focus(False)
          self.list_box_bombs.set_focus()
          self.focused_control = self.list_box_bombs
        else:
          self.list_box_food.set_focus()
          self.list_box_bombs.set_focus(False)
          self.focused_control = self.list_box_food
        need_redraw = True

      elif event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
        # these may be set to None, which is okay
        if self.focused_control == self.list_box_food:
          self.player.selected_food = self.list_box_food.get_associated_object()
        else:
          self.player.selected_bomb = self.list_box_bombs.get_associated_object()
        return # exit inventory screen


      # TODO: handle resize

      elif event.type == pygame.QUIT:
        bernard.exit_program()


  def draw(self, surface):
    # update the text box text

    verbose_text = self.focused_control.get_verbose_text()
    if verbose_text == None:
      verbose_text = ""

    short_text = self.focused_control.get_short_text()
    if short_text == None:
      short_text = ""

    self.descriptive_text_box.set_text(verbose_text)
    self.action_text_box.set_text("Press [ENTER] to select %s" % short_text)

    # draw a background and a border
    (surface_width, surface_height) = surface.get_size()
    pygame.draw.rect(surface, colors.SOLID_BLACK, (0, 0, surface_width, surface_height), 0)
    pygame.draw.rect(surface, colors.SOLID_GRAY, (0, 0, surface_width, surface_height),
      BORDER_WIDTH)

    # draw controls
    self.list_box_food.draw(surface)
    self.list_box_bombs.draw(surface)
    self.descriptive_text_box.draw(surface)
    self.action_text_box.draw(surface)
