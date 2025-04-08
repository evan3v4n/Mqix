import pygame
from marker import Marker 

# game setup
pygame.init()
pygame.font.init()
window = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Mqix')

running = True
clock = pygame.time.Clock()

#font setup
font = pygame.font.SysFont('DroidSans', 30)
lives_text = font.render('LIVES: ', True, 'black')
one_life = font.render('*', True, 'black')
two_lives = font.render('* *', True, 'black')
three_lives = font.render('* * *', True, 'black')

# window related variables
bg_color = (252, 215, 183)
screen_width = window.get_width()
screen_height = window.get_height()
initial_margin = 50 # distance of the border from the edge of the screen
border_rect = pygame.Rect(0,0, screen_width - (2*initial_margin), screen_height - (2*initial_margin))
border_rect.center = (screen_width/2, screen_height/2)

#create a marker instance
marker = Marker(screen_width, screen_height, initial_margin)

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

    key = pygame.key.get_pressed()
    if key[pygame.K_SPACE]:
        marker.push(None)
        
    marker.move(key)
    marker.draw(window)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()