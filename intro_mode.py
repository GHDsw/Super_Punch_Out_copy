import game_framework
from pico2d import *

import title_mode

image = None
intro_start_time = 0.0

def pause():
    pass

def resume():
    pass

def init():
    global image, intro_start_time

    image = load_image('test_intro.png')
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
    #딱히 동작도 안하는데 입력을 받는 이유
    #pico2d가 내부적으로 이벤트 큐를 관리하기 때문에
    #이벤트 큐가 쌓이지 않도록 주기적으로 비워줘야 한다
    events = get_events()