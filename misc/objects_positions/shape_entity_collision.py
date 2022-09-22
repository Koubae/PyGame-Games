"""@credit -> https://stackoverflow.com/a/65064907/13903942"""
import pygame

pygame.init()
window = pygame.display.set_mode((1280, 640))
rect1 = pygame.Rect(*window.get_rect().center, 0, 0).inflate(75, 75)
rect2 = pygame.Rect(0, 0, 85, 85)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    rect2.center = pygame.mouse.get_pos()

    coords1 = (640, 320)
    coords2 = (641, 274)
    collide = rect2.collidelist([pygame.Rect(coords1, (10, 10)), pygame.Rect(coords2, (10, 10))])
    color = (255, 255, 255)
    if collide != -1:
        color = (255, 0, 0)
        print(collide)
        # print(rect2.topright)
        # print(rect1.center)


    window.fill(0)
    pygame.draw.rect(window, color, rect1)
    pygame.draw.rect(window, (0, 255, 0), rect2, 6, 1)
    pygame.display.flip()

pygame.quit()
exit()