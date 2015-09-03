# thanks http://forums.tigsource.com/index.php?topic=4589.0

import pygame, random
from pygame.locals import *

class Maze:
 def __init__(self, mazeLayer = None, solveLayer = None,
              width = 80, height = 60):
  self.mazeArray = []
  self.state = 'c'  # c = creating, s = solving, r = reset
  self.mLayer = mazeLayer # surface
  self.sLayer = solveLayer# surface
  self.width = width
  self.height = height

  if self.mLayer and self.sLayer:
   self.mLayer.fill((0, 0, 0, 0))
   self.sLayer.fill((0, 0, 0, 0))

  for y in range(height):
   if self.mLayer and self.sLayer:
    pygame.draw.line(self.mLayer, (0,0,0,255), (0, y*8), (640, y*8))
   for x in range(width):
    self.mazeArray.append(0x0)
    if self.mLayer and self.sLayer and y == 0:
     pygame.draw.line(self.mLayer, (0,0,0,255), (x*8,0), (x*8,480))

  if self.mLayer and self.sLayer:
   pygame.draw.rect(self.sLayer, (0,0,255,255), Rect(0,0,8,8))
   pygame.draw.rect(self.sLayer, (255,0,255,255), Rect((632),(472),8,8))

  # Maze Section
  self.totalCells = height*width
  self.wallList = []
  self.currentCell = random.randint(0, self.totalCells-1)
  c = self.currentCell
  mz = self.mazeArray[c]
  self.mazeArray[c] |= 0x00F0 # now its part of the maze
  self.wallList.append((c,0))
  self.wallList.append((c,1))
  self.wallList.append((c,2))
  self.wallList.append((c,3)) # fill the walls
  self.visitedCells = 1
  self.cellStack = []
  self.compass = [(-1,0),(0,1),(1,0),(0,-1)]

  # finish generating maze here rather than in update calls -- JVO
  while self.state == 'c':
      self.update()

 def update(self):
  if self.state == 'c':
   #if self.visitedCells >= self.totalCells:
   if len(self.wallList) <= 0:
    self.currentCell = 0 # set current to top-left
    self.cellStack = []
    self.state = 's'
    #print ('Maze generation complete...')
    #print (self.mazeArray)
    #print ('Maze Array Length: %s' % len(self.mazeArray))
    return

   moved = False

   while(len(self.wallList) > 0):# and moved == False):
    # pick a random wall
    wi = random.randint(0, len(self.wallList)-1)
    self.currentCell = self.wallList[wi][0]
    x = self.currentCell % self.width
    y = self.currentCell // self.width
    dir = self.wallList[wi][1]
    nx = x + self.compass[dir][0]
    ny = y + self.compass[dir][1]
    nidx = ny*self.width + nx
    dx = x*8
    dy = y*8
    direction = 1 << dir # make it perty

    if ((nx >= 0) and (ny >= 0) and (nx < self.width) and (ny < self.height)):
     if (self.mazeArray[nidx] & 0x00F0) == 0:
      if direction & 1:
       self.mazeArray[nidx] |= (4)
       if self.mLayer and self.sLayer:
        pygame.draw.line(self.mLayer, (0,0,0,0), (dx,dy+1),(dx,dy+7))
      elif direction & 2:
       self.mazeArray[nidx] |= (8)
       if self.mLayer and self.sLayer:
        pygame.draw.line(self.mLayer, (0,0,0,0), (dx+1,dy+8),(dx+7,dy+8))
      elif direction & 4:
       self.mazeArray[nidx] |= (1)
       if self.mLayer and self.sLayer:
        pygame.draw.line(self.mLayer, (0,0,0,0), (dx+8,dy+1),(dx+8,dy+7))
      elif direction & 8:
       self.mazeArray[nidx] |= (2)
       if self.mLayer and self.sLayer:
        pygame.draw.line(self.mLayer, (0,0,0,0), (dx+1,dy),(dx+7,dy))
      self.mazeArray[self.currentCell] |= direction
      self.mazeArray[(ny*self.width + nx)] |= 0x00F0 # mark as part of the maze

      # add its walls to the list
      self.wallList.append((ny*self.width + nx,0))
      self.wallList.append((ny*self.width + nx,1))
      self.wallList.append((ny*self.width + nx,2))
      self.wallList.append((ny*self.width + nx,3))
      moved = True
    self.wallList.remove(self.wallList[wi])

##  elif self.state == 's':
##   return # solving phase disabled -- JVO
##   if self.currentCell == (self.totalCells-1): # have we reached the exit?
##    self.state = 'r'
##    return
##   moved = False
##   while(moved == False):
##    x = self.currentCell % 80
##    y = self.currentCell // 80
##    neighbors = []
##    directions = self.mazeArray[self.currentCell] & 0xF
##    for i in range(4):
##     if (directions & (1<<i)) > 0:
##      nx = x + self.compass[i][0]
##      ny = y + self.compass[i][1]
##      if ((nx >= 0) and (ny >= 0) and (nx < 80) and (ny < 60)):
##       nidx = ny*80+nx
##       if ((self.mazeArray[nidx] & 0xFF00) == 0): # make sure there's no backtrack
##        neighbors.append((nidx,1<<i))
##    if len(neighbors) > 0:
##     idx = random.randint(0,len(neighbors)-1)
##     nidx,direction = neighbors[idx]
##     dx = x*8
##     dy = y*8
##     if direction & 1:
##      self.mazeArray[nidx] |= (4 << 12)
##     elif direction & 2:
##      self.mazeArray[nidx] |= (8 << 12)
##     elif direction & 4:
##      self.mazeArray[nidx] |= (1 << 12)
##     elif direction & 8:
##      self.mazeArray[nidx] |= (2 << 12)
##     pygame.draw.rect(self.sLayer, (0,255,0,255), Rect(dx,dy,8,8))
##     self.mazeArray[self.currentCell] |= direction << 8
##     self.cellStack.append(self.currentCell)
##     self.currentCell = nidx
##     moved = True
##    else:
##     pygame.draw.rect(self.sLayer, (255,0,0,255), Rect((x*8),(y*8),8,8))
##     self.mazeArray[self.currentCell] &= 0xF0FF # not a solution
##     self.currentCell = self.cellStack.pop()
##  elif self.state == 'r':
##   self.__init__(self.mLayer,self.sLayer)

 def get_walls(self, x, y):
  'returns a tuple of bools for (north, east, south, west)'
  cell = ~self.mazeArray[y*self.width + x]
  north = bool(cell & 0b00001000)
  east  = bool(cell & 0b00000100)
  south = bool(cell & 0b00000010)
  west  = bool(cell & 0b00000001)
  return (north, east, south, west)

 def set_walls(self, x, y, walls):
  present = 0b11110000;

  # set present cell and adjacent cells

  i = (y - 1)*self.width + x # north of this cell
  if walls[0]:
    present = present | 0b00001000
    if i >= 0 and i < len(self.mazeArray):
      self.mazeArray[i] = self.mazeArray[i] & 0b11111101
  elif i >= 0 and i < len(self.mazeArray):
    self.mazeArray[i] = self.mazeArray[i] | 0b00000010

  i = y*self.width + x + 1 # east of this cell
  if walls[1]:
    present = present | 0b00000100
    if i >= 0 and i < len(self.mazeArray):
      self.mazeArray[i] = self.mazeArray[i] & 0b11111110
  elif i >= 0 and i < len(self.mazeArray):
    self.mazeArray[i] = self.mazeArray[i] | 0b00000001

  i = (y + 1)*self.width + x # south of this cell
  if walls[2]:
    present = present | 0b00000010
    if i >= 0 and i < len(self.mazeArray):
      self.mazeArray[i] = self.mazeArray[i] & 0b11110111
  elif i >= 0 and i < len(self.mazeArray):
    self.mazeArray[i] = self.mazeArray[i] | 0b00001000

  i = y*self.width + x - 1 # west of this cell
  if walls[3]:
    present = present | 0b00000001
    if i >= 0 and i < len(self.mazeArray):
      self.mazeArray[i] = self.mazeArray[i] & 0b11111011
  elif i >= 0 and i < len(self.mazeArray):
    self.mazeArray[i] = self.mazeArray[i] | 0b00000100

  # preserve border walls
  if y == 0: present = present | 0b00001000
  if x == self.width - 1: present = present | 0b00000100
  if y == self.height - 1: present = present | 0b00000010
  if x == 0: present = present | 0b00000001

  self.mazeArray[y*self.width + x] = ~present

 def get_size(self):
  'returns (width, height)'
  return (self.width, self.height)

 def draw(self, screen):
  screen.blit(self.sLayer, (0,0))
  screen.blit(self.mLayer, (0,0))

def main():
 """Maze Main Function - Luke Arntson, Jan '09
  Written using - http://www.mazeworks.com/mazegen/mazetut/index.htm
 """
 pygame.init()
 screen = pygame.display.set_mode((640, 480))
 pygame.display.set_caption('Labyrinth')
 pygame.mouse.set_visible(0)
 background = pygame.Surface(screen.get_size())
 background = background.convert()
 background.fill((255, 255, 255))
 mazeLayer = pygame.Surface(screen.get_size())
 mazeLayer = mazeLayer.convert_alpha()
 mazeLayer.fill((0, 0, 0, 0))
 solveLayer = pygame.Surface(screen.get_size())
 solveLayer = solveLayer.convert_alpha()
 solveLayer.fill((0, 0, 0, 0))
 newMaze = Maze(mazeLayer, solveLayer, 40, 40)
 screen.blit(background, (0, 0))
 pygame.display.flip()
 clock = pygame.time.Clock()
 global gmaze # JVO for debugging and development
 gmaze = newMaze
 while 1:
  clock.tick(60)
  for event in pygame.event.get():
   if event.type == QUIT:
    pygame.quit()
    return
   elif event.type == KEYDOWN and event.key == K_ESCAPE:
    pygame.quit()
    return
  newMaze.update()
  screen.blit(background, (0, 0))
  newMaze.draw(screen)
  pygame.display.flip()

if __name__ == '__main__':
  main()
