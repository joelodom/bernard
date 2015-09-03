import pygame
import colors


BORDER_WIDTH = 3


class ListBoxItem:
  pass


class ListBox:
  def __init__(self, x, y, width, height):
    self.x = x
    self.y = y
    self.surface = pygame.Surface((width, height))
    self.items = []
    self.selected_item = 0

  def add_item(self, item):
    '''Adds an item to the listbox.

    Items must have the following properties: TEXT.
    '''
    self.items.append(item)

  def select_next_item(self):
    if self.selected_item < len(self.items) - 1:
      self.selected_item += 1

  def select_previous_item(self):
    if self.selected_item > 0:
      self.selected_item -= 1

  def draw(self, surface):
    # draw background
    (my_width, my_height) = self.surface.get_size()
    pygame.draw.rect(self.surface, colors.SOLID_BLACK, (0, 0, my_width, my_height))

    # draw the items

    current_item = 0
    place_item_text_y = 20
    place_item_text_x = 20
    font = pygame.font.SysFont("monospace", 20)

    for item in self.items:
      if current_item == self.selected_item:
        rendered = font.render(item.TEXT, True, colors.SOLID_WHITE, colors.SOLID_BLUE)
      else:
        rendered = font.render(item.TEXT, True, colors.SOLID_WHITE)

      (rendered_width, rendered_height) = font.size(item.TEXT)
      self.surface.blit(rendered, (place_item_text_x, place_item_text_y))

      place_item_text_y = place_item_text_y + round(1.5*rendered_height)

      current_item += 1

    # draw a border around the control
    pygame.draw.rect(self.surface, colors.SOLID_WHITE, (0, 0, my_width, my_height), BORDER_WIDTH)

    # blit to input surface
    surface.blit(self.surface, (self.x, self.y))
