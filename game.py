import pygame
import random
import os
import time
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

pygame.init()

# screen settings
screen_width = 870
screen_height = 970
screen = pygame.display.set_mode((screen_width, screen_height))

# imgaes setting
current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, "images")

background = pygame.image.load(os.path.join(image_path, "background.png"))

# character
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_mask = pygame.mask.from_surface(character)
character_x_pos = 20
character_y_pos = 220
to_x = 0
to_y = 0

# Tiles and colors
tile_images =[
    pygame.image.load(os.path.join(image_path, "tile1.png")),
    pygame.image.load(os.path.join(image_path, "tile2.png")),
    pygame.image.load(os.path.join(image_path, "tile3.png")),
    pygame.image.load(os.path.join(image_path, "tile4.png")),
    pygame.image.load(os.path.join(image_path, "tile5.png")),
    pygame.image.load(os.path.join(image_path, "tile6.png")),
    pygame.image.load(os.path.join(image_path, "tile7.png"))
]

colors = ["Red", "Orange", "Yellow", "Green", "Blue", "Indigo", "Purple"]

hidetile = pygame.image.load(os.path.join(image_path, "hidetile.png"))

tiles = []

pygame.display.set_caption("Mark Game")

# Font
game_font = pygame.font.Font(None, 40)


# Tracking variables
memorize = True
find = False
answer = False
correct = False
level = 1
memorize_time = 15
find_time = 10
check_time = 5
start_ticks = pygame.time.get_ticks()
elapsed_time = 0
action = ""
timer = ""
target_color = -1
difficulty = 0
color_number = 3
difficulty_changed = False
win = False

running = True 
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False
        
        if (not answer) and event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_LEFT: 
                character_x_pos -= 110
            elif event.key == pygame.K_RIGHT: 
                character_x_pos += 110
            elif event.key == pygame.K_UP: 
                character_y_pos -= 110
            elif event.key == pygame.K_DOWN: 
                character_y_pos += 110

        if (not answer) and event.type == pygame.KEYUP: 
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                to_y = 0

    if character_x_pos < 20:
        character_x_pos = 20
    elif character_x_pos > 790:
        character_x_pos = 790
    
    if character_y_pos < 220:
        character_y_pos = 220
    elif character_y_pos > 880:
        character_y_pos = 880

    # Change Difficulty
    if level % 3 == 0 and not difficulty_changed:
        difficulty += 1
        memorize_time = 15
        if color_number < 7:
            color_number += 1
        difficulty_changed = True   

    
    if len(tiles) == 0:
        for i in range(0, 56):
            col = i % 8
            row = i // 8
            tiles.append({
                "img": tile_images[random.randrange(0, color_number)],
                "x_pos": col * 110,
                "y_pos": 200 + (row * 110)
            })
    

    # draw screen

    # Background
    screen.blit(background, (0, 0))

    # timer
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    if memorize:
        if (memorize_time - elapsed_time) <= 0 :
            memorize = False
            find = True
            target_color = random.randrange(0, color_number)
            start_ticks = pygame.time.get_ticks()
    elif find:
        if (find_time - elapsed_time) <= 0:
            find = False
            answer = True
            start_ticks = pygame.time.get_ticks()
    elif answer:
        if (check_time - elapsed_time) <= 0:
            answer = False
            memorize = True
            correct = False
            tiles.clear()
            level += 1
            memorize_time -= 5
            start_ticks = pygame.time.get_ticks() 
            difficulty_changed = False     



    # check answer
    if answer and (not correct):
        for t in tiles:
            tile_mask = pygame.mask.from_surface(t["img"])
            offset = (int(character_x_pos - t["x_pos"]), int(character_y_pos - t["y_pos"]))
            result = tile_mask.overlap(character_mask, offset)
            if result and t["img"] == tile_images[target_color]:
                correct= True
                break
    
    if memorize:
        action = game_font.render("Memorize the Colors and their Positions!",\
             True, (255, 255, 255))
        timer = game_font.render("Time Left: {}".format(int(memorize_time - elapsed_time)),\
             True, (255, 255, 255))
    elif find:
        action = game_font.render("Find the correct Color! The color is {}"\
             .format(colors[target_color]), True, (255, 255, 255))
        timer = game_font.render("Time Left: {}".format(int(find_time - elapsed_time))\
             , True, (255,255,255))
    elif answer and correct and level == 17:
        action = game_font.render("You are Correct!", True, (0, 255, 0))
        timer = game_font.render("You have finished all the levels! Congrats!!", True, (0, 255, 0))
        running = False
        win = True
    elif answer and correct:
        action = game_font.render("You are Correct!", True, (0, 255, 0))
        timer = game_font.render("Next round begins in: {}".format(int(check_time - elapsed_time)),\
             True, (255, 255, 255))
    elif answer and (not correct):
        action = game_font.render("Your answer is Wrong", True, (255, 0, 0))
        running = False

    level_display = game_font.render("Level {}".format(level), True, (255, 255, 255))
    difficulty_display = game_font.render("Difficulty : {}".format(difficulty), True, (255, 255, 255))
    screen.blit(level_display, (380, 10))
    screen.blit(difficulty_display, (670, 120))
    screen.blit(action, (20, 60))
    screen.blit(timer, (20, 90)) 

    # Tiles
    if memorize:
        for idx, val in enumerate(tiles):
            tile_img = val["img"]
            tile_x = val["x_pos"]
            tile_y = val["y_pos"]
            screen.blit(tile_img, (tile_x, tile_y))
    elif answer:
        for idx, val in enumerate(tiles):
            tile_img = val["img"]
            tile_x = val["x_pos"]
            tile_y = val["y_pos"]
            if tile_images[target_color] == tile_img:
                screen.blit(tile_img, (tile_x, tile_y))
            else:
                screen.blit(hidetile, (tile_x, tile_y))
    else:
        for i in range(0, 56):
            col = i % 8
            row = i // 8
            screen.blit(hidetile, ((col * 110), 200 + (row * 110)))
    
    screen.blit(character, (character_x_pos, character_y_pos))


    pygame.display.update()

game_font = pygame.font.Font(None, 100)
if win:
    msg = game_font.render("You Won!!", True, (0, 0, 0))
else:
    msg = game_font.render("Game Over", True, (0, 0, 0))

msg_rect = msg.get_rect(center=(int(screen_width/2), int(screen_height/2)))
screen.blit(msg, msg_rect)
pygame.display.update()
pygame.time.delay(4000)

pygame.quit()