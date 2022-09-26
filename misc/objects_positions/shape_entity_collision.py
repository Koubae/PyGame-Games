"""@credit -> https://stackoverflow.com/a/65064907/13903942"""
import pygame

pygame.init()
window = pygame.display.set_mode((1280, 640))

enemy = pygame.Rect(*window.get_rect().center, 0, 0).inflate(75, 75)
enemy_coords = enemy.topleft

sword_size = (10, 85)
sword = pygame.Rect(0, 0, *sword_size)

entities = {
    f"{enemy_coords[0]}-{enemy_coords[1]}": enemy
}

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    sword.midbottom = pygame.mouse.get_pos()

    sword_coords = sword.topleft
    sword_coords_key = f"{sword_coords[0]}-{sword_coords[1]}"


    collide = sword.collidelist([enemy])

    color = (255, 255, 255)
    if collide != -1:
        color = (255, 0, 0)
        print(collide)



    window.fill(0)
    pygame.draw.rect(window, color, enemy)
    pygame.draw.rect(window, (0, 255, 0), sword)
    pygame.display.flip()

pygame.quit()
exit()