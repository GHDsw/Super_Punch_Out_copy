import game_framework
from pico2d import *

import title_mode

sprite_size = {'intro': [[0, 0], [0, 0]],
               }

image = None
intro_start_time = 0.0

def pause():
    pass

def resume():
    pass

def init():
    global image, intro_start_time

    image = load_image('./image/Intro, Ending, Menus, Fonts.png')
    intro_start_time = get_time()

def finish():
    global image
    del image

def update():
    #로고 모드 2초간 지속
    global intro_start_time
    if get_time() - intro_start_time > 2.0:
        game_framework.change_mode(title_mode)

def draw():
    clear_canvas()
    image.draw(400, 300)
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            game_framework.change_mode(title_mode)