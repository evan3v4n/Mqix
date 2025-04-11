import pygame

class Marker:
    def __init__(self, screen_width, screen_height, initial_margin, vel=8, marker_diameter=10, board=None):
        self.vel = vel
        self.diameter = marker_diameter
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.initial_margin = initial_margin
        self.push_points = []  # List to track vertices during push
        self.lives = 3  # Number of lives for the marker
        # Start at bottom center
        self.pos = pygame.Vector2( self.screen_width//2, screen_height - self.initial_margin - 1)
        self.pushed = False 
        self.turn_points = []  # List to track turn points during push
        self.board = board  # Reference to the border object
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False


    def move(self, keys):
        """Move the marker based on pixel colors around it."""
        # Get current position
        x, y = int(self.pos.x), int(self.pos.y)
        
        # Get the surface to check pixel colors
        surface = pygame.display.get_surface()
        
        # Initialize movement flags
        can_move_left = True
        can_move_right = False
        can_move_up = False
        can_move_down = False

        

                # If in push mode, add current position to push points
        if self.pushed:
            can_move_down = True
            can_move_up = True
            can_move_left = True
            can_move_right = True

            #pushing marker inside the border

            #between the side of the border
            if x == self.initial_margin and self.initial_margin < y < self.screen_height - self.initial_margin:
                self.pos.x = self.initial_margin + 1
                self.moving_left = True
                self.moving_right = self.moving_up = self.moving_down = False
            elif x == self.screen_width - self.initial_margin -1 and self.initial_margin < y < self.screen_height - self.initial_margin: 
                self.pos.x = self.screen_width - self.initial_margin - 2
                self.moving_right = True
                self.moving_left = self.moving_up = self.moving_down = False
            elif y == self.initial_margin and self.initial_margin < x < self.screen_width - self.initial_margin:
                self.pos.y = self.initial_margin + 1
                self.moving_down = True
                self.moving_up = self.moving_left = self.moving_right = False
            elif y == self.screen_height - self.initial_margin -1 and self.initial_margin < x < self.screen_width - self.initial_margin:
                self.pos.y = self.screen_height - self.initial_margin - 2
                self.moving_up = True
                self.moving_down = self.moving_left = self.moving_right = False
            #corners of the border
            elif x == self.initial_margin and y == self.initial_margin:
                self.pos.x = self.initial_margin + 1
                self.pos.y = self.initial_margin + 1
            elif x == self.screen_width - self.initial_margin -1 and y == self.initial_margin:
                self.pos.x = self.screen_width - self.initial_margin - 2
                self.pos.y = self.initial_margin + 1
            elif x == self.initial_margin and y == self.screen_height - self.initial_margin -1:
                self.pos.x = self.initial_margin + 1
                self.pos.y = self.screen_height - self.initial_margin - 2
            elif x == self.screen_width - self.initial_margin -1 and y == self.screen_height - self.initial_margin -1:
                self.pos.x = self.screen_width - self.initial_margin - 2
                self.pos.y = self.screen_height - self.initial_margin - 2
            
        else:
            # Check pixels in each direction, but only if within window bounds
            if self.initial_margin <= x - 1 <= self.screen_width - self.initial_margin and 0 <= y < self.screen_height:
                can_move_left = (surface.get_at((x - 1,y))[0:3] == (0, 0, 0))
    
            if self.initial_margin <= x + 1 < self.screen_width - self.initial_margin and self.initial_margin <= y < self.screen_height - self.initial_margin:
                can_move_right = (surface.get_at((x + 1, y))[0:3] == (0, 0, 0))
        
            if 0 <= x < self.screen_width and self.initial_margin <= y - 1 < self.screen_height - self.initial_margin:
                can_move_up = (surface.get_at((x, y - 1))[0:3] == (0, 0, 0))
        
            if 0 <= x < self.screen_width and self.initial_margin <= y + 1 < self.screen_height:
                can_move_down = (surface.get_at((x, y + 1))[0:3] == (0, 0, 0))
            
        # Move based on key presses and available directions
        if keys[pygame.K_LEFT] and can_move_left:
            if not self.moving_left and self.pushed:
                self.turn_points.append(pygame.Vector2(self.pos))
            self.pos.x -= self.vel
            self.moving_left = True
            self.moving_right = self.moving_up = self.moving_down = False
            self.add_push_point(pygame.Vector2(self.pos))

        elif keys[pygame.K_RIGHT] and can_move_right:
            if not self.moving_right and self.pushed:
                self.turn_points.append(pygame.Vector2(self.pos))
            self.pos.x += self.vel
            self.moving_right = True
            self.moving_left = self.moving_up = self.moving_down = False
            self.add_push_point(pygame.Vector2(self.pos))
        elif keys[pygame.K_UP] and can_move_up:
            if not self.moving_up and self.pushed:
                self.turn_points.append(pygame.Vector2(self.pos))
            self.pos.y -= self.vel
            self.moving_up = True
            self.moving_down = self.moving_left = self.moving_right = False
            self.add_push_point(pygame.Vector2(self.pos))
        elif keys[pygame.K_DOWN] and can_move_down:
            if not self.moving_down and self.pushed:
                self.turn_points.append(pygame.Vector2(self.pos))
            self.pos.y += self.vel
            self.moving_down = True
            self.moving_up = self.moving_left = self.moving_right = False
            self.add_push_point(pygame.Vector2(self.pos))


        # Check if marker has moved outside the initial border
        if self.pos.x < self.initial_margin:
            self.pos.x = self.initial_margin
        elif self.pos.x > self.screen_width - self.initial_margin -1:
            self.pos.x = self.screen_width - self.initial_margin -1
        if self.pos.y < self.initial_margin:
            self.pos.y = self.initial_margin            
        elif self.pos.y > self.screen_height - self.initial_margin -1:
            self.pos.y = self.screen_height - self.initial_margin - 1

        if self.push :
            if surface.get_at((int(self.pos.x),int(self.pos.y)))[0:3] == (0, 0, 0):
                self.claim_territory(self.board)
        

    def push(self):
        """Initiates push mode when marker moves outside initial border."""
        if not self.pushed:
            # push marker inside the border
            self.turn_points.append(pygame.Vector2(self.pos))
            self.push_points = [pygame.Vector2(self.pos)]
            self.pushed = True
    
    def add_push_point(self, point):
        """Adds a point to the push points list."""
        if self.pushed:
            # Check if the point is not already in the list
            if point not in self.push_points:
                # Add the point to the push points list
                self.push_points.append(point)
                # Check if the point is not already in the 
            elif len(self.push_points) > 0 and point in self.push_points:
                self.pos = self.push_points[0]
                self.turn_points=[]
                # Reset the push points
                self.push_points = []
                self.pushed = False
                # Reduce the lives of the marker
                self.reduce_lives()
        
            

    def claim_territory(self, board):
        """Claims territory if marker returns to original border."""
        if board is not None:
            if self.pushed and len(self.push_points) > 2:
                # Check if marker returned to original border
                # If true, update border using vertices in push_points
                self.turn_points.append(pygame.Vector2(self.pos))
                #print(f"Claiming territory with points: {self.turn_points}")
                board.update_border(self.turn_points)
                self.turn_points = []
                self.pushed = False
                self.push_points = []
        if board is None:
            # If marker is not in push mode, reset the push points
            self.turn_points.append(pygame.Vector2(self.pos))
            #print(f"Claiming territory with points: {self.turn_points}")
            self.push_points = []
            self.pushed = False
            self.turn_points = []

    def reduce_lives(self):
        """Reduces lives by 1."""
        self.lives -= 1
        if self.pushed:
            self.pushed = False
            #Reset marker position to the starting point of the push
            self.pos = self.push_points[0]
            #Reset the push points
            self.push_points = []
        
        
    def draw(self, window):
        """Draw the marker and push line if in push mode."""
        pygame.draw.circle(window, 'green', self.pos, self.diameter)
        if self.pushed and len(self.push_points) > 1:
            pygame.draw.lines(window, 'red', False, self.push_points)
