import pygame
from marker import Marker 
from board import Board

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
#create a board instance
board = Board(screen_width,screen_height,border,window)

while running:
    pygame.time.delay(100)
    window.fill(bg_color)
    pygame.draw.rect(window, 'black', border_rect, 3)
    for event in pygame.event.get():
        #closing the window when the close button is clicked
        if event.type == pygame.QUIT:
            running = False

    key = pygame.key.get_pressed()

    #TESTING REMOVE LATER
    if key[pygame.K_p]:
        board.update_border([(100, 100), (200, 100), (200, 200), (100, 200)])
    if key[pygame.K_o]:
        board.update_border([(50, 50), (150, 50), (150, 150), (100, 150), (100, 250), (50, 250)])
    if key[pygame.K_i]:
        board.update_border([(150, 150), (650, 150), (750, 450), (650, 650), (150, 650), (50, 450)]) 
    if board.check_if_win():
        print("DONE")
        pygame.quit()
    pygame.draw.lines(window,'black', True, [(20,200),(980,200),(980,500)],3)
    #TESTING REMOVE LATER

    board.draw(window)
    
    marker.move(key)
    marker.modify_direction(key)
    marker.draw(window)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()