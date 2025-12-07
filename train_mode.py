import random
from pico2d import *

import game_framework
import game_world
import intro_mode

from state_bar import State_bar
from boy import Boy
from rings import Rings
import common
from trainer import Enemy

start_time = 0.0
bgm = None

def handle_events():
    global start_time
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.change_mode(intro_mode)
            common.enemy.hp = 0
        if event.type == SDL_KEYDOWN and event.key == SDLK_p:
            common.boy.hp = 0
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            common.boy.handle_event(event)

def init():
    global state_bar
    global start_time, bgm

    bgm = load_music('./audio/Battle.wav')
    bgm.set_volume(32)
    bgm.repeat_play()

    rings = Rings()
    game_world.add_object(rings, 0)

    common.boy = Boy()
    game_world.add_object(common.boy, 3)

    common.enemy = Enemy()
    game_world.add_object(common.enemy, 2)

    state_bar = State_bar()
    game_world.add_object(state_bar, 1)

    start_time = get_time()

def update():
    game_world.update()
    game_world.handle_collision()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    game_world.clear()

def pause(): pass
def resume(): pass

