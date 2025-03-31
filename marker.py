import pygame

class Marker:
    def __init__(self, screen_width, screen_height, border, vel=8, marker_diameter=10):
        self.vel = vel
        self.marker_diameter = marker_diameter
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.border = border

        # Start at bottom center
        self.pos = pygame.Vector2(screen_width / 2, screen_height - (border / 2))
        self.direction = "horizontal"
        self.can_change_direction = False
        self.at_horizontal_border = True
        self.at_vertical_border = False

    def update_border_status(self):
        """Recalculate if the marker is at a horizontal or vertical border."""
        self.at_horizontal_border = self.pos.x <= self.border or self.pos.x >= self.screen_width - self.border
        self.at_vertical_border = self.pos.y <= self.border or self.pos.y >= self.screen_height - self.border

    def modify_direction(self, keys):
        """Allow direction change only at corners."""
        if (self.at_horizontal_border and self.at_vertical_border) :
            self.can_change_direction = True

        if self.can_change_direction:
            if keys[pygame.K_UP] or keys[pygame.K_DOWN]:
                self.direction = "vertical"
            elif keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
                self.direction = "horizontal"
            self.can_change_direction = False  # Reset after switching

    def move(self, keys):
        """Move the marker based on direction."""
        if self.direction == "horizontal":
            if keys[pygame.K_LEFT] and self.pos.x > self.border:
                self.pos.x -= self.vel
            elif keys[pygame.K_RIGHT] and self.pos.x < self.screen_width - self.border:
                self.pos.x += self.vel
        elif self.direction == "vertical":
            if keys[pygame.K_UP] and self.pos.y > self.border:
                self.pos.y -= self.vel
            elif keys[pygame.K_DOWN] and self.pos.y < self.screen_height - self.border:
                self.pos.y += self.vel
        self.update_border_status() 

    def draw(self, window):
        """Draw the marker."""
        self.push()
        pygame.draw.circle(window, 'green', self.pos, self.marker_diameter)
