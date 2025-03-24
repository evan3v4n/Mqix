import pygame
print(pygame.__version__)

# game setup
pygame.init()
window = pygame.display.set_mode((800, 800))
running = True
bg_color = (252, 215, 183)
marker_pos = pygame.Vector2(window.get_width()/ 2, 790)
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        #closing the window when the close button is clicked
        if event.type == pygame.QUIT:
            running = False

    window.fill(bg_color)

    pygame.draw.circle(window, 'green', marker_pos, 10)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()