import pygame
import random
import sys
import time

pygame.init()

WIDTH = 800
HEIGHT = 600

BLUE = (0,0,255)
RED = (255,0,0)
BKG_COLOR = (0,0,0)
YELLOW = (255,255,0)


player_size = 50
player_pos = [WIDTH/2, HEIGHT - 2 * player_size]

enemy_size = 50
enemy_pos = [random.randint(0, WIDTH - enemy_size), 0]
enemy_list = [enemy_pos]
SPEED = 10

score = 0
screen =  pygame.display.set_mode((WIDTH, HEIGHT))

game_over = False

clock = pygame.time.Clock()

FONT = pygame.font.SysFont("monospace", 35)

def GAME_OVER(score):
    screen.fill(BKG_COLOR)
    pygame.display.update()
    text = "GAME OVER!"
    text1 ="Your Score: " + str(score)
    label = FONT.render(text, 1, YELLOW)
    
    screen.blit(label, ((WIDTH / 2) - ((len(text) * 20) / 2), HEIGHT / 2))
    
    
    label1 = FONT.render(text1, 1, YELLOW)
    screen.blit(label1, ((WIDTH / 2) - ((len(text) * 25) / 2), HEIGHT / (5/2)))
    pygame.display.update()
    
def set_level(score, SPEED):
    if score < 20:
        SPEED = 5
    elif score < 40:
        SPEED = 8
    elif score < 60:
        SPEED = 10
    else:
        SPEED = 15
    return SPEED

def drop_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < 1 and delay < 1:
        x_pos = random.randint(0,WIDTH - enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])

def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        pygame.draw.rect(screen, RED, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

def update_enemy_positions(enemy_list, score):
    for i, enemy_pos in enumerate(enemy_list):
        # Updates Enemy Position
        if enemy_pos[1] >= 0 and enemy_pos[1] < HEIGHT:
            enemy_pos[1] += SPEED
        else:
            enemy_list.pop(i)
            score += 1
    return score


def collision_check(enemy_list, player_pos):
    for enemy_pos in enemy_list:
        if detect_collision(player_pos, enemy_pos):
            return True
    return False
def detect_collision(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]

    if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x + enemy_size)):
        if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < e_y + enemy_size):
            return True
        
    return False 

running = True
game_over = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_pos[0] -= player_size
            elif event.key == pygame.K_RIGHT:
                player_pos[0] += player_size

    screen.fill(BKG_COLOR)
    
    if not game_over:
        drop_enemies(enemy_list)
        score = update_enemy_positions(enemy_list, score)
        SPEED = set_level(score, SPEED)
        
        if collision_check(enemy_list, player_pos):
            score += 1  # Pontszám növelése, ha elkapják az ellenséget

        draw_enemies(enemy_list)
        pygame.draw.rect(screen, BLUE, (player_pos[0], player_pos[1], player_size, player_size))
    else:
        GAME_OVER(score)

    # A pontszám megjelenítése mindkét esetben
    text = "Score: " + str(score)
    label = FONT.render(text, 1, YELLOW)
    screen.blit(label, (10, 10))  # Pontszám megjelenítése a képernyő bal felső sarkában
    
    # Ellenőrzés, hogy az ellenség elért-e a játékosig
    for enemy_pos in enemy_list:
        if enemy_pos[1] > HEIGHT - player_size:
            game_over = True
            GAME_OVER(score)
            break  # Kilépés a ciklusból, ha az egyik ellenség elért a játékosig

    pygame.display.update()
    clock.tick(30)
