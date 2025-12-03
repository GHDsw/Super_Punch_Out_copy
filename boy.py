from pico2d import load_image, get_time, load_font, draw_rectangle
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_UP, SDLK_DOWN, SDLK_z, SDLK_x
import math
import common

import game_world
import game_framework

from state_machine import StateMachine


def space_down(e): # e is space down ?
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

time_out = lambda e: e[0] == 'TIMEOUT'

Return = lambda e: e[0] == 'RETURN'

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
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 2

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

    '1': [[8, 250], [95, 385]], '2': [[97, 250], [184, 385]], '3': [[186, 250], [249, 385]], '4': [[251, 250], [322, 385]], '5': [[324, 250], [403, 385]],
    '6': [[405, 250], [468, 385]], '7': [[470, 250], [533, 385]], '8': [[535, 250], [590, 385]], '9': [[592, 250], [679, 385]], '10': [[681, 250], [784, 385]],

    '1': [[8, 387], [79, 538]], '2': [[81, 387], [152, 538]], '3': [[154, 387], [225, 538]],'4': [[227, 387], [314, 538]], '5': [[316, 387], [379, 538]],
    '6': [[381, 387], [460, 538]], '7': [[462, 387], [541, 538]],

    '1': [[8, 540], [87, 667]], '2': [[89, 540], [168, 667]], '3': [[170, 540], [281, 667]],'4': [[283, 540], [354, 667]],

    }


def reposition(self):
    self.x, self.y = self.origin_x, self.origin_y
    self.dir = 0


class Idle:

    def __init__(self, boy):
        self.boy = boy
        self.t = 0.0
        self.distance = math.sqrt((self.boy.x - 1280) ** 2 + (self.boy.y - 1024) ** 2)

    def enter(self, e):
        self.boy.wait_time = get_time()

        self.boy.dir = 0
        sx, sy = sprite_size['IDle'][0]
        ex, ey = sprite_size['IDle'][1]

    def exit(self, e):
        pass

    def do(self):
        self.boy.frame = (self.boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)%2

    def draw(self):
        self.boy.image.clip_draw(self.boy.clip_x, self.boy.clip_y, self.boy.clip_w, self.boy.clip_h,
                                 self.boy.x, self.boy.y,
                                 self.boy.output_size_w, self.boy.output_size_h)


class GAURD:
    def __init__(self, boy):
        pass

    def enter(self, e):
        pass

    def exit(self, e):
        pass

    def do(self):
        pass

    def draw(self):
        pass


class Move:
    def __init__(self, boy):
        self.boy = boy
        self.t = 0.0
        self.distance = math.sqrt((self.boy.x - 1280) ** 2 + (self.boy.y - 1024) ** 2)

    def enter(self, e):
        if right_down(e):
            self.boy.dir = 1
        elif left_down(e):
            self.boy.dir = -1
        if left_up(e) or right_up(e):
            self.Return = True

    def exit(self, e):
        # if space_down(e):
        #     self.boy.fire_ball()
        pass

    def do(self):
        self.boy.frame = (self.boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

        if self.boy.x <850 and self.boy.x > 750:
            sx, sy = sprite_size['Move2'][0]
            ex, ey = sprite_size['Move2'][1]
        else:
            sx, sy = sprite_size['Move1'][0]
            ex, ey = sprite_size['Move1'][1]

        if self.Return:
            if self.t < 1.0:
                self.t += MOVE_SPEED_PPS * game_framework.frame_time / self.distance
                self.boy.x = (1.0 - self.t) * (self.boy.origin_x +self.boy.dir*100) + self.t * self.boy.origin_x
                self.boy.y = (1.0 - self.t) * (self.boy.origin_y-20) + self.t * self.boy.origin_y
                #self.boy.y = (1.0 - self.t) * self.t * sy + ey #이렇게 작성하면 통통 튐
            else:
                self.boy.x, self.boy.y = self.boy.origin_x, self.boy.origin_y
                self.t = 0.0
                self.Return = False
        else:
            self.boy.x, self.boy.y = self.boy.origin_x + self.boy.dir*100, self.boy.origin_y-20

        self.boy.clip_x = sx
        self.boy.clip_y = self.boy.img_h - ey - 1  # top-based y -> bottom-based y 변환
        self.boy.clip_w = ex - sx + 1
        self.boy.clip_h = ey - sy + 1

        if self.boy.x == self.boy.origin_x:
            self.boy.state_machine.handle_state_event(('RETURN', None))

    def draw(self):
        if self.boy.dir == 1: # right
            #self.boy.image.clip_draw(int(self.boy.frame) * 100, 100, 100, 100, self.boy.x, self.boy.y)
            self.boy.image.clip_composite_draw(self.boy.clip_x, self.boy.clip_y, self.boy.clip_w, self.boy.clip_h,
                                               0 ,'h', self.boy.x, self.boy.y, self.boy.output_size_w, self.boy.output_size_h)
        else: # face_dir == -1: # left
            #self.boy.image.clip_draw(int(self.boy.frame) * 100, 0, 100, 100, self.boy.x, self.boy.y)
            self.boy.image.clip_draw(self.boy.clip_x, self.boy.clip_y, self.boy.clip_w, self.boy.clip_h,
                                     self.boy.x, self.boy.y, self.boy.output_size_w, self.boy.output_size_h)

class Attack:
    def __init__(self, boy):
        self.boy = boy

    def enter(self, e):
        self.boy.wait_time = get_time()
        if z_down(e):
            self.boy.dir = -1
        if x_down(e):
            self.boy.dir = 1

    def exit(self, e):
        # if space_down(e):
        #     self.boy.fire_ball()
        pass

    def do(self):
        self.boy.frame = (self.boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)%2

        if self.boy.face_dir == 1:
            if self.boy.frame == 1:
                sx, sy = sprite_size['HeadAttackReady'][0]  # 좌상 (x1, y1)
                ex, ey = sprite_size['HeadAttackReady'][1]  # 우하 (x2, y2)
            else:
                sx, sy = sprite_size['HeadAttack'][0]  # 좌상 (x1, y1)
                ex, ey = sprite_size['HeadAttack'][1]  # 우하 (x2, y2)
        else:
            if self.boy.frame == 1:
                sx, sy = sprite_size['BodyAttackReady'][0]  # 좌상 (x1, y1)
                ex, ey = sprite_size['BodyAttackReady'][1]  # 우하 (x2, y2)
            else:
                sx, sy = sprite_size['BodyAttack'][0]  # 좌상 (x1, y1)
                ex, ey = sprite_size['BodyAttack'][1]  # 우하 (x2, y2)
        self.boy.clip_x = sx
        self.boy.clip_y = self.boy.img_h - ey - 1  # top-based y -> bottom-based y 변환
        self.boy.clip_w = ex - sx + 1
        self.boy.clip_h = ey - sy + 1

        #타임아웃 넘기는거 위치 바꿨더니 해결됨 ㅋㅋ
        if get_time() - self.boy.wait_time > 0.5:
            self.boy.dir = 0
            self.boy.state_machine.handle_state_event(('TIMEOUT', None))

    def draw(self):
        if self.boy.face_dir == 1: # up
            if self.boy.dir == 1: #right
                self.boy.image.clip_composite_draw(self.boy.clip_x, self.boy.clip_y, self.boy.clip_w, self.boy.clip_h,
                                                   0, 'h', self.boy.x, self.boy.y, self.boy.output_size_w, self.boy.output_size_h)
            elif self.boy.dir == -1: #left
                self.boy.image.clip_draw(self.boy.clip_x, self.boy.clip_y, self.boy.clip_w, self.boy.clip_h,
                                         self.boy.x, self.boy.y, self.boy.output_size_w, self.boy.output_size_h)
        elif self.boy.face_dir == -1: # down
            if self.boy.dir == 1:
                self.boy.image.clip_composite_draw(self.boy.clip_x, self.boy.clip_y, self.boy.clip_w, self.boy.clip_h,
                                                   0, 'h', self.boy.x, self.boy.y, self.boy.output_size_w, self.boy.output_size_h)
            elif self.boy.dir == -1:  # left
                self.boy.image.clip_draw(self.boy.clip_x, self.boy.clip_y, self.boy.clip_w, self.boy.clip_h,
                                         self.boy.x,self.boy.y, self.boy.output_size_w, self.boy.output_size_h)





class Boy:
    def __init__(self):

        self.hp = 10

        self.font = load_font('ENCR10B.TTF', 16)

        self.x, self.y = self.origin_x, self.origin_y = 400, 100
        self.frame = 0
        self.dir = 0
        self.image = load_image('./image/Little_Mac.png')

        self.img_h = self.image.h  # 이미지 전체 높이
        self.clip_x = self.clip_y = self.clip_w = self.clip_h = 0

        self.output_size_w = self.output_size_h = 0

        self.IDLE = Idle(self)
        self.MOVE = Move(self)
        self.ATTACK = Attack(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE : {
                    z_down: self.ATTACK, x_down: self.ATTACK,
                    up_down: self.GAURD,
                    down_down: self.MOVE, right_down: self.MOVE, left_down: self.MOVE
                },
                self.GAURD: {
                    up_up: self.IDLE
                },
                self.MOVE : {
                    down_up: self.IDLE,
                    right_up: self.IDLE, left_up: self.IDLE,
                    time_out: self.IDLE
                },
                self.ATTACK : {
                    time_out: self.IDLE
                }
            }
        )


    def update(self):
        self.state_machine.update()
        self.output_size_w = self.clip_w * 1.5
        self.output_size_h = self.clip_h * 1.5

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
        self.font.draw(self.x-10, self.y + 50, f'{self.hp:02d}', (255, 255, 0))
        # *을 붙이는 이유
        # get_bb()가 반환하는 값이 튜플이기 때문에 언패킹을 해줘야 한다.
        # draw_rectangle 함수는 4개의 인자(x1,y1,x2,y2)를 받아야 하는데
        # get_bb()가 반환하는 값은 하나의 튜플이기 때문에 오류가 발생한다.
        # 따라서 *을 붙여서 튜플을 언패킹하여 4개의 인자로 전달해준다.
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        #self.state_machine.get_bb() < 상태에 따라 다르게 충돌 상자 설정하려면 여기서 구현
        return self.x - self.clip_w/2, self.y - self.clip_h/2, self.x + self.clip_w/2, self.y + self.clip_h/2

    def handle_collision(self, group, other):
        if group == 'boy:enemy':
            pass
    #     if group == 'boy:ball':
    #         self.ball_count += 1
    #         # 충돌한 ball은 ball 자신이 제거하도록
    #     if group == 'boy:zombie':
    #         # 게임 종료 처리
    #         game_framework.quit()
    #         pass