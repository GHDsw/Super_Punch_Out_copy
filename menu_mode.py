# python
import game_framework
from pico2d import *

import play_mode
import train_mode

sprite_size = {'arrow': [[1976, 2992], [1980, 3000]],
               'background': [[1952, 844], [2207, 1067]],
               }

MENU_TITLE = "MENU"
PLAY_TEXT = "PLAY MODE"
TRAIN_TEXT = "TRAINING"

TITLE_POS = (400, 500)
PLAY_POS = (400, 400)
TRAIN_POS = (400, 300)

CHAR_WIDTH_EST = 20  # 글자 폭 추정치(중앙 정렬 계산용)

menu_index = 0  # 0 = PLAY, 1 = TRAIN


# 글자 크기 / 간격 (요구사항)
LETTER_W = 7
LETTER_H = 12
GAPX = 9
GAPY = 4
GAP_MIDDLE = 17

# 그리드 설정 (5 cols x 6 rows), 세트는 가로로 배치 (대문자 | 소문자)
COLS = 5
ROWS = 6
SETS = 2
TOTAL_COLS = COLS * SETS
TOTAL_ROWS = ROWS

# 애니메이션 관련 (기존 값 유지)
TIME_PER_ACTION = 10
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 22

font = None
frame = 0

# 커서 상태: column(0..TOTAL_COLS-1), row(0..ROWS-1) where 0 is 맨 위
arrow_col = 0
arrow_row = 0

# 선택된 글자 (최대 5)
selected = []

def pause():
    pass

def resume():
    pass

def init():
    global alp_image, font, menu_index
    alp_image = load_image('./image/Intro,Menu.png')
    try:
        font = load_font('ENCR10B.TTF', 32)
    except:
        font = None
    menu_index = 0

def finish():
    global alp_image, font
    if alp_image:
        del alp_image
    alp_image = None
    if font:
        del font
    font = None

def update():
    global frame
    frame += 1

def draw():
    clear_canvas()
    # 배경 간단 출력 (있으면)
    if alp_image:
        bsx, bsy = sprite_size['background'][0]
        bex, bey = sprite_size['background'][1]
        img_h = alp_image.h
        b_clip_x = bsx
        b_clip_y = img_h - bey - 1
        b_clip_w = bex - bsx + 1
        b_clip_h = bey - bsy + 1
        alp_image.clip_draw(b_clip_x, b_clip_y, b_clip_w, b_clip_h, 400, 300, 800, 600)

    def draw_centered(text, pos_y, color=(255,255,255)):
        x_center = 400
        w = len(text) * CHAR_WIDTH_EST
        start_x = x_center - w / 2
        if font:
            font.draw(start_x, pos_y, text, color)
        else:
            # 폰트 없을 때는 사각형으로 대체
            for i, ch in enumerate(text):
                draw_rectangle(start_x + i*CHAR_WIDTH_EST - 8, pos_y - 8, start_x + i*CHAR_WIDTH_EST + 8, pos_y + 8)

        return start_x

    # 제목
    draw_centered(MENU_TITLE, TITLE_POS[1], (255, 255, 0))

    # 항목들
    play_start_x = draw_centered(PLAY_TEXT, PLAY_POS[1], (255,255,255))
    train_start_x = draw_centered(TRAIN_TEXT, TRAIN_POS[1], (255,255,255))

    # 화살표 위치: 텍스트의 왼쪽, 약간 여유를 둠
    arrow_offset = -30
    arrow_y = PLAY_POS[1] if menu_index == 0 else TRAIN_POS[1]
    # 화살표는 '>' 문자로 그리거나 없으면 사각형으로 대체
    arrow_x = (play_start_x + arrow_offset) if menu_index == 0 else (train_start_x + arrow_offset)
    if font:
        font.draw(arrow_x, arrow_y, ">", (255, 200, 0))
    else:
        draw_rectangle(arrow_x - 8, arrow_y - 8, arrow_x + 8, arrow_y + 8)

    update_canvas()

def handle_events():
    global menu_index
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_UP:
                menu_index = max(0, menu_index - 1)
            elif event.key == SDLK_DOWN:
                menu_index = min(1, menu_index + 1)
            elif event.key == SDLK_SPACE:
                if menu_index == 0:
                    game_framework.change_mode(play_mode)
                else:
                    game_framework.change_mode(train_mode)

