from pico2d import *
#load_image, get_time, load_font
import math

import game_world
import game_framework

import game_world

sprite_size = {'state_bar': [[2049, 2760], [2288, 2791]],
               'little_mac': [[1805, 2721], [1834, 2750]],
               'gabby_jay': [[1937, 1199], [1966, 1228]],#70*94
               }

TIME_PER_ACTION = 1
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

image = None

class State_bar:
    def __init__(self):

        self.image = load_image('./image/Intro,Menu.png')
        self.frame = 0

    def update(self):
        #self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        pass

    def draw(self):
        ring_num = 3

        sx, sy = sprite_size['state_bar'][0]
        ex, ey = sprite_size['state_bar'][1]

        img_h = self.image.h  # 이미지 전체 높이
        gap = 80  # 프레임 간격
        x_gap = 6
        clip_x = sx
        clip_y = img_h - ey - 1  # top-based y -> bottom-based y 변환
        clip_w = ex - sx + 1
        clip_h = ey - sy + 1
        #4프레임, 80 차이
        self.image.clip_draw(clip_x,clip_y,clip_w, clip_h, 400, 550, clip_w*3, clip_h*3)
        #draw_rectangle(*self.get_bb())

    # def get_bb(self):
    #     return 0, 0, 1600-1, 60

    def handle_collision(self, group, other):
        pass