import random
import math
import game_framework
import game_world

from pico2d import *

# zombie Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10.0

sprite_size = {
    #임시 이미지
    'IDEL': [[0, 0], [74, 173]], 'move': [[384, 0], [462, 170]], 'hit': [[0, 1597], [68, 1773]], 'atk': [[84, 365], [153, 530]], 'def': [[0, 0], [0, 0]],
    

    '1': [[0, 0], [0, 0]], '2': [[0, 0], [0, 0]], '3': [[0, 0], [0, 0]], '4': [[0, 0], [0, 0]], '5': [[0, 0], [0, 0]], '6': [[0, 0],[0, 0]],

    '1': [[0, 0], [0, 0]], '2': [[0, 0], [0, 0]],

    '1': [[0, 0], [0, 0]], '2': [[0, 0], [0, 0]],

    '1': [[0, 0], [0, 0]], '2': [[0, 0], [0, 0]], '3': [[0, 0], [0, 0]],

    '1': [[0, 0], [0, 0]], '2': [[0, 0], [0, 0]], '3': [[0, 0], [0, 0]],

    '1': [[0, 0], [0, 0]], '2': [[0, 0], [0, 0]], '3': [[0, 0], [0, 0]], '4': [[0, 0], [0, 0]], '5': [[0, 0], [0, 0]], '6': [[0, 0], [0, 0]],

    '1': [[0, 0], [0, 0]], '2': [[0, 0], [0, 0]],

    '1': [[0, 0], [0, 0]], '2': [[0, 0], [0, 0]],

    '1': [[0, 0], [0, 0]], '2': [[0, 0], [0, 0]], '3': [[0, 0], [0, 0]], '4': [[0, 0], [0, 0]], '5': [[0, 0], [0, 0]], '6': [[0, 0], [0, 0]],

    '1': [[0, 0], [0, 0]], '2': [[0, 0], [0, 0]], '3': [[0, 0], [0, 0]], '4': [[0, 0], [0, 0]], '5': [[0, 0], [0, 0]], '6': [[0, 0], [0, 0]],

    '1': [[0, 0], [0, 0]], '2': [[0, 0], [0, 0]], '3': [[0, 0], [0, 0]], '4': [[0, 0], [0, 0]], '5': [[0, 0], [0, 0]]
}

class Enemy:
    def __init__(self):
        self.x, self.y = 400, 500
        self.image = load_image('./image/Gabby_Jay.png')
        self.frame = random.randint(0, 9)
        self.dir = random.choice([-1,1])


    def get_bb(self):
        return self.x - 100, self.y - 100, self.x + 100, self.y + 100

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time
        if self.x > 1600:
            self.dir = -1
        elif self.x < 800:
            self.dir = 1
        self.x = clamp(800, self.x, 1600)
        pass


    def draw(self):
        if self.dir < 0:
            self.image.composite_draw(0, 'h', self.x, self.y, self.size, self.size)
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        if group == 'Enemy:boy' and other.stopped is False:
            if self.attack_cnt == 1:
                game_world.remove_object(self)
            else:
                self.attack_cnt -= 1
                self.size = 100 * self.attack_cnt
                self.y -= 50
        if group == 'boy:Enemy':
            pass