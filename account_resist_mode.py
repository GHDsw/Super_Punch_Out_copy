import game_framework
from pico2d import *

import play_mode

sprite_size = {'alphabet_table': [[1690, 2845], [1849, 2952]],
               }

TIME_PER_ACTION = 10
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 22

image = None
frame = 0

def pause():
    pass

def resume():
    pass

def init():
    global image, intro_start_time

    image = load_image('./image/Intro,Menu.png')
    intro_start_time = get_time()

def finish():
    global image
    del image

def update():
    global frame

def draw():
    clear_canvas()
    sx, sy = sprite_size['alphabet_table'][0]
    ex, ey = sprite_size['alphabet_table'][1]

    img_h = image.h  # 이미지 전체 높이
    clip_x = sx
    clip_y = img_h - ey - 1  # top-based y -> bottom-based y 변환
    clip_w = ex - sx + 1
    clip_h = ey - sy + 1
    # 22프레임, 한줄에 8프레임씩
    # 20,356 , 257,579 -> 296,356 , 551,579
    # 각 프레임은 20*20 차이
    #image.clip_draw(left, bottom, clip_w, clip_h, 400, 300)
    image.clip_draw(clip_x, clip_y, clip_w, clip_h, 400, 300)
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            game_framework.change_mode(play_mode)
