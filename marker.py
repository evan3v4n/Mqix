import pygame

class Marker:
    def __init__(self, screen_width, screen_height, initial_margin, vel=8, marker_diameter=10):
        self.vel = vel
        self.diameter = marker_diameter
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.initial_margin = initial_margin
        self.push_points = []  # List to track vertices during push

        # Start at bottom center
        self.pos = pygame.Vector2(screen_width / 2, screen_height - (initial_margin / 2))
        self.pushed = False

    def move(self, keys):
        """Move the marker based on pixel colors around it."""
        # Get current position
        x, y = int(self.pos.x), int(self.pos.y)
        
        # Get the surface to check pixel colors
        surface = pygame.display.get_surface()
        
        # Initialize movement flags
        can_move_left = True
        can_move_right = True
        can_move_up = False
        can_move_down = False

        # Check pixels in each direction, but only if within window bounds
        if 0 <= x - self.vel < self.screen_width and 0 <= y < self.screen_height:
            can_move_left = surface.get_at((x - self.vel, y))[0:3] != (0, 0, 0)
        
        if 0 <= x + self.vel < self.screen_width and 0 <= y < self.screen_height:
            can_move_right = surface.get_at((x + self.vel, y))[0:3] != (0, 0, 0)
        
        if 0 <= x < self.screen_width and 0 <= y - self.vel < self.screen_height:
            can_move_up = surface.get_at((x, y - self.vel))[0:3] != (0, 0, 0)
        
        if 0 <= x < self.screen_width and 0 <= y + self.vel < self.screen_height:
            can_move_down = surface.get_at((x, y + self.vel))[0:3] != (0, 0, 0)

        # Move based on key presses and available directions
        if keys[pygame.K_LEFT] and can_move_left:
            self.pos.x -= self.vel
        elif keys[pygame.K_RIGHT] and can_move_right:
            self.pos.x += self.vel
        elif keys[pygame.K_UP] and can_move_up:
            self.pos.y -= self.vel
        elif keys[pygame.K_DOWN] and can_move_down:
            self.pos.y += self.vel

        # Check if marker has moved outside the initial border
        if (self.pos.x < self.initial_margin or 
            self.pos.x > self.screen_width - self.initial_margin or
            self.pos.y < self.initial_margin or 
            self.pos.y > self.screen_height - self.initial_margin):
            self.push(None)  # Start push mode
        
        # If in push mode, add current position to push points
        if self.pushed:
            self.push_points.append(pygame.Vector2(self.pos))

    def push(self, border):
        """Initiates push mode when marker moves outside initial border."""
        if not self.pushed:
            self.push_points = [pygame.Vector2(self.pos)]
            self.pushed = True

    def claim_territory(self, border):
        """Claims territory if marker returns to original border."""
        if self.pushed and len(self.push_points) > 2:
            # Check if marker returned to original border
            # If true, update border using vertices in push_points
            self.pushed = False
            self.push_points = []

        
    def draw(self, window):
        """Draw the marker and push line if in push mode."""
        pygame.draw.circle(window, 'green', self.pos, self.marker_diameter)
        if self.pushed and len(self.push_points) > 1:
            pygame.draw.lines(window, 'red', False, self.push_points)
