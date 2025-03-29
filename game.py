import pygame
from marker import Marker 

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

#create a marker instance
marker = Marker(screen_width, screen_height, border)

while running:
    pygame.time.delay(100)
    window.fill(bg_color)
    pygame.draw.rect(window, 'black', border_rect, 3)
    for event in pygame.event.get():
        #closing the window when the close button is clicked
        if event.type == pygame.QUIT:
            running = False

    key = pygame.key.get_pressed()
    marker.move(key)
    marker.modify_direction(key)
    marker.draw(window)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()