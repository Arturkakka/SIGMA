import pygame 
pygame.init()
import random

windows = pygame.display.set_mode((500,500))

back_color = (9, 128, 251)
game = True
clock = pygame.time.Clock()
player1 = pygame.Rect(230,230,30,30)

bullets = []
bullets2 = []


while game:

    if random.randint(0,200) < 10:
        x = random.randint(0,480)
        y = -10
        bullets.append(pygame.Rect(x, y, 20, 20))

    for b in bullets:
        pygame.draw.rect(windows, (0,0,0), b)

    for b in bullets:
        b.y += 5
        if b.colliderect(player1):
            game = False 
##################################################
    if random.randint(0,200) < 10:
        x = -10
        y = random.randint(0,480)
        bullets2.append(pygame.Rect(x, y, 20, 20))

    for b in bullets2:
        pygame.draw.rect(windows, (0,0,0), b)

    for b in bullets2:
        b.x += 5
        if b.colliderect(player1):
            game = False 
        
    


    
    pygame.display.update()
    clock.tick(60)
    windows.fill(back_color)
    pygame.draw.rect(windows,(0,0,255),player1)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player1.x > 0:
        player1.x -= 5 
    if keys[pygame.K_d] and player1.x < 450:
        player1.x += 5 
    if keys[pygame.K_s] and player1.y < 450:
        player1.y += 5 
    if keys[pygame.K_w] and player1.y > 0:
        player1.y -= 5 
    