import pygame

# game setup
pygame.init()
window = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Mqix')

running = True
bg_color = (252, 215, 183)
marker_pos = pygame.Vector2(window.get_width()/ 2, 790)
clock = pygame.time.Clock()
vel = 5
while running:
    pygame.time.delay(100)
    window.fill(bg_color)

    for event in pygame.event.get():
        #closing the window when the close button is clicked
        if event.type == pygame.QUIT:
            running = False

    key = pygame.key.get_pressed()
    # moves marker left and right (currently no boundaries)
    if key[pygame.K_LEFT]:
        marker_pos.x -= vel
    if key[pygame.K_RIGHT]:
        marker_pos.x += vel

    pygame.draw.circle(window, 'green', marker_pos, 10)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()