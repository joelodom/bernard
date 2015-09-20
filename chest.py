import random
import images

class Chest:
  def __init__(self, constants):
    self.constants = constants

    #defaults
    self.get_tier()
    self.get_image()

    # set location randomly
    self.x = random.randint(0, self.constants.MAZE_WIDTH - 1)
    self.y = random.randint(0, self.constants.MAZE_HEIGHT - 1)

    

  def get_tier(self):
    self.TIER = random.choice(['1', '1', '1', '1', '1', '1l', '1l'])

  def get_image(self):
    if self.TIER == '1':
      self.IMAGE = images.TIER_1_CHEST
    elif self.TIER == '1l':
      self.IMAGE = images.TIER_1_LOCKED_CHEST

class ChestsInMaze:
  def __init__(self, constants):
    self.constants = constants

    # populate the maze with random chest
    self.chests = []
    while len(self.chests) < self.constants.NUMBER_OF_CHESTS:
      self.chests.append(Chest(constants))
      
      

  def draw(self, surface):
    cell_width = self.constants.SCREEN_WIDTH//self.constants.MAZE_WIDTH
    cell_height = self.constants.SCREEN_HEIGHT//self.constants.MAZE_HEIGHT
    
    for chest in self.chests:
      images.draw_image_in_cell(self.constants, surface, chest.IMAGE, chest.x, chest.y)

      
    
      
  
