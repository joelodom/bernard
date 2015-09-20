# Copyright (c) 2013-2015 by Joel Odom & Alex Odom, Marietta, GA All Rights Reserved

import pygame
import sys
import math
import random
import os
import third_party.maze
import monsters
import colors
import tests
import weapons
import player as player_module
import store as store_module
import bombs
import sounds
import images
import inventory
import gui
import chest


# tunables

PYTHON_MAJOR_VERSION = 3
PYTHON_MINOR_VERSION = 2

BASE_MAZE_WIDTH = 2 # cells
BASE_MAZE_HEIGHT = 2
MAZE_LEVEL_INCREASE = 1

INITIAL_WINDOW_SIZE = 0.9 # percent of screen

INITIAL_WINDOW_X = 200
INITIAL_WINDOW_Y = 50

WALL_COLOR = colors.SOLID_WHITE
WALL_WIDTH_DIVISOR = 7 # larger divisor means thinner walls

MONSTER_DENSITY = 0.02
CHEST_DENSITY = 0.01

CLOCK_TICK_MS = 500 # one unit of game time
WEAPON_TICK_MS = 100 # for weapon firing redraws and discharge

LANTERN_RADIUS = 5 # radius in cells

MONSTER_BUFFER_SIZE = 3 # cells (game may hang if this is too large!)

HEALTH_BAR_RELATIVE_X = 0.85
HEALTH_BAR_RELATIVE_Y = 0.02
HEALTH_BAR_RELATIVE_WIDTH = 0.13
HEALTH_BAR_RELATIVE_HEIGHT = 0.03
HEALTH_BAR_OUTLINE_WIDTH = 2 # pixels

CHARGE_BAR_RELATIVE_X = HEALTH_BAR_RELATIVE_X
CHARGE_BAR_RELATIVE_Y = HEALTH_BAR_RELATIVE_Y + HEALTH_BAR_RELATIVE_HEIGHT + 0.01
CHARGE_BAR_RELATIVE_WIDTH = HEALTH_BAR_RELATIVE_WIDTH
CHARGE_BAR_RELATIVE_HEIGHT = HEALTH_BAR_RELATIVE_HEIGHT
CHARGE_BAR_OUTLINE_WIDTH = HEALTH_BAR_OUTLINE_WIDTH # pixels

SELECTED_ITEMS_BOX_RELATIVE_X = 0.3
SELECTED_ITEMS_BOX_RELATIVE_Y = 0.02
SELECTED_ITEMS_BOX_RELATIVE_WIDTH = 0.5
SELECTED_ITEMS_BOX_RELATIVE_HEIGHT = 0.07

MESSAGE_FONT_DIVISOR = 25 # smaller number means bigger font

MAX_WEAPON_CHARGE = 10

# other constants (not intended to be tunable)
CLOCK_TICK_EVENT = pygame.USEREVENT + 1
WEAPON_TICK_EVENT = pygame.USEREVENT + 2


def draw_centered_text(surface, message):
  '''Draws a centered message on any surface.'''
  (surface_width, surface_height) = surface.get_size()
  size = (surface_width + surface_height)//MESSAGE_FONT_DIVISOR
  font = pygame.font.SysFont("monospace", size, bold=True)
  rendered_text = font.render(message, True, colors.SOLID_RED)
  (width, height) = font.size(message)
  surface.blit(rendered_text, ((surface_width - width)//2, (surface_height - height)//2))


def draw_centered_message(screen, message):
  '''Draws a centered message on the game screen.

  Use this function if you plan to pause after drawing to hold an informational message
  on the game screen.
  '''
  draw_centered_text(screen, message)
  pygame.display.update()


def build_background_surface(constants):
  background_surface = pygame.Surface(
    (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
  background_surface = background_surface.convert_alpha()
  background_surface.fill(colors.SOLID_BLACK)
  return background_surface


def build_maze_surface(maze, constants):

  # draw the maze

  maze_surface = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
  maze_surface = maze_surface.convert_alpha()
  maze_surface.fill(colors.TRANSPARENT)

  half_wall_width = constants.WALL_WIDTH//2
  if half_wall_width < 1: half_wall_width = 1

  quarter_wall_width = constants.WALL_WIDTH//4

  for y in range(constants.MAZE_HEIGHT):

    # get north and south boundaries
    north = constants.CELL_HEIGHT*y # pixels
    south = constants.CELL_HEIGHT*(y + 1)

    for x in range(constants.MAZE_WIDTH):

      # get cell wall placements
      walls = maze.get_walls(x, y)
      has_north_wall = walls[0]
      has_east_wall = walls[1]
      has_south_wall = walls[2]
      has_west_wall = walls[3]

      # get east and west boundaries
      east = constants.CELL_WIDTH*(x + 1)
      west = constants.CELL_WIDTH*x

      # draw walls

      if has_north_wall:
        start_x = west
        start_y = north + quarter_wall_width
        end_x = east
        end_y = start_y
        pygame.draw.line(maze_surface, constants.WALL_COLOR,
          (start_x, start_y), (end_x, end_y), half_wall_width)

      if has_east_wall:
        start_x = east - quarter_wall_width
        start_y = north
        end_x = start_x
        end_y = south
        pygame.draw.line(maze_surface, constants.WALL_COLOR,
          (start_x, start_y), (end_x, end_y), half_wall_width)

      if has_south_wall:
        start_x = east
        start_y = south - quarter_wall_width
        end_x = west
        end_y = start_y
        pygame.draw.line(maze_surface, constants.WALL_COLOR,
          (start_x, start_y), (end_x, end_y), half_wall_width)

      if has_west_wall:
        start_x = west + quarter_wall_width
        start_y= south
        end_x = start_x
        end_y = north
        pygame.draw.line(maze_surface, constants.WALL_COLOR,
          (start_x, start_y), (end_x, end_y), half_wall_width)

  # draw a rectangular border

  pygame.draw.rect(maze_surface, constants.WALL_COLOR,
    (-quarter_wall_width, -quarter_wall_width,
    constants.CELL_WIDTH*(constants.MAZE_WIDTH + 1) + half_wall_width,
    constants.CELL_HEIGHT*(constants.MAZE_HEIGHT + 1) + half_wall_width),
    half_wall_width)

  # draw stairs
  if constants.LEVEL > 1:
    images.draw_image_in_cell(constants, maze_surface, images.STAIRS_UP, 0, 0)
  images.draw_image_in_cell(constants, maze_surface, images.STAIRS_DOWN,
    constants.MAZE_WIDTH - 1, constants.MAZE_HEIGHT - 1)

  return maze_surface


def build_objects_surface(objects_in_maze, constants):

  # initialize the objects surface
  objects_surface = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
  objects_surface = objects_surface.convert_alpha()
  objects_surface.fill(colors.TRANSPARENT)

  # draw objects (note that this currently is a ChestsInMaze object, but this could change
  objects_in_maze.draw(objects_surface)

  return objects_surface


def apply_bomb_damage(bomb, player, monsters_in_maze, maze, constants):
  y_min = bomb.y - bomb.BLAST_RADIUS
  if y_min < 0: y_min = 0

  y_max = bomb.y + bomb.BLAST_RADIUS
  if y_max > constants.MAZE_HEIGHT - 1: y_max = constants.MAZE_HEIGHT - 1

  x_min = bomb.x - bomb.BLAST_RADIUS
  if x_min < 0: x_min = 0

  x_max = bomb.x + bomb.BLAST_RADIUS
  if x_max > constants.MAZE_WIDTH - 1: x_max = constants.MAZE_WIDTH - 1

  for y in range(y_min, y_max + 1):
    for x in range(x_min, x_max + 1):
      # calculate distance fraction (0.0 at bomb site, 1.0 at blast radius)
      dx = bomb.x - x
      dy = bomb.y - y
      distance_fraction = math.sqrt(dx*dx + dy*dy)/bomb.BLAST_RADIUS

      # possibly destroy interior walls

      walls = maze.get_walls(x, y)

      north = walls[0]
      east = walls[1]
      south = walls[2]
      west = walls[3]

      if y > 0:
        north = north and (random.random() < distance_fraction)
      if x < constants.MAZE_WIDTH - 1:
        east = east and (random.random() < distance_fraction)
      if y < constants.MAZE_HEIGHT - 1:
        south = south and (random.random() < distance_fraction)
      if x > 0:
        west = west and (random.random() < distance_fraction)

      maze.set_walls(x, y, (north, east, south, west))

      # damage player
      if x == player.x and y == player.y:
        damage = int((1.0 - distance_fraction)*player.MAX_HEALTH)
        if damage > 0:
          player.health = player.health - damage

      # scare monsters
      for monster in monsters_in_maze.get_monsters_at(x, y):
        scare = int((1.0 - distance_fraction)*7.0*bomb.BLAST_RADIUS)
        if scare > monster.scared_ticks:
          monster.scared_ticks = scare


def build_sprite_surface(
  constants, monsters_in_maze, weapons, weapon_is_firing, player, bomb, maze):

  # initialize the sprite surface
  sprite_surface = pygame.Surface(
    (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
  sprite_surface = sprite_surface.convert_alpha()
  sprite_surface.fill(colors.TRANSPARENT)

  # draw monsters
  monsters_in_maze.draw(sprite_surface)

  # draw bomb
  if bomb != None:
    if bomb.time_remaining > 0:
      bomb.draw(sprite_surface)
    else: # KABOOM!
      bomb.play_sound()
      pygame.draw.ellipse(sprite_surface, colors.SOLID_YELLOW,
        (constants.CELL_WIDTH*(bomb.x - bomb.BLAST_RADIUS)
        + constants.CELL_WIDTH//2,
        constants.CELL_HEIGHT*(bomb.y - bomb.BLAST_RADIUS)
        + constants.CELL_HEIGHT//2,
        2*constants.CELL_WIDTH*bomb.BLAST_RADIUS,
        2*constants.CELL_HEIGHT*bomb.BLAST_RADIUS), 0)
      bomb.exploded = True

  # draw weapon beam
  if player.weapon != None and weapon_is_firing:
    player.weapon.draw(player, sprite_surface)

  # draw player
  player.draw(sprite_surface)

  return sprite_surface


def build_lantern_surface(constants, player):
  lantern_surface = pygame.Surface(
    (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
  lantern_surface = lantern_surface.convert_alpha()
  lantern_surface.fill(colors.SOLID_BLACK)
  pygame.draw.ellipse(lantern_surface, colors.TRANSPARENT,
    (constants.CELL_WIDTH*(player.x - LANTERN_RADIUS)
      + constants.CELL_WIDTH//2,
    constants.CELL_HEIGHT*(player.y - LANTERN_RADIUS)
      + constants.CELL_HEIGHT//2,
    2*constants.CELL_WIDTH*LANTERN_RADIUS,
    2*constants.CELL_HEIGHT*LANTERN_RADIUS), 0)
  return lantern_surface


def build_info_surface(constants, player, bomb):
  # start with a transparent surface
  info_surface = pygame.Surface(
    (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
  info_surface = info_surface.convert_alpha()
  info_surface.fill(colors.TRANSPARENT)

  # draw bomb time left
  if bomb != None and bomb.time_remaining > 0:
    draw_centered_text(info_surface, str(bomb.time_remaining))

  # draw the health bar

  fraction_health_remaining = player.health/player.MAX_HEALTH

  pygame.draw.rect(info_surface, colors.SOLID_BLUE,
    (int(HEALTH_BAR_RELATIVE_X*constants.SCREEN_WIDTH),
    int(HEALTH_BAR_RELATIVE_Y*constants.SCREEN_HEIGHT),
    int(HEALTH_BAR_RELATIVE_WIDTH*constants.SCREEN_WIDTH),
    int(HEALTH_BAR_RELATIVE_HEIGHT*constants.SCREEN_HEIGHT)),
    HEALTH_BAR_OUTLINE_WIDTH)

  info_surface.fill(colors.SOLID_BLUE,
    (int(HEALTH_BAR_RELATIVE_X*constants.SCREEN_WIDTH),
    int(HEALTH_BAR_RELATIVE_Y*constants.SCREEN_HEIGHT),
    int(fraction_health_remaining*HEALTH_BAR_RELATIVE_WIDTH*constants.SCREEN_WIDTH),
    int(HEALTH_BAR_RELATIVE_HEIGHT*constants.SCREEN_HEIGHT)))

  # draw the weapon charge bar

  fraction_charge_remaining = player.weapon.charge/MAX_WEAPON_CHARGE

  pygame.draw.rect(info_surface, colors.SOLID_WHITE,
    (int(CHARGE_BAR_RELATIVE_X*constants.SCREEN_WIDTH),
    int(CHARGE_BAR_RELATIVE_Y*constants.SCREEN_HEIGHT),
    int(CHARGE_BAR_RELATIVE_WIDTH*constants.SCREEN_WIDTH),
    int(CHARGE_BAR_RELATIVE_HEIGHT*constants.SCREEN_HEIGHT)),
    CHARGE_BAR_OUTLINE_WIDTH)

  info_surface.fill(colors.SOLID_WHITE,
    (int(CHARGE_BAR_RELATIVE_X*constants.SCREEN_WIDTH),
    int(CHARGE_BAR_RELATIVE_Y*constants.SCREEN_HEIGHT),
    int(fraction_charge_remaining*CHARGE_BAR_RELATIVE_WIDTH*constants.SCREEN_WIDTH),
    int(CHARGE_BAR_RELATIVE_HEIGHT*constants.SCREEN_HEIGHT)))

  # draw the text box with the selected items

  selected_food = player.get_selected_food()
  selected_food_name = 'NONE' if selected_food == None else selected_food.NAME

  selected_bomb = player.get_selected_bomb()
  selected_bomb_name = 'NONE' if selected_bomb == None else selected_bomb.NAME

  selected_items_text = 'Selected Food: %s\nSelected Bomb: %s' % (
    selected_food_name, selected_bomb_name);
  selected_items_box = gui.TextBox(
    int(SELECTED_ITEMS_BOX_RELATIVE_X*constants.SCREEN_WIDTH),
    int(SELECTED_ITEMS_BOX_RELATIVE_Y*constants.SCREEN_HEIGHT),
    int(SELECTED_ITEMS_BOX_RELATIVE_WIDTH*constants.SCREEN_WIDTH),
    int(SELECTED_ITEMS_BOX_RELATIVE_HEIGHT*constants.SCREEN_HEIGHT),
    selected_items_text)
  selected_items_box.draw(info_surface)

  return info_surface


def test_for_monster_collision(player, monsters_in_maze):
  collision_happened = False
  for monster in monsters_in_maze.get_monsters_at(player.x, player.y):
    player.handle_monster_collision(monster)
    collision_happened = True
  return collision_happened


def pause(milliseconds): # pause time is approximate
  start_ticks = pygame.time.get_ticks()
  while True:
    pygame.time.wait(20)
    if pygame.time.get_ticks() - start_ticks >= milliseconds:
      return
    pygame.event.pump()


class Constants: # constants change with change in level or screen size
  def __init__(self, level, screen):
    self.MONSTER_BUFFER_SIZE = MONSTER_BUFFER_SIZE
    self.WALL_COLOR = WALL_COLOR
    self.MAX_WEAPON_CHARGE = MAX_WEAPON_CHARGE
    self.level_changed(level, screen) # calculate level and screen constants

  def level_changed(self, level, screen):
    self.LEVEL = level
    self.MAZE_WIDTH = BASE_MAZE_WIDTH + MAZE_LEVEL_INCREASE*level
    self.MAZE_HEIGHT = BASE_MAZE_HEIGHT + MAZE_LEVEL_INCREASE*level
    self.NUMBER_OF_MONSTERS = round(MONSTER_DENSITY * self.MAZE_WIDTH * self.MAZE_HEIGHT)
    self.NUMBER_OF_CHESTS = round(CHEST_DENSITY * self.MAZE_WIDTH * self.MAZE_HEIGHT)
    self.screen_changed(screen) # recalculate screen constants

  def screen_changed(self, screen):
    (self.SCREEN_WIDTH, self.SCREEN_HEIGHT) = screen.get_size()
    self.CELL_WIDTH = self.SCREEN_WIDTH//self.MAZE_WIDTH # pixels per cell
    self.CELL_HEIGHT = self.SCREEN_HEIGHT//self.MAZE_HEIGHT
    cell_average = (self.CELL_WIDTH + self.CELL_WIDTH)//2
    self.WALL_WIDTH = cell_average//WALL_WIDTH_DIVISOR
    if self.WALL_WIDTH < 1: self.WALL_WIDTH = 1


def run_level(constants, screen, player, mazes, maze_objects):

  # get the maze or instantiate a random maze

  maze = mazes.get(constants.LEVEL, None)
  if maze == None:
    maze = third_party.maze.Maze(width = constants.MAZE_WIDTH, height = constants.MAZE_HEIGHT)
    mazes[constants.LEVEL] = maze

  objects_in_maze = maze_objects.get(constants.LEVEL, None)
  if objects_in_maze == None:
    # populate with chests (other objects coming soon!)
    objects_in_maze = chest.ChestsInMaze(constants)
    maze_objects[constants.LEVEL] = objects_in_maze

  # populate with monsters
  monsters_in_maze = monsters.MonstersInMaze(constants, player.x, player.y)

  # build static surfaces
  background_surface = build_background_surface(constants)
  maze_surface = build_maze_surface(maze, constants)
  objects_surface = build_objects_surface(objects_in_maze, constants)

  # start a clock tick event (updates clock tick if already set)
  pygame.time.set_timer(CLOCK_TICK_EVENT, CLOCK_TICK_MS)

  # keep track of any bomb in the maze
  bomb = None

  # keep track of whether or not the player's weapon is firing
  weapon_is_firing = False

  # clear any old events before starting loop
  pygame.event.clear()

  # keep track of whether or not the player has moved yet
  player_has_moved = False

  while True:
    # build dynamic surfaces
    sprite_surface = build_sprite_surface(
      constants, monsters_in_maze, weapons, weapon_is_firing, player, bomb, maze)
    lantern_surface = build_lantern_surface(constants, player)
    info_surface = build_info_surface(constants, player, bomb)

    # blit the surfaces to the screen
    screen.blit(background_surface, (0, 0))
    screen.blit(maze_surface, (0, 0))
    screen.blit(objects_surface, (0, 0))
    screen.blit(sprite_surface, (0, 0))
    screen.blit(lantern_surface, (0, 0))
    screen.blit(info_surface, (0, 0))
    pygame.display.update()

    # test for player death
    if player.health <= 0:
      draw_centered_message(screen, "Game Over")
      sounds.stop_all_sounds()
      pause(5000)
      return None # no next level

    # wait for an event
    event = pygame.event.wait()

    # handle clock ticks
    if event.type == CLOCK_TICK_EVENT:
      # count down any bomb
      if bomb != None:
        if bomb.time_remaining > 0:
          sounds.BOMB_COUNTDOWN_SOUND.play()
          bomb.time_remaining = bomb.time_remaining - 1
        elif bomb.exploded:
          apply_bomb_damage(bomb, player, monsters_in_maze, maze, constants)
          maze_surface = build_maze_surface(maze, constants)
          bomb = None # remove exploded bomb

      # recharge weapon
      if player.weapon.charge < MAX_WEAPON_CHARGE:
        player.weapon.charge = player.weapon.charge + 1

      # determine weapon hit squares
      weapon_hit_squares = []
      if weapon_is_firing:
        if player.facing == 0: # north
          for y in range(player.weapon.BEAM_LENGTH + 1):
            weapon_hit_squares.append((player.x, player.y - y))
            if maze.get_walls(player.x, player.y - y)[0]:
              break # don't shoot through walls
        elif player.facing == 1: # east
          for x in range(player.weapon.BEAM_LENGTH + 1):
            weapon_hit_squares.append((player.x + x, player.y))
            if maze.get_walls(player.x + x, player.y)[1]:
              break # don't shoot through walls
        elif player.facing == 2: # south
          for y in range(player.weapon.BEAM_LENGTH + 1):
            weapon_hit_squares.append((player.x, player.y + y))
            if maze.get_walls(player.x, player.y + y)[2]:
              break # don't shoot through walls
        else: # west
          for x in range(player.weapon.BEAM_LENGTH + 1):
            weapon_hit_squares.append((player.x - x, player.y))
            if maze.get_walls(player.x - x, player.y)[3]:
              break # don't shoot through walls

      # send tick to all monsters
      monsters_in_maze.tick(maze, player, weapon_hit_squares)

    # handle arrow keys
    elif event.type == pygame.KEYUP and (event.key == pygame.K_UP or event.key == pygame.K_RIGHT
      or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT):

      if event.key == pygame.K_UP:
        player.facing = 0
        if not maze.get_walls(player.x, player.y)[0]:
          player.y = player.y - 1
          if test_for_monster_collision(player, monsters_in_maze):
            player.y = player.y + 1 # don't go through monster
      elif event.key == pygame.K_RIGHT:
        player.facing = 1
        if not maze.get_walls(player.x, player.y)[1]:
          player.x = player.x + 1
          if test_for_monster_collision(player, monsters_in_maze):
            player.x = player.x - 1 # don't go through monster
      elif event.key == pygame.K_DOWN:
        player.facing = 2
        if not maze.get_walls(player.x, player.y)[2]:
          player.y = player.y + 1
          if test_for_monster_collision(player, monsters_in_maze):
            player.y = player.y - 1 # don't go through monster
      elif event.key == pygame.K_LEFT:
        player.facing = 3
        if not maze.get_walls(player.x, player.y)[3]:
          player.x = player.x - 1
          if test_for_monster_collision(player, monsters_in_maze):
            player.x = player.x + 1 # don't go through monster

      player_has_moved = True # (really tracks if player has attempted to move)

    # handle ascend and descend keys

    elif event.type == pygame.KEYUP and event.key == pygame.K_d:
      # must be on stairs down
      if player.x == constants.MAZE_WIDTH - 1 and player.y == constants.MAZE_HEIGHT - 1:
        next_level = (constants.LEVEL + 1)
        draw_centered_message(screen, "Going to Level %s" % next_level)
        sounds.stop_all_sounds()
        pause(2000)
        return next_level

    elif event.type == pygame.KEYUP and event.key == pygame.K_u:
      # must be on stairs up
      if player.x == 0 and player.y == 0:
        next_level = (constants.LEVEL - 1)
        if next_level > 0:
          draw_centered_message(screen, "Going to Level %s" % next_level)
          sounds.stop_all_sounds()
          pause(2000)
          return next_level

    # handle test key
    elif event.type == pygame.KEYUP and event.key == pygame.K_F12:
      tests.run_tests(constants)
      # easter egg
      player.health = player.MAX_HEALTH
      player.weapon = weapons.SuperMegaCannon(constants)

    # handle store key (temporary code)
    elif event.type == pygame.KEYUP and event.key == pygame.K_F11:
      # allow the store to seize complete control of the game
      weapon_is_firing = False
      sounds.stop_all_sounds()
      store = store_module.Store(constants)
      store.seize()

    # handle inventory key
    elif event.type == pygame.KEYUP and event.key == pygame.K_i:
      # allow the inventory screen to seize complete control of the game
      weapon_is_firing = False
      sounds.stop_all_sounds()
      inventory.Inventory(player).seize()

    # handle pause key
    elif event.type == pygame.KEYUP and event.key == pygame.K_p:
      draw_centered_message(screen, "Paused")
      while True:
        event = pygame.event.wait()
        if event.type == pygame.KEYUP and event.key == pygame.K_p:
          break # unpause

    # handle bomb placement key
    elif event.type == pygame.KEYUP and event.key == pygame.K_b and bomb == None:
      bomb = bombs.Dynamite(constants, player.x, player.y)
    elif event.type == pygame.KEYUP and event.key == pygame.K_a and bomb == None:
      bomb = bombs.AtomBomb(constants, player.x, player.y)

    # handle weapons events
    elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
      if player.weapon.charge > 1: # only allow use when weapon has some charge
        weapon_is_firing = True
        sounds.FIRE_SOUND.play(-1)
        pygame.time.set_timer(WEAPON_TICK_EVENT, WEAPON_TICK_MS)
    elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
      weapon_is_firing = False
      sounds.FIRE_SOUND.stop()
    elif event.type == WEAPON_TICK_EVENT:
      if weapon_is_firing:
        # discharge
        if player.weapon.charge > 0:
          player.weapon.charge = player.weapon.charge - 1
        else:
          weapon_is_firing = False
          sounds.FIRE_SOUND.stop()
      else:
        # stop the weapon tick event if firing has stopped
        pygame.time.set_timer(WEAPON_TICK_EVENT, 0)

    # handle resize events
    elif event.type == pygame.VIDEORESIZE:
      # reset the screen
      screen = pygame.display.set_mode(event.dict['size'], pygame.RESIZABLE)

      # rebind screen parameters
      constants.screen_changed(screen)

      # rebuild static surfaces
      background_surface = build_background_surface(constants)
      maze_surface = build_maze_surface(maze, constants)
      objects_surface = build_objects_surface(objects_in_maze, constants)

    # handle quit events
    elif event.type == pygame.QUIT or (
      event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
        return None # no next level


def exit_program():
  pygame.quit()
  sys.exit()


def main():
  # check the Python version so that We don't end up with strange behavior
  version = sys.version_info
  assert(version[0] == PYTHON_MAJOR_VERSION)

  # run the main function
  # set initial window position
  os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (INITIAL_WINDOW_X, INITIAL_WINDOW_Y)

  # pygame initialization
  sounds.pre_init()
  pygame.init()
  sounds.init()
  images.init()

  # set up initial display
  info = pygame.display.Info()
  smallest_dim = min(info.current_w, info.current_h)
  win_size = round(INITIAL_WINDOW_SIZE*smallest_dim)
  screen = pygame.display.set_mode((win_size, win_size), pygame.RESIZABLE)
  pygame.display.set_caption("Uncle Bernard's Basement")

  # instantiate constants container
  level = 1
  constants = Constants(level, screen)

  # instantiate player & set initial weapon
  player = player_module.Player(constants)
  player.weapon = weapons.MiniBlaster(constants)

  # instantiate a dictionary of mazes and their objects
  mazes = {}
  maze_objects = {}

  # loop through levels
  while True:
    next_level = run_level(constants, screen, player, mazes, maze_objects)
    sounds.stop_all_sounds()
    if next_level == None: # end of game
      break
    constants.level_changed(next_level, screen)
    if next_level > level: # down
      player.x = 0
      player.y = 0
      player.facing = 2 # south
    else: # up
      player.x = constants.MAZE_WIDTH - 1
      player.y = constants.MAZE_HEIGHT - 1
      player.facing = 0 # north
    level = next_level

  exit_program()


if __name__ == '__main__':
  main()
