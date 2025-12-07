# python
import os
import game_framework
from pico2d import *
import re

import intro_mode

sprite_size = {
               'a': [[1690, 2845], [1996, 2856]],
               'background': [[1952, 844], [2207, 1067]],
               }

TIME_PER_ACTION = 10
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 22

image = None
frame = 0

font = None
lines = []

def pause():
    pass

def resume():
    pass

def _load_sorted_and_trim_records(path, max_entries=10):
    """
    `recode.txt`를 읽어
    - 각 라인을 공백으로 분리하여 마지막 토큰을 `recode`로 간주
    - recode가 숫자가 아니면 해당 라인 버림
    - recode 기준 내림차순 정렬, 동점일 경우 ID(문자열) 내림차순
    - 상위 `max_entries`만 파일에 덮어쓰기 저장하고 그 리스트를 반환
    """
    parsed = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for raw_line in f.read().splitlines():
                line = raw_line.strip()
                if not line:
                    continue
                tokens = line.split()
                if len(tokens) < 2:
                    # recode가 없는 라인 -> 무시
                    continue
                rec_token = tokens[-1]
                id_token = ' '.join(tokens[:-1])
                try:
                    val = float(rec_token)
                    parsed.append((val, id_token))
                except ValueError:
                    # recode가 숫자가 아니면 무시
                    continue
    except Exception:
        return []

    # recode(수치) 내림차순, 동점이면 ID 내림차순
    parsed.sort(key=lambda x: (x[0], x[1]), reverse=True)

    # 상위 max_entries만 보존
    top = parsed[:max_entries]

    # 파일에 덮어쓰기: "ID recode" 형식으로 저장
    try:
        with open(path, 'w', encoding='utf-8') as f:
            out_lines = []
            for val, id_str in top:
                # 정수면 정수 형태로, 아니면 소수 형태로 저장
                if float(val).is_integer():
                    rec_str = str(int(val))
                else:
                    rec_str = str(val)
                out_line = f"{id_str} {rec_str}"
                out_lines.append(out_line)
                f.write(out_line + "\n")
    except Exception:
        # 쓰기 실패 시에는 그냥 표시용 리스트만 리턴
        out_lines = [f"{id_str} {int(val) if float(val).is_integer() else val}" for val, id_str in top]

    return out_lines


def init():
    global image, font, lines
    image = load_image('./image/Intro,Menu.png')
    try:
        font = load_font('ENCR10B.TTF', 16)
    except:
        font = None
    try:
        path = os.path.join(os.getcwd(), 'record.txt')  # 파일명은 `recode.txt`
        lines = _load_sorted_and_trim_records(path, max_entries=10)
    except Exception:
        lines = []

def finish():
    global image, font
    if image:
        del image
    image = None
    if font:
        del font
    font = None

def update():
    global frame
    frame += 1

def draw():
    global image
    clear_canvas()

    bsx, bsy = sprite_size['background'][0]
    bex, bey = sprite_size['background'][1]
    img_h = image.h
    b_clip_x = bsx
    b_clip_y = img_h - bey - 1
    b_clip_w = bex - bsx + 1
    b_clip_h = bey - bsy + 1
    # 배경은 화면 전체(800x600)로 그리기
    image.clip_draw(b_clip_x, b_clip_y, b_clip_w, b_clip_h, 400, 300, 800, 600)

    # 중심 좌표
    cx, cy = 400, 300

    # 화면에 이미지나 배경이 필요하면 여기 그리기 (선택)
    # image.clip_draw( ... )  # 필요 시 사용

    # 텍스트 블록 중앙 정렬하여 그리기
    line_count = len(lines)
    if line_count == 0:
        # 파일이 비어있으면 안내 텍스트
        msg = 'No records'
        if font:
            w = len(msg) * 16
            font.draw(cx - w / 2, cy, msg, (255, 255, 255))
        else:
            draw_rectangle(cx - 60, cy - 10, cx + 60, cy + 10)
    else:
        char_width = 16    # 문자당 대략 폭 (폰트가 없을 때도 일관되게 계산)
        line_spacing = 30  # 줄 간격
        total_height = line_count * line_spacing
        start_y = cy + (total_height / 2) - (line_spacing / 2)
        for i, line in enumerate(lines):
            y = start_y - i * line_spacing
            if font:
                # 간단한 가로 중앙 정렬 (문자 폭 추정)
                x = cx - (len(line) * char_width) / 2
                font.draw(x, y, line, (255, 255, 255))
            else:
                x = cx - (len(line) * char_width) / 2
                # 폰트가 없으면 사각형으로 대체 (시각 확인용)
                draw_rectangle(x - 8, y - 8, x + len(line) * char_width + 8, y + 8)

    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            game_framework.change_mode(intro_mode)
            # 선택 저장 함수가 game_framework나 다른 모듈에 있으면 필요 시 호출
