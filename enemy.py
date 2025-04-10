import pygame
import random

class Enemy:
  def __init__(self, screen_width, screen_height, border, vel, diameter, type):
    self.vel = vel
    self.diameter = diameter

    if type == "qix":
      # for qix, start at top right corner
      self.pos = 
    else:
      # for sparx, start at top middle
      self.pos = 
      self.direction = random.choice(["left", "right"])
      self.at_vertical_border = False
      self.at_horizontal_border = True

  #### QIX FUNCTIONS

  # check for collision by using Rect.collide
  def qix_collide():
  """Checks for collision with player."""

  #### SPARX FUNCTIONS

  # check for collision by checking if touching marker's unique color?
  def sparx_collide(): 

  # check for collision by checking if reaches starting_point coordinate, changes direction
  def push_collide(starting_point): 
    if self.pos == starting_point:

  def change_direction():
    if 
