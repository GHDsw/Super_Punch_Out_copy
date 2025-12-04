import random
import math
import game_framework
import game_world

from pico2d import *
from state_machine import StateMachine
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector

time_out = lambda e: e[0] == 'TIMEOUT'
event_end = lambda e: e[0] == 'EVENT_END'
event_move = lambda e: e[0] == 'EVENT_MOVE'
event_hit = lambda e: e[0] == 'EVENT_HIT'
event_attack = lambda e: e[0] == 'EVENT_ATTACK'

# zombie Run Speed
PIXEL_PER_METER = (100.0 / 0.1)  # 10 pixel 1 cm
MOVE_SPEED_KMPH = 20.0  # Km / Hour
MOVE_SPEED_MPM = (MOVE_SPEED_KMPH * 1000.0 / 60.0)
MOVE_SPEED_MPS = (MOVE_SPEED_MPM / 60.0)
MOVE_SPEED_PPS = (MOVE_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
NOR_PER_ACTION = 2
SPE_PER_ACTION = 3
GIMMIK_PER_ACTION = 6
OUT_PER_ACTION = 12

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

class Enemy:

    images = None

    def __init__(self):

        self.x, self.y = 400, 300
        self.image = load_image('./image/Gabby_Jay.png')
        self.frame = random.randint(0, 9)
        self.dir = random.choice([-1,1])

        self.img_h = self.image.h  # 이미지 전체 높이
        self.clip_x = self.clip_y = self.clip_w = self.clip_h = 0
        self.output_size_w = self.output_size_h = 0

        self.hp = 10

        self.build_behavior_tree()

    def get_bb(self):
        return self.x - self.clip_w, self.y - self.clip_h, self.x + self.clip_w, self.y + self.clip_h

    def update(self):
        self.frame = (self.frame + OUT_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % NOR_PER_ACTION
        self.output_size_w = self.clip_w * 3
        self.output_size_h = self.clip_h * 3
        self.bt.run()
        pass


    def draw(self):
        self.boy.image.clip_composite_draw(self.clip_x, self.clip_y, self.clip_w, self.clip_h,
                                           0, 'h', self.x, self.y + 120, self.output_size_w,
                                           self.output_size_h)
        draw_rectangle(*self.get_bb())
        pass

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        if group == 'boy:enemy':
            self.hp -= 10

    def Idle(self):
        self.state = 'Idle'
        sx, sy = sprite_size['Idle']
        ex, ey = sprite_size['Idle'][1]
        self.clip_x, self.clip_y, self.clip_w, self.clip_h = game_framework.carculate_image_position(self, sx, sy, ex,
                                                                                                     ey)
        return BehaviorTree.SUCCESS

    def stance_check(self):
        #스탠스 체크
        return BehaviorTree.SUCCESS

    def Move(self):
        self.state = 'Move'
        sx, sy = sprite_size['Move']
        ex, ey = sprite_size['Move'][1]
        self.clip_x, self.clip_y, self.clip_w, self.clip_h = game_framework.carculate_image_position(self, sx, sy, ex,
                                                                                                     ey)
        return BehaviorTree.SUCCESS

    def direction_check(self):
        #이동 방향 체크
        return BehaviorTree.SUCCESS

    def Attack(self):
        self.state = 'Atk'
        sx, sy = sprite_size['Atk']
        ex, ey = sprite_size['Atk'][1]
        self.clip_x, self.clip_y, self.clip_w, self.clip_h = game_framework.carculate_image_position(self, sx, sy, ex,
                                                                                                     ey)
        return BehaviorTree.SUCCESS

    def Defend(self):
        self.state = 'Def'
        sx, sy = sprite_size['Def']
        ex, ey = sprite_size['Def'][1]
        self.clip_x, self.clip_y, self.clip_w, self.clip_h = game_framework.carculate_image_position(self, sx, sy, ex,
                                                                                                     ey)
        return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        # a1 = Action('Set target location', self.set_target_location, 1000, 1000)
        # a2 = Action('Move to', self.move_to)
        # root = move_to_target_location = Sequence('Move to target location', a1, a2)

        a_Idle = Action('IDLE', self.Idle)
        c_stance = Condition('Stance Chk', self.stance_check)

        a_Move = Action('MOVE', self.Move)
        c_dir = Condition('Direction Chk', self.direction_check)

        a_Atk = Action('ATTACK', self.Attack)
        #스탠스 체크 활용

        a_Def = Action('DEFEND', self.Defend)
        #스탠스 체크 활용



        root =
        self.bt = BehaviorTree(root)