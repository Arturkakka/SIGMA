import pygame 
pygame.init()
import random
font = pygame.font.Font(None, 204)
text = font.render("", True,(0, 0, 0))

windows = pygame.display.set_mode((1370,714))

players = []

player = pygame.Rect(925,225,100,200)
player1 = pygame.Rect(725,225,100,200)
player2 = pygame.Rect(525,225,100,200)
player3 = pygame.Rect(325,225,100,200)

game = True
clock = pygame.time.Clock()

while game:
    windows.fill((9, 128, 251))
    windows.blit(text,(40,40))
    pygame.draw.rect(windows,(0,0,255),player)
    pygame.draw.rect(windows,(0,0,255),player1)
    pygame.draw.rect(windows,(0,0,255),player2)
    pygame.draw.rect(windows,(0,0,255),player3)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            print (10)
        elif event.type == pygame.KEYDOWN:
            print(20)
    pygame.display.update()
    clock.tick(60)
 