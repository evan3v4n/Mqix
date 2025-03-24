import pygame

# game setup
pygame.init()
window = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Mqix')

running = True
clock = pygame.time.Clock()

# window related variables
bg_color = (252, 215, 183)
screen_width = window.get_width()
screen_height = window.get_height()
border = 20 # distance of the border from the edge of the screen
border_rect = pygame.Rect(0, 0, screen_width - border, screen_height - border)
border_rect.center = (screen_width/2, screen_height/2)

# marker related variables
marker_diameter = 10
vel = 8
marker_pos = pygame.Vector2(screen_width/ 2, screen_height - (border/2))
edge = True
pushed = False
direction = "horizontal"
can_change_direction = False

def modify_marker_direction():
    global direction, can_change_direction

    # Allow direction change when at a border (corner of the movement path)
    at_horizontal_border = marker_pos.x <= border or marker_pos.x >= screen_width - border
    at_vertical_border = marker_pos.y <= border or marker_pos.y >= screen_height - border

    if at_horizontal_border and at_vertical_border:
        can_change_direction = True

    # Change direction only if allowed
    if can_change_direction:
        if key[pygame.K_UP] or key[pygame.K_DOWN]:
            direction = "vertical"
        elif key[pygame.K_LEFT] or key[pygame.K_RIGHT]:
            direction = "horizontal"
        can_change_direction = False

while running:
    pygame.time.delay(100)
    window.fill(bg_color)
    pygame.draw.rect(window, 'black', border_rect, 3)
    for event in pygame.event.get():
        #closing the window when the close button is clicked
        if event.type == pygame.QUIT:
            running = False

    key = pygame.key.get_pressed()
    # moves marker left and right 
    if direction == "horizontal":
        if key[pygame.K_LEFT] and marker_pos.x > border:
            marker_pos.x -= vel
            can_change_direction = False  # Prevents immediate direction change
        elif key[pygame.K_RIGHT] and marker_pos.x < screen_width - border:
            marker_pos.x += vel
            can_change_direction = False

    elif direction == "vertical":
        if key[pygame.K_UP] and marker_pos.y > border:
            marker_pos.y -= vel
            can_change_direction = False
        elif key[pygame.K_DOWN] and marker_pos.y < screen_height - border:
            marker_pos.y += vel
            can_change_direction = False

    modify_marker_direction()
    
    # Draw the marker
    pygame.draw.circle(window, 'green', marker_pos, marker_diameter)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()