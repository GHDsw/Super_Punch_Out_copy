import game_framework
from pico2d import *

import play_mode

sprite_size = {'ring': [[1124, 66], [1379, 289]],
               'title': [[20, 66], [275,289]],
               }

TIME_PER_ACTION = 1
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION_ring = 4
FRAMES_PER_ACTION_logo = 3

image = None
title_start_time = 0.0
frame_ring = 0
frame_logo = 0

image = None

def pause():
    pass

def resume():
    pass

def init():
    global image

    image = load_image('./image/Intro,Menu.png')

def finish():
    global image
    del image

def update():
    # 로고 모드 2초간 지속
    global intro_start_time
    if get_time() - title_start_time > 30.0:
        game_framework.change_mode(play_mode)

    global frame_ring
    frame_ring = (frame_ring + FRAMES_PER_ACTION_ring * ACTION_PER_TIME * game_framework.frame_time) % 4
    global frame_logo
    frame_logo = (frame_logo + FRAMES_PER_ACTION_logo * ACTION_PER_TIME * game_framework.frame_time) % 3
    pass

def draw():
    clear_canvas()
    sxR, syR = sprite_size['ring'][0]
    exR, eyR = sprite_size['ring'][1]

    img_h = image.h  # 이미지 전체 높이
    gap = 20  # 프레임 간격
    clip_x = sxR
    clip_y = img_h - eyR - 1  # top-based y -> bottom-based y 변환
    clip_w = exR - sxR + 1
    clip_h = eyR - syR + 1
    #frame_ring 부분
    # 4프레임
    # 각 프레임은 20 차이
    # image.clip_draw(left, bottom, clip_w, clip_h, 400, 300)
    image.clip_draw(clip_x + clip_w * (int(frame_ring) % 4) + gap * (int(frame_ring) % 4),
                    clip_y,
                    clip_w, clip_h, 400, 300)
    #frame_logo 부분
    sxL, syL = sprite_size['title'][0]
    exL, eyL = sprite_size['title'][1]
    clip_x = sxL
    clip_y = img_h - eyL - 1  # top-based y -> bottom-based y 변환
    clip_w = exL - sxL + 1
    clip_h = eyL - syL + 1
    # 3프레임
    # 각 프레임은 20 차이
    image.clip_draw(clip_x + clip_w * (int(frame_logo) % 3+1) + gap * (int(frame_logo) % 3+1),
                    clip_y,
                    clip_w, clip_h, 400, 300)
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type,event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            game_framework.change_mode(play_mode)