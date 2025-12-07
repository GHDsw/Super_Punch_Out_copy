from pico2d import *

import game_framework
import common

sprite_size = {'state_bar': [[2049, 2760], [2288, 2791]],
               'little_mac': [[1805, 2721], [1834, 2750]],
               'gabby_jay': [[1937, 1199], [1966, 1228]],#70*94
               }

TIME_PER_ACTION = 1
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

image = None

def fill_rectangle(x, y, w, h, color=(255, 0, 0)):
    w = max(0, int(w))
    h = max(0, int(h))
    if w == 0 or h == 0:
        return
    for i in range(w):
        draw_rectangle(x + i, y, x + i + 1, y + h)
    # 테두리 그리기
    draw_rectangle(x - 1, y - 1, x + w + 1, y + h + 1)

class State_bar:
    def __init__(self):

        self.image = load_image('./image/Intro,Menu.png')
        self.frame = 0
        self.img_h = self.image.h  # 이미지 전체 높이
        self.boy_hp = self.boy_maxhp = common.boy.hp
        self.enemy_hp = self.enemy_maxhp = common.enemy.hp

    def update(self):
        #self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        self.boy_hp = common.boy.hp
        self.enemy_hp = common.enemy.hp
        pass

    def draw(self):
        sx, sy = sprite_size['state_bar'][0]
        ex, ey = sprite_size['state_bar'][1]
        clip_x, clip_y, clip_w, clip_h = game_framework.carculate_image_position(self, sx, sy, ex, ey)
        self.image.clip_draw(clip_x,clip_y,clip_w, clip_h, 400, 550, clip_w*3, clip_h*3)

        sx, sy = sprite_size['little_mac'][0]
        ex, ey = sprite_size['little_mac'][1]
        clip_x, clip_y, clip_w, clip_h = game_framework.carculate_image_position(self, sx, sy, ex, ey)
        self.image.clip_draw(clip_x, clip_y, clip_w, clip_h, 100, 550, clip_w * 3, clip_h * 3)

        sx, sy = sprite_size['gabby_jay'][0]
        ex, ey = sprite_size['gabby_jay'][1]
        clip_x, clip_y, clip_w, clip_h = game_framework.carculate_image_position(self, sx, sy, ex, ey)
        self.image.clip_draw(clip_x, clip_y, clip_w, clip_h, 700, 550, clip_w * 3, clip_h * 3)

        #  draw boy_hp bar (녹색)
        bw = self.boy_hp // 7
        bw = max(0, min(bw, 230))  # 최대 너비 제한(필요 시 조정)
        fill_rectangle(145, 510, bw, 30, color=(0, 200, 0))

        #  draw enemy_hp bar (빨강)
        ew = self.enemy_hp // 7
        ew = max(0, min(ew, 230))
        fill_rectangle(425, 510, ew, 30, color=(200, 0, 0))

    # def get_bb(self):
    #     return 0, 0, 1600-1, 60

    def handle_collision(self, group, other):
        pass