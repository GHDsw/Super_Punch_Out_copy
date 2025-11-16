import random
import math
import game_framework
import game_world

from pico2d import *
from state_machine import StateMachine

time_out = lambda e: e[0] == 'TIMEOUT'

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

class IDLE:
    def __init__(self):
        pass

    def enter(self):
        pass

    def exit(self):
        pass

    def do(self):
        pass

    def draw(self):
        pass


class MOVE:
    def __init__(self):
        pass

    def enter(self):
        pass

    def exit(self):
        pass

    def do(self):
        pass

    def draw(self):
        pass


class ATTACK:
    def __init__(self):
        pass

    def enter(self):
        pass

    def exit(self):
        pass

    def do(self):
        pass

    def draw(self):
        pass


class Enemy:
    def __init__(self):
        self.IDLE = None
        self.x, self.y = 400, 500
        self.image = load_image('./image/Gabby_Jay.png')
        self.frame = random.randint(0, 9)
        self.dir = random.choice([-1,1])
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {up_down: self.IDLE, up_up: self.IDLE, down_down: self.IDLE, down_up: self.IDLE,
                            z_down: self.ATTACK, x_down: self.ATTACK,
                            time_out: self.IDLE,
                            right_down: self.MOVE, left_down: self.MOVE},
                self.MOVE: {right_up: self.MOVE, left_up: self.MOVE,
                            right_down: self.MOVE, left_down: self.MOVE,
                            Return: self.IDLE
                            },
                self.ATTACK: {time_out: self.IDLE}
            }
        )


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