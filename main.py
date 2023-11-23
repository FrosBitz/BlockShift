import pygame
import sys
import random
import math
from setting import *


class Display :

    #global highest_score

    def __init__(self) :
        self.font = pygame.font.Font(None, FONT_SIZE)
        pygame.display.set_caption("Falling 2048")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0)
    def color(self) :
        #self.screen.fill(m_grey)
        self.screen.fill(d_grey, rect = (200, 100, 80, 560))
        self.screen.fill(l_grey, rect = (280, 100, 80, 560))
        self.screen.fill(d_grey, rect = (360, 100, 80, 560))
        self.screen.fill(l_grey, rect = (440, 100, 80, 560))
        self.screen.fill(d_grey, rect = (520, 100, 80, 560))
        self.screen.fill(nearly_white, rect = (200, 100, 400, 80))
    def line(self) :
        pygame.draw.line(self.screen, frame_color, (195, 97), (604, 97), 5)
        pygame.draw.line(self.screen, frame_color, (195, 662), (604, 662), 5)
        pygame.draw.line(self.screen, frame_color, (197, 96), (197, 662), 5)
        pygame.draw.line(self.screen, frame_color, (602, 96), (602, 662), 5) 
    def draw_text(self, text, x, y):
        img = self.font.render(text, True, BLACK)
        self.screen.blit(img, [x, y])
    def run(self, score) :
        self.color()
        self.line()
        #self.draw_text("BlockShift", 310, 40)
        self.draw_text("Score ", 280, 690)
        self.draw_text(str(score), 520 - self.font.size(str(score))[0], 690)
    def game_over(self) :
        pygame.draw.rect(self.screen, WHITE, (120, 330, 560, 140))
        self.draw_text("GAME OVER", 300, 355)
        self.draw_text("PRESS 'R' TO RESTART GAME", 150, 405)
                 
class Block :
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
    def text(self, text, x, y):
        img = self.font.render(text, True, BLACK)
        self.screen.blit(img, [x, y])
    def draw(self, num, x, y):
        red = 237 * num % 256
        green = 211 * num % 256
        blue = 179 * num % 256
        color = (red, green, blue)
        pygame.draw.rect(self.screen, color, (x, y, BLOCK_SIZE, BLOCK_SIZE),border_radius=15)
        (w, h) = self.font.size(str(2 ** num))
        num_pos_x = x + BLOCK_SIZE / 2 - w / 2
        num_pos_y = y + BLOCK_SIZE / 2 - h / 2
        self.text(str(2 ** num), num_pos_x, num_pos_y)

def restart_game() -> None :

    global field
    global score
    global fall_speed

    global is_moving
    global next_num
    global horizontal_input
    global horizontal_delay
    global vertical_input
    global game_over
    
    field = [[0 for i in range(FIELD_WIDTH)] for j in range(FIELD_HEIGHT)]
    score = 0
    fall_speed = 0.02

    is_moving = False
    next_num = random.randint(1, 5)
    horizontal_input = 0
    horizontal_delay = 0
    vertical_input = 0
    game_over = False


def highest(w: int) -> int :
    global field
    for h in range(FIELD_HEIGHT) :
        if field[h][w] > 0 :
            return h
    return FIELD_HEIGHT


def is_fallable(h: int, w :int) -> bool:
    for check_h in range(h + 1, FIELD_HEIGHT) :
        if field[check_h][w] == 0 :
            return True
    return False


def combine_animation() -> None :

    global is_animating
    global animation_place
    global animation_direction
    global animation_progress
    global animation_type
    

    # case 1 : down, left, right
    for h in range(FIELD_HEIGHT - 1) :
        for w in  range(1, FIELD_WIDTH - 1) :
            if field[h][w] > 0 and field[h][w] == field[h + 1][w] == field[h][w - 1] == field[h][w + 1] :
                is_animating = True
                animation_place = [w, h]
                animation_direction = [DOWN, LEFT, RIGHT]
                animation_progress = 0
                animation_type = COMBINE
                return
    
    # case 2 : left, right 
    for h in range(FIELD_HEIGHT) :
        for w in range(1, FIELD_WIDTH - 1) :
            if field[h][w] > 0 and field[h][w] == field[h][w - 1] == field[h][w + 1] :
                is_animating = True
                animation_place = [w, h]
                animation_direction = [LEFT, RIGHT]
                animation_progress = 0
                animation_type = COMBINE
                return
            
    # case 3 : down, right
    for h in range(FIELD_HEIGHT - 1) :
        for w in range(0, FIELD_WIDTH - 1) :
            if field[h][w] > 0 and field[h][w] == field[h + 1][w] == field[h][w + 1] :
                is_animating = True
                animation_place = [w, h]
                animation_direction = [DOWN, RIGHT]
                animation_progress = 0
                animation_type = COMBINE
                return

    # case 4 : down, left
    for h in range(FIELD_HEIGHT - 1) :
        for w in range(1, FIELD_WIDTH) :
            if field[h][w] > 0 and field[h][w] == field[h + 1][w] == field[h][w - 1] :
                is_animating = True
                animation_place = [w, h]
                animation_direction = [DOWN, LEFT]
                animation_progress = 0
                animation_type = COMBINE
                return
        
    # case 5 : down
    for h in range(FIELD_HEIGHT - 1) :
        for w in range(FIELD_WIDTH) :
            if field[h][w] > 0 and field[h][w] == field[h + 1][w] :
                is_animating = True
                animation_place = [w, h]
                animation_direction = [DOWN]
                animation_progress = 0
                animation_type = COMBINE
                return

    # case 6 : right
    for h in range(FIELD_HEIGHT) :
        for w in range(FIELD_WIDTH - 1) :
            if field[h][w] > 0 and field[h][w] == field[h][w + 1] :
                is_animating = True
                animation_place = [w, h]
                animation_direction = [RIGHT]
                animation_progress = 0
                animation_type = COMBINE
                return
            

def fall_animation() -> None :
    
    global is_animating
    global animation_place
    global animation_direction
    global animation_progress
    global animation_type
    global fall_check

    fall_check = [[False for i in range(FIELD_WIDTH)] for j in range(FIELD_HEIGHT)]
    is_falling = False

    for h in range(FIELD_HEIGHT) :
        for w in range(FIELD_WIDTH) :
            if field[h][w] > 0 and is_fallable(h, w) :
                is_falling = True
                fall_check[h][w] = True
    if is_falling == True :
        is_animating = True
        animation_progress = 0
        animation_type = FALL


def set_animation() -> None :
    combine_animation()
    fall_animation()


def is_animating_place(h :int, w :int) -> bool :
    global animation_place
    global animation_direction
    global animation_type
    global fall_check
    if animation_type == COMBINE :
        for direction in animation_direction :
            if h == animation_place[1] + direction[1] and w == animation_place[0] + direction[0] :
                return True
    elif animation_type == FALL :
        if fall_check[h][w] == True :
            return True
    return False

def main() :

    global field
    global score
    global fall_speed

    global is_moving
    global moving_num
    global next_num
    global horizontal_input
    global horizontal_delay
    global vertical_input
    global game_over
    
    global is_animating
    global animation_place
    global animation_direction
    global animation_progress
    global animation_type
    global fall_check

    moving_pos = [-1, -1] # moving_pos[0] = horizontal, moving_pos[1] = vertical
    fall_speed = 0.02
    delay = 10

    is_moving = False
    moving_num = 0
    next_num = random.randint(1, 5)
    horizontal_input = 0
    horizontal_delay = 0
    vertical_input = 0
    game_over = False

    is_animating = False
    animation_place = []
    animation_direction = []
    animation_progress = 0
    animation_type = 0
    fall_check = []

    field = [[0 for i in range(FIELD_WIDTH)] for j in range(FIELD_HEIGHT)]
    score = 0

    pygame.init()

    pygame.display.set_caption("Falling 2048")
    clock = pygame.time.Clock()
    display = Display()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0)
    font =  pygame.font.Font(None, FONT_SIZE)
    background = pygame.image.load('/Users/peemsutthi/Desktop/BlockSHIFT/assets/background2.JPG').convert()
    backgroundSurface = pygame.transform.scale(background,(2800,2660))
    backgroundRect = backgroundSurface.get_rect(center = (400,380))

    running = True
    while running :
        

        screen.blit(backgroundSurface,backgroundRect)

        display.run(score)

        button = pygame.key.get_pressed()
        
        if horizontal_delay > 0 :
            horizontal_delay -= 1
        if horizontal_delay == 0 and is_moving :
            if button[pygame.K_LEFT] or button[pygame.K_a] :
                horizontal_input -= 1
                horizontal_delay = 8
            if button[pygame.K_RIGHT] or button[pygame.K_d] :
                horizontal_input += 1
                horizontal_delay = 8
        if button[pygame.K_DOWN] or button[pygame.K_s] or button[pygame.K_SPACE]:
            vertical_input = 1
        
        # game algorithm
        if not game_over :
            if not is_animating :
                if is_moving :
                    # moving block in horizontal update
                    if horizontal_input == 1 and moving_pos[1] > -1 and moving_pos[0] < FIELD_WIDTH - 1 and field[math.ceil(moving_pos[1])][moving_pos[0] + 1] == 0 :
                        moving_pos[0] += 1 
                    elif horizontal_input == -1 and moving_pos[1] > -1  and moving_pos[0] > 0 and field[math.ceil(moving_pos[1])][moving_pos[0] - 1] == 0 :
                        moving_pos[0] -= 1
                    # moving block in vertical update
                    if moving_pos[1] < FIELD_HEIGHT - 1 and field[math.floor(moving_pos[1]) + 1][moving_pos[0]] == 0 :
                        moving_pos[1] += fall_speed
                        if vertical_input == 1 :
                            moving_pos[1] += 0.1
                        moving_pos[1] = min(moving_pos[1], highest(moving_pos[0]) - 1)
                    else :
                        if highest(moving_pos[0]) > 0 :
                            field[math.floor(moving_pos[1])][moving_pos[0]] = moving_num
                        else :
                            game_over = True
                        delay = 10
                        is_moving = False
                else : # not is_moving
                    if delay > 0 :
                        delay -= 1
                    elif delay == 0 :
                        is_moving = True
                        moving_num = next_num
                        next_num = random.randint(1, 5)
                        moving_pos = [random.randint(0, FIELD_WIDTH - 1), -1]
                        if fall_speed <= 0.06 :
                            fall_speed += 0.0002 

            if is_animating : 
                if animation_type == COMBINE :
                    if animation_progress < 1 :
                        animation_progress = min(animation_progress + fall_speed, 1)
                    elif animation_progress == 1 :
                        for direction in animation_direction :
                            field[animation_place[1]][animation_place[0]] += 1
                            field[animation_place[1] + direction[1]][animation_place[0] + direction[0]] = 0
                            
                        score += 2 ** (field[animation_place[1]][animation_place[0]])
                        is_animating = False
                elif animation_type == FALL :
                    if animation_progress < 1 :
                        animation_progress = min(animation_progress + fall_speed, 1)
                    elif animation_progress == 1 :
                        for h in range(FIELD_HEIGHT - 1, -1, -1) :
                            for w in range(FIELD_WIDTH) :
                                if fall_check[h][w] == True :
                                    field[h + 1][w] = field[h][w]
                                    field[h][w] = 0
                        is_animating = False
            else :
                set_animation()
        else : # game_over
            if button[pygame.K_r] :
                restart_game()

        horizontal_input = 0
        vertical_input = 0

        # game display
        for h in range(FIELD_HEIGHT) :
            for w in range(FIELD_WIDTH) :
                if field[h][w] > 0 :
                    if is_animating and is_animating_place(h, w) :
                        continue
                    else :
                        block = Block(screen, font)
                        block.draw(field[h][w], 200 + BLOCK_SIZE * w, 180 + BLOCK_SIZE * h)
        
        if is_moving :
            block = Block(screen, font)
            block.draw(moving_num, 200 + BLOCK_SIZE * moving_pos[0], 180 + BLOCK_SIZE * moving_pos[1])
        if is_animating :
            if animation_type == COMBINE :
                for direction in animation_direction :
                    w = animation_place[0] + direction[0]
                    h = animation_place[1] + direction[1]
                    block = Block(screen, font)
                    block.draw(field[h][w], 200 + BLOCK_SIZE * (w - direction[0] * animation_progress), 180 + BLOCK_SIZE * (h - direction[1] * animation_progress))
            elif animation_type == FALL :
                for h in range(FIELD_HEIGHT) :
                    for w in range(FIELD_WIDTH) :
                        if fall_check[h][w] == True :
                            block = Block(screen, font)
                            block.draw(field[h][w], 200 + BLOCK_SIZE * w, 180 + BLOCK_SIZE * (h + animation_progress)) 
        block = Block(screen, font)
        block.draw(next_num, 110, 100)

        if game_over :
            display.game_over()

        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                running = False
        
        pygame.display.update()
        clock.tick(60)


    pygame.quit()
    sys.exit()

if __name__ == '__main__' :
    main()