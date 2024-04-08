import pygame
import random
import json
import math
import datetime

pygame.init()

WIDTH = int(1280)
HEIGHT = int(1024)

NEWTON_IMAGE = pygame.transform.scale(pygame.image.load("newton.png"), (int(201 * 0.67), int(346 * 0.67)))
APPLE_IMAGE = pygame.transform.scale(pygame.image.load("apple.png"), (int(100 * 0.67), int(100 * 0.67)))

BKG_COLOR = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

game_bg = pygame.image.load("game_bg.png")
game_bg = pygame.transform.scale(game_bg, (WIDTH, HEIGHT))

player_size = int(150 * 0.67)
player_pos = [WIDTH / 2, HEIGHT - 2 * player_size]

enemy_size = int(100 * 0.67)
enemy_pos = [random.randint(0, WIDTH - enemy_size), 0]
enemy_list = [enemy_pos]
SPEED = int(10 * 0.67)

score = 0
screen = pygame.display.set_mode((WIDTH, HEIGHT))

game_over = False

clock = pygame.time.Clock()

FONT = pygame.font.Font("level-up.otf", int(72 * 0.67))


def save_scores(scores):
    with open('scores.json', 'w') as file:
        json.dump(scores, file)


def load_scores():
    try:
        with open('scores.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return {}


scores = load_scores()


def draw_menu():
    screen.fill(BKG_COLOR)
    menu_bg = pygame.image.load("wp.png")
    menu_bg = pygame.transform.scale(menu_bg, (WIDTH, HEIGHT))
    screen.blit(menu_bg, (0, 0))

    title_text = "NEWTON GAME"
    title_font = pygame.font.Font("level-up.otf", int(37 * 0.67))
    title_label = title_font.render(title_text, True, YELLOW)
    title_rect = title_label.get_rect(center=(WIDTH / 1.97, HEIGHT / 8.7))

    breathing = int(5 * (1 + math.sin(pygame.time.get_ticks() / 300)))

    shadow_label = title_font.render(title_text, True, WHITE)
    shadow_rect = shadow_label.get_rect(center=(title_rect.centerx + breathing, title_rect.centery + breathing))

    screen.blit(shadow_label, shadow_rect)

    outline_label = title_font.render(title_text, True, BLACK)
    outline_rect = outline_label.get_rect(center=(title_rect.centerx + 2, title_rect.centery + 2))
    screen.blit(outline_label, outline_rect)

    screen.blit(title_label, title_rect)

    text_play = "Press SPACE to play"
    label_play = FONT.render(text_play, True, BLACK)

    larger_font = pygame.font.Font("level-up.otf", int(76 * 0.67))
    label_play = larger_font.render(text_play, True, BLACK)

    scale_factor = 1 + 0.1 * math.sin(pygame.time.get_ticks() / 300)

    scaled_text = pygame.transform.scale(label_play, (int(label_play.get_width() * scale_factor), int(label_play.get_height() * scale_factor)))

    text_rect = scaled_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))

    screen.blit(scaled_text, text_rect)

    text_play = "Press SPACE to play"
    label_play = FONT.render(text_play, True, WHITE)

    scale_factor = 1 + 0.1 * math.sin(pygame.time.get_ticks() / 300)

    scaled_text = pygame.transform.scale(label_play, (int(label_play.get_width() * scale_factor), int(label_play.get_height() * scale_factor)))

    text_rect = scaled_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))

    screen.blit(scaled_text, text_rect)

    developer_text = "Developers: H. Andris, N. Bence, Z. Botond (10)"
    developer_label = pygame.font.Font("level-up.otf", int(22 * 0.67)).render(developer_text, True, WHITE)
    developer_rect = developer_label.get_rect(bottomleft=(int(20 * 0.67), HEIGHT - int(20 * 0.67)))

    outline_thickness = int(2 * 0.67)
    outline_rect = developer_rect.inflate(outline_thickness * 2, outline_thickness * 2)
    pygame.draw.rect(screen, BLACK, outline_rect)
    screen.blit(developer_label, developer_rect)

    copyright_text = "Copyright Kenyer CO. Do not distribute! v0.91"
    copyright_label = pygame.font.Font("level-up.otf", int(20 * 0.67)).render(copyright_text, True, WHITE)
    copyright_rect = copyright_label.get_rect(bottomright=(WIDTH - int(20 * 0.67), HEIGHT - int(20 * 0.67)))

    outline_rect = copyright_rect.inflate(outline_thickness * 2, outline_thickness * 2)
    pygame.draw.rect(screen, BLACK, outline_rect)
    screen.blit(copyright_label, copyright_rect)

    current_time = datetime.datetime.now().strftime("UTC+1: %H:%M:%S")
    time_label = pygame.font.Font("level-up.otf", int(30 * 0.67)).render(current_time, True, WHITE)
    time_rect = time_label.get_rect(topright=(WIDTH - int(20 * 0.67), int(20 * 0.67)))
    screen.blit(time_label, time_rect)

    pygame.display.update()

def start_level(level):
    global enemy_size, SPEED
    if level == 1:
        enemy_size = int(150 * 0.67)
        SPEED = 6
    elif level == 2:
        enemy_size = int(100 * 0.67)
        SPEED = 10
    elif level == 3:
        enemy_size = int(50 * 0.67)
        SPEED = 15


def GAME_OVER(score):
    screen.fill(BKG_COLOR)

    screen.blit(game_bg, (0, 0))

    text = "GAME OVER!"
    label = pygame.font.Font("level-up.otf", int(100 * 0.67)).render(text, True, (230,38,0))
    label_rect = label.get_rect(center=(WIDTH / 2, HEIGHT / 3))

    breathing = int(10 * (1 + math.sin(pygame.time.get_ticks() / 300)))

    label_breath = pygame.transform.scale(label, (label.get_width() + breathing, label.get_height() + breathing))
    label_rect_breath = label_breath.get_rect(center=(WIDTH / 2, HEIGHT / 3))

    outline_label = pygame.font.Font("level-up.otf", int(105 * 0.67)).render(text, True, BLACK)
    outline_rect = outline_label.get_rect(center=(label_rect_breath.centerx + 2, label_rect_breath.centery + 2))

    outline_label = pygame.transform.scale(outline_label, (outline_label.get_width() + breathing, outline_label.get_height() + breathing))
    outline_rect = outline_label.get_rect(center=(label_rect_breath.centerx + 2, label_rect_breath.centery + 2))

    screen.blit(outline_label, outline_rect)

    screen.blit(label_breath, label_rect_breath)

    text_score = "Your Score: " + str(score)
    label_score = FONT.render(text_score, True, YELLOW)
    label_score_rect = label_score.get_rect(center=(WIDTH / 2, HEIGHT / 2 + int(100 * 0.67)))

    outline_label_score = FONT.render(text_score, True, BLACK)
    outline_rect_score = outline_label_score.get_rect(center=(label_score_rect.centerx + 2, label_score_rect.centery + 2))

    screen.blit(outline_label_score, outline_rect_score)

    screen.blit(label_score, label_score_rect)

    text_restart = "Press SPACE to restart."
    label_restart = FONT.render(text_restart, True, YELLOW)
    label_restart_rect = label_restart.get_rect(center=(WIDTH / 2, HEIGHT / 2 + int(200 * 0.67)))

    outline_label_restart = FONT.render(text_restart, True, BLACK)
    outline_rect_restart = outline_label_restart.get_rect(center=(label_restart_rect.centerx + 2, label_restart_rect.centery + 2))

    screen.blit(outline_label_restart, outline_rect_restart)

    screen.blit(label_restart, label_restart_rect)

    pygame.display.update()


def set_level(score, SPEED):
    if score < 3:
        SPEED = 6
    elif score < 10:
        SPEED = 8
    elif score < 20:
        SPEED = 10
    elif score < 35:
        SPEED = 15
    elif score < 50:
        SPEED = 20
    else:
        SPEED = 25
    return SPEED


def drop_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < 1 and delay < 1:
        x_pos = random.randint(0, WIDTH - enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])


def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        screen.blit(APPLE_IMAGE, (enemy_pos[0], enemy_pos[1]))


def update_enemy_positions(enemy_list, score):
    for i, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < HEIGHT:
            enemy_pos[1] += SPEED
        else:
            enemy_list.pop(i)
            score += 1
    return score


def collision_check(enemy_list, player_pos):
    player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)
    for enemy_pos in enemy_list:
        enemy_rect = pygame.Rect(enemy_pos[0], enemy_pos[1], enemy_size, enemy_size)
        if player_rect.colliderect(enemy_rect):
            enemy_list.remove(enemy_pos)
            return True
    return False


def draw_score(score, score_changed):
    text = "Score: " + str(score)

    label_white = FONT.render(text, True, WHITE)
    label_black = FONT.render(text, True, BLACK)

    if score_changed:
        scale_factor = 1.2

        scaled_text_white = pygame.transform.scale(label_white, (int(label_white.get_width() * scale_factor), int(label_white.get_height() * scale_factor)))
        scaled_text_black = pygame.transform.scale(label_black, (int(label_black.get_width() * scale_factor), int(label_black.get_height() * scale_factor)))

        text_rect = scaled_text_white.get_rect(topleft=(int(10 * 0.67), int(10 * 0.67)))

        screen.blit(scaled_text_black, (text_rect.x + 2, text_rect.y + 2))
        screen.blit(scaled_text_white, text_rect)
    else:
        text_rect = label_white.get_rect(topleft=(int(10 * 0.67), int(10 * 0.67)))

        screen.blit(label_black, (text_rect.x + 2, text_rect.y + 2))
        screen.blit(label_white, text_rect)


def restart_game():
    global player_pos, enemy_list, score, game_over
    player_pos = [WIDTH / 2, HEIGHT - 2 * player_size]
    enemy_list = [[random.randint(0, WIDTH - enemy_size), 0]]
    score = 0
    game_over = False


running = True
menu_active = True
current_level = 1
return_to_menu = False
score_changed = False

while running:
    if menu_active:
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menu_active = False
                elif event.key == pygame.K_1:
                    pass
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_pos[0] -= player_size
                elif event.key == pygame.K_RIGHT:
                    player_pos[0] += player_size
                elif event.key == pygame.K_SPACE and game_over:
                    restart_game()
                elif event.key == pygame.K_ESCAPE:
                    return_to_menu = True
                elif event.key == pygame.K_SPACE and not game_over:
                    pass

        if return_to_menu:
            menu_active = True
            return_to_menu = False
            continue

        screen.blit(game_bg, (0, 0))

        if not game_over:
            drop_enemies(enemy_list)
            score = update_enemy_positions(enemy_list, score)
            SPEED = set_level(score, SPEED)

            if collision_check(enemy_list, player_pos) is True:
                score += 1
                score_changed = True
            else:
                score_changed = False

            draw_enemies(enemy_list)
            screen.blit(NEWTON_IMAGE, (player_pos[0], player_pos[1]))

        else:
            GAME_OVER(score)

        draw_score(score, score_changed)

        for enemy_pos in enemy_list:
            if enemy_pos[1] > HEIGHT - player_size:
                game_over = True
                break

        pygame.display.update()
        clock.tick(30)

save_scores(scores)

pygame.quit()
