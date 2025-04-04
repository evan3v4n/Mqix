import pygame

class Enemy:
  def __init__(self, screen_width, screen_height, border, vel, diameter):
    self.vel = vel
    self.diameter = diameter

    # start at top left corner
    
