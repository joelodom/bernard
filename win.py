import pygame
import time
import colors
import sys

pygame.init()

class Win():

    INITIAL_WINDOW_SIZE = 0.9 # percent of screen
    LARGE_MESSAGE_FONT_DIVISOR = 75 # smaller number means bigger font
    info = pygame.display.Info()
    smallest_dim = min(info.current_w, info.current_h)
    win_size = round(INITIAL_WINDOW_SIZE*smallest_dim)
    screen = pygame.display.set_mode((win_size, win_size), pygame.RESIZABLE)
  
    def draw_centered_text(self,surface, message):
      '''Draws a centered message on any surface.'''
      (surface_width, surface_height) = surface.get_size()
      size = (surface_width + surface_height)//self.LARGE_MESSAGE_FONT_DIVISOR
      font = pygame.font.SysFont("monospace", size, bold=True)
      rendered_text = font.render(message, True, colors.SOLID_RED)
      (width, height) = font.size(message)
      surface.blit(rendered_text, ((surface_width - width)//2, (surface_height - height)//2))
      
    def draw_centered_message(self, screen, message):
      '''Draws a centered message on the game screen.

      Use this function if you plan to pause after drawing to hold an informational message
      on the game screen.
      '''
      self.draw_centered_text(self.screen, message)
      pygame.display.update()
      
    def __init__(self):
        self.screen.fill(colors.SOLID_BLACK)
        self.draw_centered_message(self.screen, "Congradulations! You have won by compleating level 25!")
        time.sleep(5)
        pygame.quit()
        sys.exit()
        
