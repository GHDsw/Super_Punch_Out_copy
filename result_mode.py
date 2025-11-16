# python
import os
import game_framework
from pico2d import *
import re

import intro_mode

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

def _load_sorted_records_by_record(path):
    """
    각 라인에서 '첫 번째 공백 문자 이후'부터 숫자를 찾아 파싱.
    - 공백이 있으면 공백 뒤 부분에서 숫자를 검색
    - 공백이 없으면 전체 라인에서 숫자를 검색 (기존 동작 보존)
    숫자가 있으면 숫자 기준 내림차순, 없으면 문자열 기준 내림차순으로 반환
    """
    numeric = []
    non_numeric = []
    num_re = re.compile(r'([0-9]+(?:\.[0-9]+)?)')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for raw_line in f.read().splitlines():
                line = raw_line  # 원문 보존
                # 첫 공백 이후를 검색 영역으로 설정
                m_space = re.search(r'\s', line)
                if m_space:
                    search_area = line[m_space.end():]  # 첫 공백 문자 다음부터
                else:
                    search_area = line  # 공백 없으면 전체 라인
                m = num_re.search(search_area)
                if m:
                    try:
                        val = float(m.group(1))
                        numeric.append((val, line))
                    except Exception:
                        non_numeric.append(line)
                else:
                    non_numeric.append(line)
    except Exception:
        return []

    numeric.sort(key=lambda x: x[0], reverse=True)
    non_numeric.sort(reverse=True)
    return [line for _, line in numeric] + non_numeric

def init():
    global image, font, lines
    image = load_image('./image/Intro,Menu.png')
    try:
        font = load_font('ENCR10B.TTF', 16)
    except:
        font = None
    try:
        path = os.path.join(os.getcwd(), 'record.txt')
        lines = _load_sorted_records_by_record(path)
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
    clear_canvas()

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
