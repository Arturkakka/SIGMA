import pygame
import random
import sys
from pygame import *

# Налаштування основних параметрів гри
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
TEXT_COLOR = (255, 255, 255)
BACKGROUND_COLOR = (0, 0, 0)
FPS = 40
BADDIE_MIN_SIZE = 10
BADDIE_MAX_SIZE = 40
BADDIE_MIN_SPEED = 1
BADDIE_MAX_SPEED = 8
ADD_NEW_BADDIE_RATE = 6
ADD_NEW_BONUS_RATE = 200 
PLAYER_MOVE_RATE = 5
PLAYER_HEALTH = 3  
BONUS_SIZE = 20  

# Клас для створення та управління гравцем
class Player(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        super().__init__()
        self.image = pygame.image.load(image_path) 
        self.rect = self.image.get_rect()  
        self.rect.topleft = (x, y)  
        self.move_left = self.move_right = self.move_up = self.move_down = False  

    def update(self):
       
        if self.move_left and self.rect.left > 0:
            self.rect.move_ip(-1 * PLAYER_MOVE_RATE, 0)
        if self.move_right and self.rect.right < WINDOW_WIDTH:
            self.rect.move_ip(PLAYER_MOVE_RATE, 0)
        if self.move_up and self.rect.top > 0:
            self.rect.move_ip(0, -1 * PLAYER_MOVE_RATE)
        if self.move_down and self.rect.bottom < WINDOW_HEIGHT:
            self.rect.move_ip(0, PLAYER_MOVE_RATE)

# Клас для створення та управління ворогами
class Baddie(pygame.sprite.Sprite):
    def __init__(self, image_path, size, speed, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image_path), (size, size))  
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)  
        self.speed = speed  

    def update(self):
        # Рух ворога
        self.rect.move_ip(0, self.speed)

# Клас для створення та управління бонусами
class Bonus(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image_path), (BONUS_SIZE, BONUS_SIZE))  
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)  
        self.speed = 5  # Швидкість

    def update(self):
        # Рух бонусу
        self.rect.move_ip(0, self.speed)


def terminate():
    pygame.quit()  
    sys.exit()  


def wait_for_player_to_press_key():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()  
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()  # Завершення гри при натисканні Escape
                return

# Функція для перевірки зіткнення гравця з ворогом
def player_has_hit_baddie(player, baddies):
    hit_baddie = pygame.sprite.spritecollideany(player, baddies)
    if hit_baddie:
        baddies.remove(hit_baddie)  # Видалення ворога після зіткнення
        return True
    return False

# Функція для перевірки зіткнення гравця з бонусом
def player_has_hit_bonus(player, bonuses):
    hit_bonus = pygame.sprite.spritecollideany(player, bonuses)
    if hit_bonus:
        bonuses.remove(hit_bonus)  # Видалення бонусу після зіткнення
        return True
    return False


def draw_text(text, font, surface, x, y):
    text_obj = font.render(text, 1, TEXT_COLOR)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)


def draw_centered_text(text, font, surface, y):
    text_obj = font.render(text, 1, TEXT_COLOR)
    text_rect = text_obj.get_rect(center=(WINDOW_WIDTH / 2, y))
    surface.blit(text_obj, text_rect)

#налаштування вікна гри
pygame.init()
main_clock = pygame.time.Clock()
window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Dodger')
pygame.mouse.set_visible(False)

# Налаштування шрифтів та звуків
font = pygame.font.SysFont(None, 48)
game_over_sound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('background.mid')

player = Player('player.png', WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50)
baddies = pygame.sprite.Group()
bonuses = pygame.sprite.Group()

#скидання гри
def reset_game():
    global baddies, bonuses
    baddies.empty() 
    bonuses.empty()  

top_score = 0
while True:
    # Початкові налаштування перед грою
    baddies.empty()
    bonuses.empty()
    score = 0
    health = PLAYER_HEALTH
    player.rect.topleft = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50)
    reverse_cheat = slow_cheat = False
    baddie_add_counter = 0
    bonus_add_counter = 0
    pygame.mixer.music.play(-1, 0.0)  

    while True:
        score += 1  # Збільшення рахунку
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == ord('z'):
                    reverse_cheat = True 
                if event.key == ord('x'):
                    slow_cheat = True
                if event.key == K_LEFT or event.key == ord('a'):
                    player.move_right = False
                    player.move_left = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    player.move_left = False
                    player.move_right = True
                if event.key == K_UP or event.key == ord('w'):
                    player.move_down = False
                    player.move_up = True
                if event.key == K_DOWN or event.key == ord('s'):
                    player.move_up = False
                    player.move_down = True

            if event.type == KEYUP:
                if event.key == ord('z'):
                    reverse_cheat = False
                    score = 0  
                if event.key == ord('x'):
                    slow_cheat = False
                    score = 0  
                if event.key == K_ESCAPE:
                    terminate()

                if event.key == K_LEFT or event.key == ord('a'):
                    player.move_left = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    player.move_right = False
                if event.key == K_UP or event.key == ord('w'):
                    player.move_up = False
                if event.key == K_DOWN or event.key == ord('s'):
                    player.move_down = False

            if event.type == MOUSEMOTION:
                player.rect.centerx = event.pos[0]
                player.rect.centery = event.pos[1]

        if not reverse_cheat and not slow_cheat:
            baddie_add_counter += 1
        if baddie_add_counter == ADD_NEW_BADDIE_RATE:
            baddie_add_counter = 0
            baddie_size = random.randint(BADDIE_MIN_SIZE, BADDIE_MAX_SIZE)
            baddie = Baddie('baddie.png', baddie_size, random.randint(BADDIE_MIN_SPEED, BADDIE_MAX_SPEED),
                            random.randint(0, WINDOW_WIDTH - baddie_size), 0 - baddie_size)
            baddies.add(baddie)

        bonus_add_counter += 1
        if bonus_add_counter == ADD_NEW_BONUS_RATE:
            bonus_add_counter = 0
            bonus = Bonus('bonus.png', random.randint(0, WINDOW_WIDTH - BONUS_SIZE), 0 - BONUS_SIZE)
            bonuses.add(bonus)

        
        player.update()
        baddies.update()
        bonuses.update()

        # Видалення ворогів, що вийшли за межі 
        for baddie in baddies:
            if baddie.rect.top > WINDOW_HEIGHT:
                baddies.remove(baddie)

        # Видалення бонусів що вийшли за межі
        for bonus in bonuses:
            if bonus.rect.top > WINDOW_HEIGHT:
                bonuses.remove(bonus)

        # Малювання всіх обєктів 
        window_surface.fill(BACKGROUND_COLOR)
        baddies.draw(window_surface)
        bonuses.draw(window_surface)
        window_surface.blit(player.image, player.rect)

        # Відображення рахунку та здоровя гравця
        draw_text(f'Score: {score}', font, window_surface, 10, 0)
        draw_text(f'Top Score: {top_score}', font, window_surface, 10, 40)
        draw_text(f'Health: {health}', font, window_surface, 10, 80)

        pygame.display.update()

        # Перевірка зіткнення гравця з ворогом
        if player_has_hit_baddie(player, baddies):
            health -= 1
            if health == 0:
                if score > top_score:
                    top_score = score
                break

        # Перевірка зіткнення гравця з бонусом
        if player_has_hit_bonus(player, bonuses):
            health += 1  

        main_clock.tick(FPS)

    pygame.mixer.music.stop()
    game_over_sound.play()

    # Відображення тексту
    draw_centered_text('Game Over', font, window_surface, WINDOW_HEIGHT / 3)
    draw_centered_text('Press a key to play again.', font, window_surface, (WINDOW_HEIGHT / 3) + 50)
    pygame.display.update()
    wait_for_player_to_press_key()
    reset_game() 
