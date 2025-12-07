# python
import game_framework
from pico2d import *
import os
import string

import play_mode

sprite_size = {'alphabet_table': [[1690, 2845], [1849, 2952]],
               'a': [[1690, 2845], [1996, 2856]],
               'arrow': [[1976, 2992], [1980, 3000]],
               'background': [[1952, 844], [2207, 1067]],
               }

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

alp_image = None
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
    global alp_image, font, arrow_col, arrow_row, selected
    alp_image = load_image('./image/Intro,Menu.png')
    try:
        font = load_font('ENCR10B.TTF', 32)
    except:
        font = None
    arrow_col = 0
    arrow_row = 0
    selected = []

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
    bsx, bsy = sprite_size['background'][0]
    bex, bey = sprite_size['background'][1]
    img_h = alp_image.h
    b_clip_x = bsx
    b_clip_y = img_h - bey - 1
    b_clip_w = bex - bsx + 1
    b_clip_h = bey - bsy + 1
    # 배경은 화면 전체(800x600)로 그리기
    alp_image.clip_draw(b_clip_x, b_clip_y, b_clip_w, b_clip_h, 400, 300, 800, 600)


    sx, sy = sprite_size['alphabet_table'][0]
    ex, ey = sprite_size['alphabet_table'][1]

    img_h = alp_image.h
    clip_x = sx
    clip_y = img_h - ey - 1  # top-based y -> bottom-based y
    clip_w = ex - sx + 1
    clip_h = ey - sy + 1

    # 화면에 테이블을 중앙에 그림 (원본과 동일 비율)
    dest_center_x = 400
    dest_center_y = 300
    scale_img = 3  # 원본과 동일하게 3배로 확대
    alp_image.clip_draw(clip_x, clip_y, clip_w, clip_h, dest_center_x, dest_center_y, clip_w * scale_img, clip_h * scale_img)

    # 테이블의 왼쪽 하단(화면 좌표)
    table_left = dest_center_x - (clip_w * scale_img) / 2
    table_bottom = dest_center_y - (clip_h * scale_img) / 2

    # 소스(클립 영역)에서의 레이아웃 계산 (top-based)
    set_width_src = COLS * LETTER_W + (COLS - 1) * GAPX
    total_src_width = SETS * set_width_src + GAP_MIDDLE
    total_src_height = ROWS * LETTER_H + (ROWS - 1) * GAPY

    # arrow 위치 계산 (세트가 가로로 배치됨)
    set_index = arrow_col // COLS  # 0 = 대문자, 1 = 소문자
    col_in_set = arrow_col % COLS
    row_in_set = arrow_row  # 0..ROWS-1

    # 소스 내에서의 중심 좌표 (left 기준, top 기준)
    x_from_left = set_index * (set_width_src + GAP_MIDDLE) + col_in_set * (LETTER_W + GAPX) + LETTER_W / 2.0
    y_from_top = row_in_set * (LETTER_H + GAPY) + LETTER_H / 2.0

    # top-based -> bottom-based 변환
    y_from_bottom = clip_h - y_from_top

    # 화면 좌표로 변환
    arrow_x = table_left + x_from_left * scale_img - 7 * scale_img  # 화살표 이미지 폭 고려
    arrow_y = table_bottom + y_from_bottom * scale_img

    # 화살표 클립 정보 및 그리기
    asx, asy = sprite_size['arrow'][0]
    aex, aey = sprite_size['arrow'][1]
    a_img_h = alp_image.h
    a_clip_x = asx
    a_clip_y = a_img_h - aey - 1
    a_clip_w = aex - asx + 1
    a_clip_h = aey - asy + 1

    alp_image.clip_draw(a_clip_x, a_clip_y, a_clip_w, a_clip_h, arrow_x, arrow_y, a_clip_w * scale_img, a_clip_h * scale_img)

    # 선택된 글자 표시 (상단 중앙)
    display_y = 530
    selected_str = ''.join(selected)
    if font:
        total_width = len(selected_str) * 24
        start_x = 400 - total_width / 2
        for i, ch in enumerate(selected_str):
            font.draw(start_x + i * 24, display_y, ch, (255, 255, 255))
    else:
        total_width = len(selected_str) * 24
        start_x = 400 - total_width / 2
        for i, ch in enumerate(selected_str):
            draw_rectangle(start_x + i * 24 - 10, display_y - 10, start_x + i * 24 + 10, display_y + 10)

    update_canvas()

# python
def save_selected_to_file():
    global selected
    try:
        path = os.path.join(os.getcwd(), 'record.txt')
        with open(path, 'a', encoding='utf-8') as f:
            f.write(''.join(selected) + ' ')
    except Exception as e:
        print('Failed to save selected alphabets:', e)

def handle_events():
    global arrow_col, arrow_row, selected
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif(event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            if selected:
                save_selected_to_file()
                game_framework.change_mode(play_mode)
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_LEFT:
                arrow_col = max(0, arrow_col - 1)
            elif event.key == SDLK_RIGHT:
                arrow_col = min(TOTAL_COLS - 1, arrow_col + 1)
            elif event.key == SDLK_UP:
                arrow_row = max(0, arrow_row - 1)
            elif event.key == SDLK_DOWN:
                arrow_row = min(TOTAL_ROWS - 1, arrow_row + 1)
            elif event.key == SDLK_z:
                set_idx = arrow_col // COLS
                col_in_set = arrow_col % COLS
                idx_in_set = arrow_row * COLS + col_in_set
                if idx_in_set < 26 and len(selected) < 5:
                    if set_idx == 0:
                        selected.append(string.ascii_uppercase[idx_in_set])
                    else:
                        selected.append(string.ascii_lowercase[idx_in_set])
            elif event.key == SDLK_x:
                if selected:
                    selected.pop()

