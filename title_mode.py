import game_framework
from pico2d import *

import account_resist_mode

sprite_size = {'ring': [[1124, 66], [1379, 289]],
               'title': [[20, 66], [275,289]],
               }

TIME_PER_ACTION = 1
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION_ring = 8
FRAMES_PER_ACTION_logo = 3

MENU_TITLE = "PRESS SPACE"
TITLE_POS = (400, 100)
CHAR_WIDTH_EST = 20  # 글자 폭 추정치(중앙 정렬 계산용)

image = None
font = None

title_start_time = 0.0
frame_ring = 0
frame_logo = 0

image = None
bgm = None

def pause():
    pass

def resume():
    pass

def init():
    global image, bgm, font
    image = load_image('./image/Intro,Menu.png')
    bgm = load_music('./audio/Title.wav')
    bgm.set_volume(32)
    bgm.play()
    try:
        font = load_font('ENCR10B.TTF', 32)
    except:
        font = None

def finish():
    global image, font
    del image
    if font is not None:
        del font
        font = None

def update():
    # 로고 모드 2초간 지속
    global intro_start_time
    # if get_time() - title_start_time > 30.0:
    #     game_framework.change_mode(account_resist_mode)

    global frame_ring
    frame_ring = (frame_ring + FRAMES_PER_ACTION_ring * ACTION_PER_TIME * game_framework.frame_time) % 4
    global frame_logo
    frame_logo = (frame_logo + FRAMES_PER_ACTION_logo * ACTION_PER_TIME * game_framework.frame_time) % 3
    pass

def draw():
    global font
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
                    clip_w, clip_h, 400, 300, 800, 600)
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
                    clip_w, clip_h, 400,300, 800, 600)

    def draw_centered(text, pos_y, color=(255, 255, 255)):
        x_center = 400
        w = len(text) * CHAR_WIDTH_EST
        start_x = x_center - w / 2
        if font:
            font.draw(start_x, pos_y, text, color)
        else:
            # 폰트 없을 때는 사각형으로 대체
            for i, ch in enumerate(text):
                draw_rectangle(start_x + i * CHAR_WIDTH_EST - 8, pos_y - 8, start_x + i * CHAR_WIDTH_EST + 8, pos_y + 8)

        return start_x

    # 제목
    draw_centered(MENU_TITLE, TITLE_POS[1], (255, 255, 0))

    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type,event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            game_framework.change_mode(account_resist_mode)