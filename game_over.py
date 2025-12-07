# python
import game_framework
from pico2d import *
import result_mode

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
    global image, font, lines
    image = load_image('./image/game_over.png')

def finish():
    global image
    if image:
        del image
    image = None

def update():
    global frame
    frame += 1

def draw():
    global image
    clear_canvas()

    img_h = image.h
    # 배경은 화면 전체(800x600)로 그리기
    image.clip_draw(0, 0, 759, 554, 400, 300, 800, 600)

    # 중심 좌표
    cx, cy = 400, 300

    # 화면에 이미지나 배경이 필요하면 여기 그리기 (선택)
    # image.clip_draw( ... )  # 필요 시 사용
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            game_framework.change_mode(result_mode)
            # 선택 저장 함수가 game_framework나 다른 모듈에 있으면 필요 시 호출
