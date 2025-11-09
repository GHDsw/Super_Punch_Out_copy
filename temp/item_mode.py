import game_framework
import game_world
from pico2d import *

import play_mode
from pannel import Pannel

pannel = None

def pause():
    pass

def resume():
    pass

def init():
    global pannel

    pannel = Pannel()
    game_world.add_object(pannel, 2)

def finish():
    game_world.remove_object(pannel)
    pass

def update():
    game_world.update()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.pop_mode()
            elif event.key == SDLK_0:
                play_mode.boy.item=None
                game_framework.pop_mode()
            elif event.key == SDLK_1:
                play_mode.boy.item='Ball'
                game_framework.pop_mode()
            elif event.key == SDLK_2:
                play_mode.boy.item='BigBall'
                game_framework.pop_mode()