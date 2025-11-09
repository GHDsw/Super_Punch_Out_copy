from pico2d import *
import game_framework

import game_world

sprite_size = {'ring1': [[0, 0], [431, 175]],
               'ring2': [[0, 256], [431, 431]],
               'ring3': [[0, 512], [431, 687]],
               'ring4': [[0, 768], [431, 944]],
               }

TIME_PER_ACTION = 1
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

image = None

class Rings:
    def __init__(self):

        self.image = load_image('./image/Boxing_Rings.png')
        self.frame = 0

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        pass

    def draw(self):
        ring_num = 3

        sx, sy = sprite_size['ring1'][0]
        ex, ey = sprite_size['ring1'][1]

        img_h = self.image.h  # 이미지 전체 높이
        gap = 80  # 프레임 간격
        x_gap = 6
        clip_x = sx
        clip_y = img_h - ey - 1  # top-based y -> bottom-based y 변환
        clip_w = ex - sx + 1
        clip_h = ey - sy + 1
        #4프레임, 80 차이
        self.image.clip_draw(clip_x + clip_w * ring_num + x_gap * ring_num,
                        clip_y - (clip_h * (int(self.frame) % 4) + gap * (int(self.frame) % 4)),
                        clip_w, clip_h, 400, 300)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return 0, 0, 1600-1, 60

    def handle_collision(self, group, other):
        pass