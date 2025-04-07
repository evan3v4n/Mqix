import pygame

class Marker:
    def __init__(self, screen_width, screen_height, initial_margin, vel=1, marker_diameter=10):
        self.vel = vel
        self.diameter = marker_diameter
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.initial_margin = initial_margin

        # Start at bottom center
        self.pos = pygame.Vector2(screen_width / 2, screen_height - initial_margin)
        self.push = False


    def move(self, keys, screen):
        x = int(self.pos.x)
        y = int(self.pos.y)
        border_color = pygame.Color('black')

        if keys[pygame.K_LEFT] and self.pos.x > self.initial_margin and screen.get_at((x - self.vel, y)) == border_color:
            self.pos.x -= self.vel
        if keys[pygame.K_RIGHT] and self.pos.x < self.screen_width - self.initial_margin and screen.get_at((x + self.vel, y)) == border_color:
            self.pos.x += self.vel
        if keys[pygame.K_UP] and self.pos.y > self.initial_margin and screen.get_at((x, y - self.vel)) == border_color:
            self.pos.y -= self.vel
        if keys[pygame.K_DOWN] and self.pos.y < self.screen_height - self.initial_margin and screen.get_at((x, y + self.vel)) == border_color:
            self.pos.y += self.vel

        
    def draw(self, window):
        """Draw the marker."""
        pygame.draw.circle(window, 'green', self.pos, self.diameter)
