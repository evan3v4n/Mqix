import pygame
from marker import Marker 
from board import Board

# game setup
pygame.init()
pygame.font.init()
window = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Mqix')

running = True
clock = pygame.time.Clock()

#font setup
font_small = pygame.font.SysFont('DroidSans', 30)
font_big = pygame.font.SysFont('DroidSans', 100)
game_over_text = font_big.render('Game Over', True, 'black')
lives_text = font_small.render('LIVES: ', True, 'black')
one_life = font_small.render('*', True, 'black')
two_lives = font_small.render('* *', True, 'black')
three_lives = font_small.render('* * *', True, 'black')

# window related variables
bg_color = (252, 215, 183)
screen_width = window.get_width()
screen_height = window.get_height()
initial_margin = 50 # distance of the border from the edge of the screen
border_rect = pygame.Rect(0,0, screen_width - (2*initial_margin), screen_height - (2*initial_margin))
border_rect.center = (screen_width/2, screen_height/2)

#create a marker instance
marker = Marker(screen_width, screen_height, initial_margin)
#create a board instance
board = Board(screen_width,screen_height,initial_margin,window)

while running:
    pygame.time.delay(100)
    window.fill(bg_color)
    window.blit(lives_text, (screen_width - 200, initial_margin//2))
    if marker.lives == 3:
        window.blit(three_lives, (screen_width - 100, initial_margin//2))
    elif marker.lives == 2:
        window.blit(two_lives, (screen_width - 100, initial_margin//2))
    elif marker.lives == 1:
        window.blit(one_life, (screen_width - 100, initial_margin//2))
    pygame.draw.rect(window, 'black', border_rect,1)
    
    #print(f"marker pos: {marker.pos.x}, {marker.pos.y}")
    #print(f"colour at marker right: {window.get_at(( int(marker.pos.x + 1) , int(marker.pos.y)))}")
    #print(f"colour: {window.get_at((749, 50))}")
    for event in pygame.event.get():
        #closing the window when the close button is clicked
        if event.type == pygame.QUIT:
            running = False
        
    #checking game over condition
    if marker.lives == 0:
            #display game over text
            window.blit(game_over_text, (screen_width//2 - 200, screen_height//2 - 50))
            pygame.display.flip()
            pygame.time.delay(5000)
            print("Game Over")
            running = False
            break

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
    
    if key[pygame.K_SPACE]:
        marker.push(None)
        
    marker.move(key)
    marker.draw(window)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()