from pico2d import *
import game_framework
import common

import math

sprite_size = {'ring1': [[0, 0], [431, 175]],
               'ring2': [[0, 256], [431, 431]],
               'ring3': [[0, 512], [431, 687]],
               'ring4': [[0, 768], [431, 944]],
               }

TIME_PER_ACTION = 1
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

PIXEL_PER_METER = (100.0 / 0.1)  # 10 pixel 1 cm
MOVE_SPEED_KMPH = 5.0  # Km / Hour
MOVE_SPEED_MPM = (MOVE_SPEED_KMPH * 1000.0 / 60.0)
MOVE_SPEED_MPS = (MOVE_SPEED_MPM / 60.0)
MOVE_SPEED_PPS = (MOVE_SPEED_MPS * PIXEL_PER_METER)

image = None

class Rings:
    def __init__(self):

        self.image = load_image('./image/Boxing_Rings.png')
        self.frame = 0
        self.x, self.y = self.start_x, self.start_y = self.origin_x, self.origin_y = 400, 300
        self.t = 0.0
        self.distance = math.sqrt((self.x - 1280) ** 2 + (self.y - 1024) ** 2)
        self.return_origin = False
        self.dir = 0

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        if common.enemy.state == 'Revive':
            if self.t < 1.0:
                # self.pos = (1.0 - self.t) * self.start_pos + self.t * self.end_pos
                self.t += MOVE_SPEED_PPS * game_framework.frame_time / self.distance
                self.x = (1.0 - self.t) * self.start_x + self.t * (self.origin_x)
            else:
                self.x = self.start_x = self.origin_x
                self.t = 0.0
                self.frame = 0
        if common.enemy.state == 'Hit':
            if self.x >= self.origin_x - 250 and self.x <= self.origin_x + 250:
                self.x += 0.5 * common.boy.ATTACK.atk_dir
            elif self.x > self.origin_x + 250:
                self.x = self.origin_x + 250
            elif self.x < self.origin_x - 250:
                self.x = self.origin_x - 250
            self.start_x = self.x
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
                        clip_w, clip_h, self.x, self.y, clip_w*3.4, clip_h*3.4)
        #draw_rectangle(*self.get_bb())

    # def get_bb(self):
    #     return 0, 0, 1600-1, 60

    def handle_collision(self, group, other):
        pass