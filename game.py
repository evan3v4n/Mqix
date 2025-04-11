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
you_win_text = font_big.render('You Win!', True, 'black')
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

#create a board instance
board = Board(screen_width,screen_height,initial_margin,window,bg_color)
#create a marker instance
marker = Marker(screen_width, screen_height, initial_margin,board=board)

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

    #square of red, so when you claim area colour appears
    pygame.draw.polygon(window,(238,87,35),[(initial_margin,initial_margin),
                                            (screen_height-1-initial_margin,initial_margin-1),
                                            (screen_width-1-initial_margin,screen_width-1-initial_margin),
                                            (initial_margin,screen_width-1-initial_margin)])
    #draw window
    board.draw(window)
    
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
    if board.check_if_win():
            #display game over text
            window.blit(you_win_text, (screen_width//2 - 150, screen_height//2 - 50))
            pygame.display.flip()
            pygame.time.delay(5000)
            print("You Win")
            running = False
            break
    key = pygame.key.get_pressed()

    #TESTING REMOVE LATER
    if key[pygame.K_p]:
         board.update_border([(200, 749), (200, 500), (49, 500)])
    if key[pygame.K_o]:
         board.update_border([(200,49),(200,200),(300,200),(300,600),(600,600),(600,49)])
    #if key[pygame.K_i]:
    #     board.update_border([(49,500),(749,500)]) 
    #if key[pygame.K_u]:
    #     board.update_border([(49,700),(749,700)]) 
    if key[pygame.K_l]:
       board.update_border([(49,300),(90,300),(90,500)]) 
    if key[pygame.K_k]:
       board.update_border([(600,749),(600,700),(700,700),(700,749)])
    
    
    #TESTING REMOVE LATER

    
    
    if key[pygame.K_SPACE]:
        marker.push()
    #print(f"moving left: {marker.moving_left}, moving right: {marker.moving_right}, moving up: {marker.moving_up}, moving down: {marker.moving_down}")
    #print(f"turning points: {marker.turn_points}")   
    marker.move(key)
    marker.draw(window)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()