import random
import math
import game_framework
import game_world

from pico2d import *
from state_machine import StateMachine

time_out = lambda e: e[0] == 'TIMEOUT'
event_end = lambda e: e[0] == 'EVENT_END'
event_move = lambda e: e[0] == 'EVENT_MOVE'
event_hit = lambda e: e[0] == 'EVENT_HIT'
event_attack = lambda e: e[0] == 'EVENT_ATTACK'

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
    'Idle': [[0, 0], [74, 173]], 'Move': [[384, 0], [462, 170]], 'Hit': [[0, 1597], [68, 1773]], 'Atk': [[84, 365], [153, 530]], 'Def': [[0, 0], [0, 0]],
    

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

class Idle:
    def __init__(self, enemy):
        self.enemy = enemy

    def enter(self, e):
        sx, sy = sprite_size['Idle'][0]
        ex, ey = sprite_size['Idle'][1]

        self.enemy.clip_x = sx
        self.enemy.clip_y = self.enemy.image.h - ey - 1  # top-based y -> bottom-based y 변환
        self.enemy.clip_w = ex - sx + 1
        self.enemy.clip_h = ey - sy + 1
        pass

    def exit(self):
        pass

    def do(self):
        pass

    def draw(self):
        self.enemy.image.clip_draw(self.enemy.clip_x, self.enemy.clip_y, self.enemy.clip_w, self.enemy.clip_h, self.enemy.x,self.enemy.y)


class Move:
    def __init__(self, enemy):
        self.enemy = enemy

    def enter(self):
        pass

    def exit(self):
        pass

    def do(self):
        pass

    def draw(self):
        pass


class Attack:
    def __init__(self, enemy):
        self.enemy = enemy

    def enter(self):
        pass

    def exit(self):
        pass

    def do(self):
        pass

    def draw(self):
        pass


class Hit:
    def __init__(self, enemy):
        self.enemy = enemy

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


        self.x, self.y = 400, 300
        self.image = load_image('./image/Gabby_Jay.png')
        self.frame = random.randint(0, 9)
        self.dir = random.choice([-1,1])

        self.clip_x = 0
        self.clip_y = 0
        self.clip_w = 0
        self.clip_h = 0

        self.hp = 10

        self.IDLE = Idle(self)
        self.MOVE = Move(self)
        self.ATTACK = Attack(self)
        self.HIT = Hit(self)

        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {time_out: self.IDLE,
                            },
                self.MOVE: {event_end: self.IDLE
                            },
                self.ATTACK: {event_end: self.IDLE
                              },
                self.HIT: {time_out: self.IDLE, event_end: self.IDLE
                }
            }

        )


    def get_bb(self):
        return self.x - 100, self.y - 100, self.x + 100, self.y + 100

    def update(self):
        # self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        # self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time
        # if self.x > 1600:
        #     self.dir = -1
        # elif self.x < 800:
        #     self.dir = 1
        # self.x = clamp(800, self.x, 1600)
        self.state_machine.update()
        pass


    def draw(self):
        self.state_machine.draw()
        # if self.dir < 0:
        #     self.image.composite_draw(0, 'h', self.x, self.y, self.size, self.size)
        draw_rectangle(*self.get_bb())
        pass

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        if group == 'boy:enemy':
            self.hp -= 10
    #     if group == 'Enemy:boy' and other.stopped is False:
    #         if self.attack_cnt == 1:
    #             game_world.remove_object(self)
    #         else:
    #             self.attack_cnt -= 1
    #             self.size = 100 * self.attack_cnt
    #             self.y -= 50
    #     if group == 'boy:Enemy':
    #         pass