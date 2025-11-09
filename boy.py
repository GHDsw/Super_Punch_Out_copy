from pico2d import load_image, get_time, load_font, draw_rectangle
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT

import game_world
import game_framework

from ball import Ball
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



# Boy의 Run Speed 계산

# Boy Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

# x1, y1, x2, y2
sprite_size = {'IDle': [[154, 395], [225, 538]],
               # 무브 원투 바뀜 펼쳐지며 회피가 아니라 돌아오며 접히는거였음
               # 어쩐지 각도 작은게 오른쪽에 있더라 젠장
               'Move1': [[186, 250], [249, 385]], 'Move2': [[251, 250], [322, 385]],
               'HeadAttackReady': [[186, 250], [249, 385]], 'HeadAttackL': [[251, 250], [322, 385]],
               'HeadAttackR': [[186, 250], [249, 385]],
               'BodyAttackReady': [[186, 250], [249, 385]], 'BodyAttack': [[251, 250], [322, 385]],

               'blank': [[8, 8], [111, 143]], 'blank': [[113, 8], [200, 143]], 'blank': [[202, 8], [305, 143]],
               'blank': [[307, 8], [394, 143]],

               'blank': [[8, 145], [71, 248]], 'blank': [[73, 145], [128, 248]], 'blank': [[130, 145], [209, 248]],
               'blank': [[211, 145], [322, 248]], 'blank': [[324, 145], [395, 248]],
               'blank': [[397, 145], [460, 248]], 'blank': [[462, 145], [549, 248]], 'blank': [[551, 145], [622, 248]],
               'blank': [[624, 145], [711, 248]],

               'blank': [[8, 250], [95, 385]], 'blank': [[97, 250], [184, 385]], 'blank': [[186, 250], [249, 385]],
               'blank': [[251, 250], [322, 385]], 'blank': [[324, 250], [403, 385]],
               'blank': [[405, 250], [468, 385]], 'blank': [[470, 250], [533, 385]], 'blank': [[535, 250], [590, 385]],
               'blank': [[592, 250], [679, 385]], 'blank': [[681, 250], [784, 385]],

               'blank': [[8, 387], [79, 538]], 'blank': [[81, 387], [152, 538]], 'blank': [[154, 387], [225, 538]],
               'blank': [[227, 387], [314, 538]], 'blank': [[316, 387], [379, 538]],
               'blank': [[381, 387], [460, 538]], 'blank': [[462, 387], [541, 538]],

               'blank': [[8, 540], [87, 667]], 'blank': [[89, 540], [168, 667]], 'blank': [[170, 540], [281, 667]],
               'blank': [[283, 540], [354, 667]],

               }



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
        self.boy.frame = (self.boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        if get_time() - self.boy.wait_time > 3:
            self.boy.state_machine.handle_state_event(('TIMEOUT', None))

    def draw(self):
        if self.boy.face_dir == 1: # right
            self.boy.image.clip_draw(int(self.boy.frame) * 100, 300, 100, 100, self.boy.x, self.boy.y)
        else: # face_dir == -1: # left
            self.boy.image.clip_draw(int(self.boy.frame) * 100, 200, 100, 100, self.boy.x, self.boy.y)


class Sleep:

    def __init__(self, boy):
        self.boy = boy

    def enter(self, e):
        pass

    def exit(self, e):
        pass

    def do(self):
        self.boy.frame = (self.boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8


    def handle_event(self, event):
        pass

    def draw(self):
        if self.boy.face_dir == 1:
            self.boy.image.clip_composite_draw(int(self.boy.frame) * 100, 300, 100, 100, 3.141592/2, '', self.boy.x - 25, self.boy.y - 25, 100, 100)
        else:
            self.boy.image.clip_composite_draw(int(self.boy.frame) * 100, 200, 100, 100, -3.141592/2, '', self.boy.x + 25, self.boy.y - 25, 100, 100)



class Run:
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
        self.boy.frame = (self.boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        self.boy.x += self.boy.dir * RUN_SPEED_PPS * game_framework.frame_time

    def draw(self):
        if self.boy.face_dir == 1: # right
            self.boy.image.clip_draw(int(self.boy.frame) * 100, 100, 100, 100, self.boy.x, self.boy.y)
        else: # face_dir == -1: # left
            self.boy.image.clip_draw(int(self.boy.frame) * 100, 0, 100, 100, self.boy.x, self.boy.y)







class Boy:
    def __init__(self):

        self.ball_count = 10

        self.font = load_font('ENCR10B.TTF', 16)

        self.x, self.y = 0, 90
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.image = load_image('./image/Little_Mac.png')

        self.IDLE = Idle(self)
        self.SLEEP = Sleep(self)
        self.RUN = Run(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.SLEEP : {space_down: self.IDLE},
                self.IDLE : {space_down: self.IDLE, time_out: self.SLEEP, right_down: self.RUN, left_down: self.RUN, right_up: self.RUN, left_up: self.RUN},
                self.RUN : {space_down: self.RUN, right_up: self.IDLE, left_up: self.IDLE, right_down: self.IDLE, left_down: self.IDLE}
            }
        )



    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
        self.font.draw(self.x-10, self.y + 50, f'{self.ball_count:02d}', (255, 255, 0))
        # *을 붙이는 이유
        # get_bb()가 반환하는 값이 튜플이기 때문에 언패킹을 해줘야 한다.
        # draw_rectangle 함수는 4개의 인자(x1,y1,x2,y2)를 받아야 하는데
        # get_bb()가 반환하는 값은 하나의 튜플이기 때문에 오류가 발생한다.
        # 따라서 *을 붙여서 튜플을 언패킹하여 4개의 인자로 전달해준다.
        draw_rectangle(*self.get_bb())

    def fire_ball(self):
        if self.ball_count > 0:
            self.ball_count -= 1
            ball = Ball(self.x+self.face_dir*40, self.y+100, self.face_dir * 15)
            game_world.add_object(ball, 1)
            game_world.add_collision_pair('grass:ball', None, ball)
            game_world.add_collision_pair('boy:ball', None, ball)
            game_world.add_collision_pair('zombie:ball', None, ball)

    def get_bb(self):
        #self.state_machine.get_bb() < 상태에 따라 다르게 충돌 상자 설정하려면 여기서 구현
        return self.x - 20, self.y - 50, self.x + 20, self.y + 40

    def handle_collision(self, group, other):
        if group == 'boy:ball':
            self.ball_count += 1
            # 충돌한 ball은 ball 자신이 제거하도록
        if group == 'boy:zombie':
            # 게임 종료 처리
            game_framework.quit()
            pass