import random
from pico2d import *

import game_framework
import game_world
import result_mode

from boy import Boy
from rings import Rings
from enemy import Enemy

boy = None
enemy = None

start_time = 0.0

def handle_events():
    global start_time
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            record = get_time() - start_time
            game_framework.save_record_to_file(record)
            game_framework.change_mode(result_mode)
        else:
            boy.handle_event(event)

def init():
    global boy
    global enemy
    global start_time
    #global balls
    # global zombies

    rings = Rings()
    game_world.add_object(rings, 0)
    #game_world.add_collision_pair('grass:ball', rings, None)

    boy = Boy()
    game_world.add_object(boy, 2)

    enemy = Enemy()
    game_world.add_object(enemy, 1)

    game_world.add_collision_pair('boy:enemy', boy, None)

    start_time = get_time()

    # balls = [Ball(random.randint(100, 1600-100), 60,0) for i in range(30)]
    # game_world.add_objects(balls, 1)
    # game_world.add_collision_pair('boy:zombie', boy, None)

    #boy와 ball 사이의 충돌 검사가 필요하다는 정보 추가
    # game_world.add_collision_pair('boy:ball',boy, None)
    # for ball in balls:
    #     if ball.y > 60:
    #         game_world.add_collision_pair('zombie:ball', None, ball)
    #     else:
    #         game_world.add_collision_pair('boy:ball', None, ball)

    # zombies = [Zombie() for i in range(4)]
    # game_world.add_objects(zombies, 1)
    #
    # for zombie in zombies:
    #     game_world.add_collision_pair('zombie:ball', zombie, None)
    #     game_world.add_collision_pair('boy:zombie', None, zombie)


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

