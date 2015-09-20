# Copyright (c) 2013-2015 by Joel Odom & Alex Odom, Marietta, GA All Rights Reserved

import pygame
import colors


# tunables

UNFOCUSED_BORDER_WIDTH = 1
FOCUSED_BORDER_WIDTH = 3

TITLE_X_INDENT = 10 # pixles

SELECTED_BORDER_X_INDENT = 8 # pixles
SELECTED_BORDER_Y_SPACING = 2 # pixles

TEXT_BOX_LINE_SPACING = 4 # pixles

class ListBoxItem:
  def __init__(self, short_text, verbose_text, associated_object):
    self.short_text = short_text
    self.verbose_text = verbose_text
    self.associated_object = associated_object


NO_SELECTED_ITEM = -1


class ListBox:
  def __init__(self, x, y, width, height, title = None):
    self.x = x
    self.y = y
    self.surface = pygame.Surface((width, height))
    self.items = []
    self.selected_item = NO_SELECTED_ITEM
    self.title = title
    self.focused = False

  def set_focus(self, focused = True):
    self.focused = focused

  def add_item(self, item):
    self.items.append(item)
    self.selected_item = 0 # this currently assumes that items are added before drawing / using

  def select_next_item(self):
    if self.selected_item == NO_SELECTED_ITEM:
      return
    if self.selected_item < len(self.items) - 1:
      self.selected_item += 1

  def select_previous_item(self):
    if self.selected_item == NO_SELECTED_ITEM:
      return
    if self.selected_item > 0:
      self.selected_item -= 1

  def get_short_text(self):
    if self.selected_item == NO_SELECTED_ITEM:
      return None
    return self.items[self.selected_item].short_text

  def get_verbose_text(self):
    if self.selected_item == NO_SELECTED_ITEM:
      return None
    return self.items[self.selected_item].verbose_text

  def get_associated_object(self):
    if self.selected_item == NO_SELECTED_ITEM:
      return None
    return self.items[self.selected_item].associated_object

  def draw(self, surface):

    font = pygame.font.SysFont("monospace", 20)
    (my_width, my_height) = self.surface.get_size()

    # draw the background
    pygame.draw.rect(self.surface, colors.SOLID_BLACK, (0, 0, my_width, my_height))

    # calculate title sizes

    title_height = 0

    if self.title != None:
      (rendered_width, title_height) = font.size(self.title)

    # draw the items

    current_item = 0
    place_item_text_y = 20 + title_height
    place_item_text_x = 20

    for item in self.items:

      # draw the item text

      rendered = font.render(item.short_text, True, colors.SOLID_WHITE)
      (rendered_width, rendered_height) = font.size(item.short_text)
      self.surface.blit(rendered, (place_item_text_x, place_item_text_y))

      # draw a box around the selected item if we have focus

      if self.focused and current_item == self.selected_item:
        pygame.draw.rect(self.surface, colors.SOLID_BLUE,
          (SELECTED_BORDER_X_INDENT, place_item_text_y - SELECTED_BORDER_Y_SPACING,
          my_width - 2*SELECTED_BORDER_X_INDENT, rendered_height + 2*SELECTED_BORDER_Y_SPACING),
          FOCUSED_BORDER_WIDTH)

      # go to the next item

      place_item_text_y = place_item_text_y + round(1.5*rendered_height)
      current_item += 1

    # draw a border around the control
    pygame.draw.rect(self.surface, colors.SOLID_WHITE,
      (0, round(title_height/2), my_width, my_height - round(title_height/2)),
      FOCUSED_BORDER_WIDTH if self.focused else UNFOCUSED_BORDER_WIDTH)

    # draw the title

    if self.title != None:
      rendered = font.render(self.title, True, colors.SOLID_WHITE, colors.SOLID_BLACK)
      self.surface.blit(rendered, (TITLE_X_INDENT, 0))

    # blit to input surface
    surface.blit(self.surface, (self.x, self.y))


class TextBox:
  def __init__(self, x, y, width, height, text = ""):
    self.x = x
    self.y = y
    self.surface = pygame.Surface((width, height))
    self.set_text(text)

  def set_text(self, text):
    self.text = text

  def draw(self, surface):

    font = pygame.font.SysFont("monospace", 20)
    (my_width, my_height) = self.surface.get_size()

    # draw the background
    pygame.draw.rect(self.surface, colors.SOLID_BLACK, (0, 0, my_width, my_height))

    # draw the text line by line

    if self.text != None:
      current_y = TEXT_BOX_LINE_SPACING;
      for line in self.text.splitlines():
        rendered = font.render(line, True, colors.SOLID_WHITE)
        (rendered_width, rendered_height) = font.size(line)
        self.surface.blit(rendered, (10, current_y))
        current_y += TEXT_BOX_LINE_SPACING + rendered_height

    # draw a border around the control
    pygame.draw.rect(self.surface, colors.SOLID_WHITE, (0, 0, my_width, my_height),
      UNFOCUSED_BORDER_WIDTH)

    # blit to input surface
    surface.blit(self.surface, (self.x, self.y))
