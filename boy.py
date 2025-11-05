from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT
import math

import game_world
from ball import Ball, BigBall
from state_machine import StateMachine


def space_down(e): # e is space down ?
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

time_out = lambda e: e[0] == 'TIMEOUT'

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

#x1, y1, x2, y2
sprite_size = {'IDLE':[[154,395], [225,538]],
               'blank':[[0,0],[0,0]]}




class Idle:

    def __init__(self, boy):
        self.boy = boy

    def enter(self, e):
        self.boy.wait_time = get_time()
        self.boy.dir = 0


    def exit(self, e):
        if space_down(e):
            self.boy.fire_ball()


    def do(self):
        # self.boy.frame = (self.boy.frame + 1) % 8
        t = get_time()
        base_x, base_y = 400, 90
        r_x, r_y = 8, 4

        # speed: 0 -> pi 이동이 1/speed 초 걸림 (예: speed = 0.5 -> 2초)
        speed = 0.5

        # phase: 0 .. 2 범위를 주기적으로 만듦
        phase = (t * speed) % 2.0
        # triangle wave로 0 .. 1 .. 0 으로 변환 (일정한 속도)
        u = phase if phase <= 1.0 else 2.0 - phase
        angle = u * math.pi

        self.boy.x = base_x + r_x * math.cos(angle)
        self.boy.y = base_y + r_y * math.sin(angle)

    def draw(self):
        # original code
        # if self.boy.face_dir == 1: # right
        #     self.boy.image.clip_draw(self.boy.frame * 100, 300, 100, 100, self.boy.x, self.boy.y)
        # else: # face_dir == -1: # left
        #     self.boy.image.clip_draw(self.boy.frame * 100, 200, 100, 100, self.boy.x, self.boy.y)

        sx, sy = sprite_size['IDLE'][0]  # 좌상 (x1, y1)
        ex, ey = sprite_size['IDLE'][1]  # 우하 (x2, y2)

        img_h = self.boy.image.h  # 이미지 전체 높이
        clip_x = sx
        clip_y = img_h - ey - 1  # top-based y -> bottom-based y 변환
        clip_w = ex - sx + 1
        clip_h = ey - sy + 1

        self.boy.image.clip_draw(clip_x, clip_y, clip_w, clip_h, self.boy.x, self.boy.y)

class Move:
    def __init__(self, boy):
        self.boy = boy

    def enter(self, e):
        if right_down(e) or left_up(e):
            self.boy.dir = self.boy.face_dir = 1
        elif left_down(e) or right_up(e):
            self.boy.dir = self.boy.face_dir = -1

    def exit(self, e):
        if space_down(e):
            self.boy.fire_ball()

    def do(self):
        #self.boy.frame = (self.boy.frame + 1) % 8
        self.boy.x = 400 + self.boy.dir * 50
        if get_time() - self.boy.wait_time > 1:
            self.boy.state_machine.handle_state_event(('TIMEOUT', None))

    def draw(self):
        # if self.boy.face_dir == 1: # right
        #     self.boy.image.clip_draw(self.boy.frame * 100, 100, 100, 100, self.boy.x, self.boy.y)
        # else: # face_dir == -1: # left
        #     self.boy.image.clip_draw(self.boy.frame * 100, 0, 100, 100, self.boy.x, self.boy.y)
        self.boy.image.draw(self.boy.x, self.boy.y)







class Boy:
    def __init__(self):

        self.item = None
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.image = load_image('Little_Mac.png')

        self.IDLE = Idle(self)
        self.MOVE = Move(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE : {space_down: self.IDLE, right_down: self.MOVE, left_down: self.MOVE},
                self.MOVE : {time_out: self.IDLE,space_down: self.MOVE, right_up: self.IDLE, left_up: self.IDLE, right_down: self.IDLE, left_down: self.IDLE}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()


    def fire_ball(self):
        if self.item == 'Ball':
            ball = Ball(self.x, self.y, self.face_dir*10)
            game_world.add_object(ball, 1)
        elif self.item == 'BigBall':
            ball = BigBall(self.x, self.y, self.face_dir*10)
            game_world.add_object(ball, 1)
        else:
            print(f'볼이 없습니다')