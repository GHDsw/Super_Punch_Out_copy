from pico2d import load_image, get_time, load_font, draw_rectangle
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_UP, SDLK_DOWN, SDLK_z, SDLK_x
import math
import common

import game_world
import game_framework
from game_framework import carculate_image_position
import result_mode

from state_machine import StateMachine


def space_down(e): # e is space down ?
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

time_out = lambda e: e[0] == 'TIMEOUT'

done = lambda e: e[0] == 'DONE'
up_done = lambda e: e[0] == 'UP_DONE'

win = lambda e: e[0] == 'WIN'
hit = lambda e: e[0] == 'HIT'

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT

def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT

def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT

def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

def up_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP

def up_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_UP

def down_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN

def down_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_DOWN

def z_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_z

def x_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_x

# Boy의 Run Speed 계산

# Boy Run Speed
PIXEL_PER_METER = (100.0 / 0.1)  # 10 pixel 1 cm
MOVE_SPEED_KMPH = 20.0  # Km / Hour
MOVE_SPEED_MPM = (MOVE_SPEED_KMPH * 1000.0 / 60.0)
MOVE_SPEED_MPS = (MOVE_SPEED_MPM / 60.0)
MOVE_SPEED_PPS = (MOVE_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
TIME_PER_ACTION = 0.25
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 1

# x1, y1, x2, y2
sprite_size = {
    'IDle': [[154, 395], [225, 538]], 'guard': [[8, 145], [71, 248]], 'backstep': [[130, 145], [209, 248]],
    # 무브 원투 바뀜 펼쳐지며 회피가 아니라 돌아오며 접히는거였음
    # 어쩐지 각도 작은게 오른쪽에 있더라 젠장
    'Move1': [[251, 250], [322, 385]], 'Move2': [[186, 250], [249, 385]],
    'HeadAttackReady': [[324, 250], [403, 385]], 'HeadAttack': [[405, 250], [468, 385]],
    'BodyAttackReady': [[462, 145], [549, 248]], 'BodyAttack': [[551, 145], [622, 248]],

    '1': [[8, 8], [111, 143]], '2': [[113, 8], [200, 143]], '3': [[202, 8], [305, 143]], '4': [[307, 8], [394, 143]],

    '1': [[8, 145], [71, 248]], '2': [[73, 145], [128, 248]], '3': [[130, 145], [209, 248]], '4': [[211, 145], [322, 248]], '5': [[324, 145], [395, 248]],
    '6': [[397, 145], [460, 248]], '7': [[462, 145], [549, 248]], '8': [[551, 145], [622, 248]], '9': [[624, 145], [711, 248]],

    '1': [[8, 250], [95, 385]], 'hit': [[97, 250], [184, 385]], '3': [[186, 250], [249, 385]], '4': [[251, 250], [322, 385]], '5': [[324, 250], [403, 385]],
    '6': [[405, 250], [468, 385]], '7': [[470, 250], [533, 385]], '8': [[535, 250], [590, 385]], '9': [[592, 250], [679, 385]], '10': [[681, 250], [784, 385]],

    'win5': [[8, 387], [79, 538]], 'win6': [[81, 387], [152, 538]], '3': [[154, 387], [225, 538]],'4': [[227, 387], [314, 538]], '5': [[316, 387], [379, 538]],
    '6': [[381, 387], [460, 538]], '7': [[462, 387], [541, 538]],

    'win1': [[8, 540], [87, 667]], 'win2': [[89, 540], [168, 667]], 'win3': [[170, 540], [281, 667]],'win4': [[283, 540], [354, 667]],

    }


def reposition(self):
    self.start_x, self.start_y = self.x, self.y
    self.t = 0.0
    self.frame = 0


class return_idle:

    def __init__(self, boy):
        self.boy = boy

    def enter(self, e):
        self.boy.wait_time = get_time()
        self.boy.dir = 0
        self.boy.stance = -1  # idle시 하단 자세
        self.boy.atk = False

    def exit(self, e):
        reposition(self.boy)
        pass

    def do(self):
        #위치가 origin이랑 다르면 돌아오게 하기
        if self.boy.x != self.boy.origin_x or self.boy.y != self.boy.origin_y:
            if self.boy.t < 1.0:
                # self.pos = (1.0 - self.t) * self.start_pos + self.t * self.end_pos
                self.boy.t += MOVE_SPEED_PPS * game_framework.frame_time / self.boy.distance
                self.boy.y = (1.0 - self.boy.t) * self.boy.start_y + self.boy.t * (self.boy.origin_y)
                self.boy.x = (1.0 - self.boy.t) * self.boy.start_x + self.boy.t * (self.boy.origin_x)
            else:
                self.boy.x = self.boy.start_x = self.boy.origin_x
                self.boy.y = self.boy.start_y = self.boy.origin_y
                self.boy.t = 0.0
        #돌아오면 idle 이미지 출력
        else:
            sx, sy = sprite_size['IDle'][0]
            ex, ey = sprite_size['IDle'][1]
            self.boy.clip_x, self.boy.clip_y, self.boy.clip_w, self.boy.clip_h = carculate_image_position(self.boy, sx, sy, ex, ey)
            self.boy.state_machine.handle_state_event(('DONE', None))

    def draw(self):
        #composite이 필요한 우측 복귀를 출력하기 위함
        if self.boy.x > self.boy.origin_x:
            self.boy.image.clip_composite_draw(self.boy.clip_x, self.boy.clip_y, self.boy.clip_w, self.boy.clip_h,
                                               0, 'h', self.boy.x, self.boy.y, self.boy.output_size_w,
                                               self.boy.output_size_h)
        else:
            self.boy.image.clip_draw(self.boy.clip_x, self.boy.clip_y, self.boy.clip_w, self.boy.clip_h,
                                     self.boy.x, self.boy.y,
                                     self.boy.output_size_w, self.boy.output_size_h)


class Idle:

    def __init__(self, boy):
        self.boy = boy

    def enter(self, e):
        self.boy.wait_time = get_time()
        self.boy.dir = 0
        self.boy.stance = -1  # idle시 하단 자세
        self.boy.atk = False

    def exit(self, e):
        reposition(self.boy)
        pass

    def do(self):
        sx, sy = sprite_size['IDle'][0]
        ex, ey = sprite_size['IDle'][1]
        self.boy.clip_x, self.boy.clip_y, self.boy.clip_w, self.boy.clip_h = carculate_image_position(self.boy, sx, sy, ex, ey)

    def draw(self):
        self.boy.image.clip_draw(self.boy.clip_x, self.boy.clip_y, self.boy.clip_w, self.boy.clip_h,
                                self.boy.x, self.boy.y,
                                self.boy.output_size_w, self.boy.output_size_h)


class Guard:
    def __init__(self, boy):
        self.boy = boy

    def enter(self, e):
        self.boy.stance = 1  # guard시 상단 자세
        sx, sy = sprite_size['guard'][0]  # 좌상 (x1, y1)
        ex, ey = sprite_size['guard'][1]  # 우하 (x2, y2)
        self.boy.clip_x, self.boy.clip_y, self.boy.clip_w, self.boy.clip_h = carculate_image_position(self.boy, sx, sy, ex, ey)
        self.boy.dir = 1

    def exit(self, e):
        reposition(self.boy)
        pass

    def do(self):
        pass

    def draw(self):
        self.boy.image.clip_draw(self.boy.clip_x, self.boy.clip_y, self.boy.clip_w, self.boy.clip_h,
                                 self.boy.x, self.boy.y+60,
                                 self.boy.output_size_w, self.boy.output_size_h)


class Move:
    def __init__(self, boy):
        self.boy = boy
        self.enter_time = 0

    def enter(self, e):
        self.enter_time = get_time()
        if right_down(e):
            self.boy.dir = 2
        elif left_down(e):
            self.boy.dir = -2
        elif down_down(e):
            self.boy.dir = -1

    def exit(self, e):
        reposition(self.boy)
        if self.boy.dir != -1:
            sx, sy = sprite_size['Move2'][0]
            ex, ey = sprite_size['Move2'][1]
            self.boy.clip_x, self.boy.clip_y, self.boy.clip_w, self.boy.clip_h = carculate_image_position(self.boy, sx, sy, ex, ey)
        pass

    def do(self):
        self.boy.frame = (self.boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

        if self.boy.dir == -1:
            sx, sy = sprite_size['backstep'][0]
            ex, ey = sprite_size['backstep'][1]
        else:
            if int(self.boy.frame) == 0:
                sx, sy = sprite_size['Move2'][0]
                ex, ey = sprite_size['Move2'][1]
            else:
                sx, sy = sprite_size['Move1'][0]
                ex, ey = sprite_size['Move1'][1]

        if get_time() - self.enter_time > 1.0:
            self.boy.state_machine.handle_state_event(('TIMEOUT', None))

        self.boy.clip_x, self.boy.clip_y, self.boy.clip_w, self.boy.clip_h = carculate_image_position(self.boy, sx, sy, ex, ey)

        self.boy.t += MOVE_SPEED_PPS * game_framework.frame_time / self.boy.distance
        if self.boy.dir == -1:
            if self.boy.t < 1.0:
                # self.pos = (1.0 - self.t) * self.start_pos + self.t * self.end_pos
                self.boy.y = (1.0 - self.boy.t) * self.boy.start_y + self.boy.t * (self.boy.origin_y + self.boy.dir * 50)
            else:
                self.boy.y = self.boy.start_y = self.boy.origin_y + self.boy.dir * 50
                self.boy.t = 0.0
        else:
            if self.boy.t < 1.0:
                # self.pos = (1.0 - self.t) * self.start_pos + self.t * self.end_pos
                self.boy.x = (1.0 - self.boy.t) * self.boy.start_x + self.boy.t * (self.boy.origin_x + self.boy.dir * 50)
            else:
                self.boy.x = self.boy.start_x = self.boy.origin_x + self.boy.dir * 50
                self.boy.t = 0.0

    def draw(self):
        if self.boy.dir == 2: # right
            #self.boy.image.clip_draw(int(self.boy.frame) * 100, 100, 100, 100, self.boy.x, self.boy.y)
            self.boy.image.clip_composite_draw(self.boy.clip_x, self.boy.clip_y, self.boy.clip_w, self.boy.clip_h,
                                               0 ,'h', self.boy.x, self.boy.y, self.boy.output_size_w, self.boy.output_size_h)
        else: # dir == -2 or -1: # left or back
            #self.boy.image.clip_draw(int(self.boy.frame) * 100, 0, 100, 100, self.boy.x, self.boy.y)
            self.boy.image.clip_draw(self.boy.clip_x, self.boy.clip_y, self.boy.clip_w, self.boy.clip_h,
                                     self.boy.x, self.boy.y, self.boy.output_size_w, self.boy.output_size_h)


class Attack:
    def __init__(self, boy):
        self.boy = boy
        self.atk_dir = 0
        self.enter_time = 0

    def enter(self, e):
        self.enter_time = get_time()
        if z_down(e):
            self.atk_dir = -1
        if x_down(e):
            self.atk_dir = 1
        self.boy.atk = True

    def exit(self, e):
        self.boy.atk = False
        pass

    def do(self):
        self.boy.frame = (self.boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

        if self.boy.stance == 1: # up
            if int(self.boy.frame) == 0:
                sx, sy = sprite_size['HeadAttackReady'][0]
                ex, ey = sprite_size['HeadAttackReady'][1]
            else:
                sx, sy = sprite_size['HeadAttack'][0]
                ex, ey = sprite_size['HeadAttack'][1]
        else:
            if int(self.boy.frame) == 0:
                sx, sy = sprite_size['BodyAttackReady'][0]
                ex, ey = sprite_size['BodyAttackReady'][1]
            else:
                sx, sy = sprite_size['BodyAttack'][0]
                ex, ey = sprite_size['BodyAttack'][1]
        self.boy.clip_x, self.boy.clip_y, self.boy.clip_w, self.boy.clip_h = carculate_image_position(self.boy, sx, sy, ex, ey)

        if get_time() - self.enter_time > 0.5:
            self.boy.state_machine.handle_state_event(('TIMEOUT', None))

    def draw(self):
        if self.boy.stance == 1: # up
            if self.atk_dir == 1: #right
                self.boy.image.clip_composite_draw(self.boy.clip_x, self.boy.clip_y, self.boy.clip_w, self.boy.clip_h,
                                                   0, 'h', self.boy.x, self.boy.y+120, self.boy.output_size_w, self.boy.output_size_h)
            elif self.atk_dir == -1: #left
                self.boy.image.clip_draw(self.boy.clip_x, self.boy.clip_y, self.boy.clip_w, self.boy.clip_h,
                                         self.boy.x, self.boy.y+120, self.boy.output_size_w, self.boy.output_size_h)
        else: # down
            if self.atk_dir == 1: #right
                self.boy.image.clip_composite_draw(self.boy.clip_x, self.boy.clip_y, self.boy.clip_w, self.boy.clip_h,
                                                   0, 'h', self.boy.x, self.boy.y+60, self.boy.output_size_w, self.boy.output_size_h)
            elif self.atk_dir == -1: #left
                self.boy.image.clip_draw(self.boy.clip_x, self.boy.clip_y, self.boy.clip_w, self.boy.clip_h,
                                         self.boy.x,self.boy.y+60, self.boy.output_size_w, self.boy.output_size_h)


class Hit:
    def __init__(self, boy):
        self.boy = boy
        self.enter_time = 0

    def enter(self, e):
        self.enter_time = get_time()
        sx, sy = sprite_size['hit'][0]
        ex, ey = sprite_size['hit'][1]
        self.boy.clip_x, self.boy.clip_y, self.boy.clip_w, self.boy.clip_h = carculate_image_position(self.boy, sx, sy,                                                                                   ex, ey)

    def exit(self, e):
        pass

    def do(self):
        self.boy.frame = (self.boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

        if get_time() - self.enter_time > 0.3:
            self.boy.state_machine.handle_state_event(('TIMEOUT', None))

    def draw(self):
        if common.enemy.dir == 1: #right
            self.boy.image.clip_composite_draw(self.boy.clip_x, self.boy.clip_y, self.boy.clip_w, self.boy.clip_h,
                                               0, 'h', self.boy.x,
                                               self.boy.y+100, self.boy.output_size_w, self.boy.output_size_h)
        elif common.enemy.dir == -1: #left
            self.boy.image.clip_draw(self.boy.clip_x, self.boy.clip_y, self.boy.clip_w, self.boy.clip_h,
                                     self.boy.x, self.boy.y+100,
                                     self.boy.output_size_w, self.boy.output_size_h)


class Win:
    def __init__(self, boy):
        self.boy = boy
        self.end = False
        pass

    def enter(self, e):
        pass

    def exit(self, e):
        pass

    def do(self):
        self.boy.frame = (self.boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 7
        if self.boy.frame < 6:
            sprite_index = f'win{int(self.boy.frame)+1}'
        else:
            sprite_index = 'win6'
        sx, sy = sprite_size[sprite_index][0]
        ex, ey = sprite_size[sprite_index][1]
        self.boy.clip_x, self.boy.clip_y, self.boy.clip_w, self.boy.clip_h = carculate_image_position(self.boy, sx, sy, ex, ey)
        if self.boy.frame >= 6:
            self.end = True

    def draw(self):
        self.boy.image.clip_draw(self.boy.clip_x, self.boy.clip_y, self.boy.clip_w, self.boy.clip_h,
                                 self.boy.x, self.boy.y,
                                 self.boy.output_size_w, self.boy.output_size_h)


class Boy:
    def __init__(self):

        self.font = load_font('ENCR10B.TTF', 16)

        self.hp = 1600
        self.origin_x, self.origin_y = self.x, self.y = self.start_x, self.start_y = 400, 200
        self.dir = 0 #0: idle, 1: defense, -1:backstep , -2: left, 2:right
        self.stance = -1  # 1: 상단, -1: 하단
        self.atk = False

        self.frame = 0
        self.t = 0.0
        self.distance = math.sqrt((self.x - 1280) ** 2 + (self.y - 1024) ** 2)

        self.image = load_image('./image/Little_Mac.png')
        self.img_h = self.image.h  # 이미지 전체 높이
        self.clip_x = self.clip_y = self.clip_w = self.clip_h = 0
        self.output_size_w = self.output_size_h = 0

        self.IDLE = Idle(self)
        self.GUARD = Guard(self)
        self.MOVE = Move(self)
        self.ATTACK = Attack(self)
        self.RETURN_IDLE = return_idle(self)
        self.WIN = Win(self)
        self.HIT = Hit(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE : {
                    z_down: self.ATTACK, x_down: self.ATTACK,
                    up_down: self.GUARD,
                    down_down: self.MOVE, right_down: self.MOVE, left_down: self.MOVE,
                    win: self.WIN,
                    hit: self.HIT
                },
                self.GUARD: {
                    up_up: self.RETURN_IDLE,
                    z_down: self.ATTACK, x_down: self.ATTACK,
                    win: self.WIN
                },
                self.MOVE : {
                    down_up: self.RETURN_IDLE,
                    right_up: self.RETURN_IDLE, left_up: self.RETURN_IDLE,
                    time_out: self.RETURN_IDLE,
                    win: self.WIN
                },
                self.ATTACK : {
                    time_out: self.IDLE,
                    win: self.WIN
                },
                self.RETURN_IDLE : {
                    done: self.IDLE,
                    win: self.WIN
                },
                self.WIN : {
                },
                self.HIT : {
                    time_out: self.IDLE
                }
            }
        )


    def update(self):
        self.state_machine.update()
        self.output_size_w = self.clip_w *3
        self.output_size_h = self.clip_h *3
        if common.enemy.dead:
            self.state_machine.handle_state_event(('WIN', None))
        if common.enemy.state == 'Atk' and int(common.enemy.frame) == 1 and self.dir == 0:
            self.state_machine.handle_state_event(('HIT', None))

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        self.font.draw(self.x-10, self.y + 50, f'{self.hp:02d}', (255, 255, 0))
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        #self.state_machine.get_bb() < 상태에 따라 다르게 충돌 상자 설정하려면 여기서 구현
        return self.x - self.clip_w/2, self.y - self.clip_h/2, self.x + self.clip_w/2, self.y + self.clip_h/2

    def handle_collision(self, group, other):
        pass