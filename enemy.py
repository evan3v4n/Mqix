import pygame
import random

class Enemy:
  def __init__(self, screen_width, screen_height, initial_margin, vel=6, diameter=10, type):
    self.vel = vel
    self.diameter = diameter
    self.screen_width = screen_width
    self.screen_height = screen_height 
    self.initial_margin = initial_margin
    self.type = type
    self.pos = [0,0]
    
    self.moving_left = False
    self.moving_right = False
    self.moving_up = False
    self.moving_down = False

    if type == "qix":
      # for qix, start at top right corner
      self.pos = [screen_width - initial_margin - diameter, initial_margin + diameter]
      self.change_direction() # Random initial direction
    else:
      # for sparx, start at top middle
      self.pos =  [screen_width // 2, initial_margin + diameter] 
      self.direction = random.choice(["left", "right"])
      self.at_vertical_initial_margin = False
      self.at_horizontal_initial_margin = True
      self.moving_left = self.direction == "left"
      self.moving_right = self.direction == "right"
    # initialize collision rect 
    self.rect = pygame.Rect(self.pos[0], self.pos[1], diameter, diameter)
  
  def move(self):
  """Moves enemy in current direction by one pixel."""
        if self.moving_left:
            self.pos[0] -= self.vel
        if self.moving_right:
            self.pos[0] += self.vel
        if self.moving_up:
            self.pos[1] -= self.vel
        if self.moving_down:
            self.pos[1] += self.vel
        # Update the rect position based on the new position
        self.rect.topleft = (self.pos[0], self.pos[1])

  #### QIX FUNCTIONS

  def qix_collide(self, player_rect):
    """Checks for Qix collision with player."""
    if self.rect.colliderect(player_rect):
      self.change_direction()
      return True
    return False

  #### SPARX FUNCTIONS

  def sparx_collide(self, player_rect): 
    """Checks for Sparx collision with player."""
    # changes direction if collides with player
    if self.rect.colliderect(player_rect):
      self.change_direction()
      return True
    return False
  
  def push_collide(self, starting_point): 
    """Checks for Sparx collision with push starting point."""
    #create a rect for the starting point
    start_rect = pygame.Rect(
            int(starting_point.x - 2),
            int(starting_point.y - 2),
            4, 4
        )
    #checks if the enemy is touching the starting point
    if self.rect.colliderect(start_rect):
          self.change_direction()
          return True
    return False
    
    
  def change_direction(self):
    """Changes enemy's movements depending on their type."""
    if self.type == "qix":
      # change direction randomly
      self.moving_left = random.choice([True, False])
      self.moving_right = not self.moving_left
      self.moving_up = random.choice([True, False])
      self.moving_down = not self.moving_up
    else:
      # change direction based on current direction
      if self.direction == "left":
        self.moving_left = False
        self.moving_right = True
        self.direction == "right"
      elif self.direction == "right":
        self.moving_left = True
        self.moving_right = False
        self.direction = "left"
      elif self.direction == "up":
        self.moving_up = False
        self.moving_down = True
        self.direction = "down"
      elif self.direction == "down":
        self.moving_up = True
        self.moving_down = False
        self.direction = "up"
      
  def draw(self, screen):
    """Draws enemy icon on screen."""
    if self.type == "qix":
      pygame.draw.circle(screen, (255, 0, 0), (self.pos[0], self.pos[1]), self.diameter)
    else:
      pygame.draw.circle(screen, (0, 255, 0), (self.pos[0], self.pos[1]), self.diameter) 