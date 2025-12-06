import random
import math
import game_framework
import game_world

from pico2d import *
from state_machine import StateMachine
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
import common

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
    'Idle': [[0, 0], [69, 168]],
    'Move': [[305, 0], [366, 168]], 'Move2': [[366, 0], [453, 168]],
    'Def': [[0, 169], [83, 345]],
    'Hit': [[60, 1570], [146, 1762]], 'Hit': [[147, 1570], [225, 1762]],
    'Stun': [[0, 1234], [ 73, 1392]],
    'Atk_up': [[84, 365], [153, 530]],
    'Atk_down': [[153, 365], [222, 530]],
    

    '1': [[0, 0], [69, 168]], '2': [[70, 0], [132, 168]], '3': [[133, 0], [212, 168]], '4': [[134, 0], [277, 168]], '5': [[315, 0], [383, 168]], '6': [[384, 0],[453, 168]],

    '1': [[0, 169], [70, 345]], '2': [[71, 169], [135, 345]],

    '1': [[0, 170], [75, 527]], '2': [[76, 170], [146, 527]],

    '1': [[0, 528], [71, 702]], '2': [[72, 528], [154, 702]], '3': [[155, 528], [253, 702]],

    '1': [[0, 703], [58, 866]], '2': [[59, 703], [145, 866]], '3': [[146, 703], [252, 866]],

    '1': [[0, 867], [63, 1043]], '2': [[64, 867], [143, 1043]], '3': [[144, 867], [242, 1043]], '4': [[143, 867], [333, 1043]], '5': [[334, 867], [415, 1043]], '6': [[416, 867], [502, 1043]],

    '1': [[0, 1044], [73, 1236]], '2': [[74, 1044], [159, 1236]],

    '1': [[0, 1045], [73, 1393]], '2': [[0, 1045], [152, 1393]],

    '1': [[0, 1394], [65, 1569]], '1': [[66, 1394], [137, 1569]], '1': [[138, 1394], [231, 1569]], '1': [[232, 1394], [311, 1569]], '1': [[312, 1394], [402, 1569]], '1': [[403, 1394], [467, 1569]],

    '1': [[0, 1570], [59, 1762]], '1': [[60, 1570], [146, 1762]], '1': [[147, 1570], [225, 1762]], '1': [[226, 1570], [330, 1762]], '1': [[331, 1570], [405, 1762]], '1': [[406, 1570], [501, 1762]],

    '1': [[0, 1763], [102, 1944]], '1': [[103, 1763], [203, 1944]], '1': [[204, 1763], [306, 1944]], '1': [[307, 1763], [384, 1944]], '1': [[385, 1763], [450, 1944]],
}

class Enemy:

    images = None

    def __init__(self):

        self.x, self.y = 400, 300
        self.dir = 0
        self.hp = 10
        self.stance = -1  #1: 상단, -1: 하단
        self.state = 'Idle'

        self.image = load_image('./image/Gabby_Jay.png')
        self.frame = random.randint(0, 9)

        self.img_h = self.image.h  # 이미지 전체 높이
        self.clip_x = self.clip_y = self.clip_w = self.clip_h = 0
        self.output_size_w = self.output_size_h = 0

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
        self.image.clip_composite_draw(self.clip_x, self.clip_y, self.clip_w, self.clip_h,
                                       0, 'h',
                                       self.x, self.y + 120,
                                       self.output_size_w, self.output_size_h)
        draw_rectangle(*self.get_bb())
        pass

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        if group == 'boy:enemy':
            self.hp -= 10

    def Idle(self):
        self.state = 'Idle'
        sx, sy = sprite_size['Idle'][0]
        ex, ey = sprite_size['Idle'][1]
        self.clip_x, self.clip_y, self.clip_w, self.clip_h = game_framework.carculate_image_position(self, sx, sy, ex, ey)
        return BehaviorTree.SUCCESS

    def stance(self):
        #스탠스 결정
        self.stance = random.choice([1, -1])
        return BehaviorTree.SUCCESS

    def Move(self):
        self.state = 'Move'
        sx, sy = sprite_size['Move'][0]
        ex, ey = sprite_size['Move'][1]
        self.clip_x, self.clip_y, self.clip_w, self.clip_h = game_framework.carculate_image_position(self, sx, sy, ex, ey)
        return BehaviorTree.SUCCESS

    def direction(self):
        #이동 방향 결정
        self.dir = random.choice([1, -1])
        return BehaviorTree.SUCCESS

    def Attack(self):
        self.state = 'Atk'
        sx, sy = sprite_size['Atk'][0]
        ex, ey = sprite_size['Atk'][1]
        self.clip_x, self.clip_y, self.clip_w, self.clip_h = game_framework.carculate_image_position(self, sx, sy, ex, ey)
        return BehaviorTree.SUCCESS

    def Defend(self):
        self.state = 'Def'
        sx, sy = sprite_size['Def'][0]
        ex, ey = sprite_size['Def'][1]
        self.clip_x, self.clip_y, self.clip_w, self.clip_h = game_framework.carculate_image_position(self, sx, sy, ex, ey)
        return BehaviorTree.SUCCESS

    def stance_check(self):
        #boy의 dir 확인
        if common.boy.dir == 1 and self.stance == 1:
            return BehaviorTree.SUCCESS
        elif common.boy.dir == -1 and self.stance == -1:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def Hit(self):
        self.state = 'Hit'
        sx, sy = sprite_size['Hit'][0]
        ex, ey = sprite_size['Hit'][1]
        self.clip_x, self.clip_y, self.clip_w, self.clip_h = game_framework.carculate_image_position(self, sx, sy, ex, ey)
        return BehaviorTree.SUCCESS

    def Atk_ing(self):
        #공격 도중 피격
        if self.state == 'Atk':
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def stun(self):
        #기절 상태
        self.state = 'Stun'
        sx, sy = sprite_size['Stun'][0]
        ex, ey = sprite_size['Stun'][1]
        self.clip_x, self.clip_y, self.clip_w, self.clip_h = game_framework.carculate_image_position(self, sx, sy, ex, ey)
        return BehaviorTree.SUCCESS


    def build_behavior_tree(self):
        # a1 = Action('Set target location', self.set_target_location, 1000, 1000)
        # a2 = Action('Move to', self.move_to)
        # root = move_to_target_location = Sequence('Move to target location', a1, a2)

        #굳이 스탠스를 따로 뺄 필요가 있을까?
        #디렉션도 마찬가지
        #행동 트리 구성
        # Idle, Move, Atk, Defend, Hit, Stun
        # 피격 판정
        # 1순위:회피 2순위:공격 도중 피격 3순위:방어 성공 4순위:피격

        a_Idle = Action('IDLE', self.Idle)

        a_Move = Action('MOVE', self.Move)

        a_Atk = Action('ATTACK', self.Attack)
        #스탠스 활용

        a_Def = Action('DEFEND', self.Defend)
        a_Hit = Action('HIT', self.Hit)
        a_Stun = Action('STUN', self.stun)
        #boy의 dir 확인으로 방어 성공 여부 판단
        c_move_chk = Condition('move chk', self.move_chk)
        c_stance_chk = Condition('stance chk', self.stance_check)
        c_atk_ing = Condition('atk ing', self.Atk_ing)

        root = stun_chk = Sequence('Stun chk', c_atk_ing ,a_Stun)
        root = def_chk = Sequence('Def chk', c_stance_chk, a_Def)

        root = Idle = Sequence('Idle', a_Atk, a_Move,a_Idle)
        root = Hit = Selector('Hit', c_move_chk, stun_chk, def_chk, a_Hit)

        root = Selector('Enemy Behavior', Hit, Idle)

        self.bt = BehaviorTree(root)