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
TIME_PER_ACTION = 2
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
NOR_PER_ACTION = 2
ONE_PER_ACTION = 1
ATK_PER_ACTION = 4
GIMMIK_PER_ACTION = 6
OUT_PER_ACTION = 12

sprite = {
    #'상태_스탠스_프레임': [[시작x, 시작y], [끝x, 끝y]]
    'Idle_-1_1': [[0, 0], [69, 168]], 'Idle_-1_2': [[70, 0], [132, 168]], 'Idle_1_1': [[133, 0], [212, 168]], 'Idle_1_2': [[134, 0], [277, 168]], 'Move_0_1': [[315, 0], [383, 168]], 'Move_0_2': [[384, 0],[453, 168]],

    'Def_1_1': [[0, 169], [70, 345]], 'Def_-1_1': [[71, 169], [135, 345]],

    'Atk_1_1': [[0, 170], [75, 527]], 'Atk_1_2': [[0, 170], [75, 527]], 'Atk_1_3': [[76, 170], [146, 527]], 'Atk_1_4': [[76, 170], [146, 527]],

    'Atk_-1_1': [[0, 528], [71, 702]], 'Atk_-1_2': [[0, 528], [71, 702]], 'Atk_-1_3': [[72, 528], [154, 702]], 'Atk_-1_4': [[155, 528], [253, 702]],

    '1': [[0, 703], [58, 866]], '2': [[59, 703], [145, 866]], '3': [[146, 703], [252, 866]],

    '1': [[0, 867], [63, 1043]], '2': [[64, 867], [143, 1043]], '3': [[144, 867], [242, 1043]], '4': [[143, 867], [333, 1043]], '5': [[334, 867], [415, 1043]], '6': [[416, 867], [502, 1043]],

    '1': [[0, 1044], [73, 1236]], '2': [[74, 1044], [159, 1236]],

    'Stun_0_1': [[0, 1045], [73, 1393]], 'Stun_0_2': [[0, 1045], [152, 1393]],

    '1': [[0, 1394], [65, 1569]], '2': [[66, 1394], [137, 1569]], '3': [[138, 1394], [231, 1569]], '4': [[232, 1394], [311, 1569]], '5': [[312, 1394], [402, 1569]], '6': [[403, 1394], [467, 1569]],

    'Hit_1_1': [[0, 1570], [59, 1762]], 'Hit_-1_1': [[60, 1570], [146, 1762]], '3': [[147, 1570], [225, 1762]], '4': [[226, 1570], [330, 1762]], '5': [[331, 1570], [405, 1762]], '6': [[406, 1570], [501, 1762]],

    '1': [[0, 1763], [102, 1944]], '2': [[103, 1763], [203, 1944]], '3': [[204, 1763], [306, 1944]], '4': [[307, 1763], [384, 1944]], '5': [[385, 1763], [450, 1944]],
}

class Enemy:

    images = None

    def __init__(self):

        self.x, self.y = 400, 300
        self.dir = 0 # 1: 오른쪽, -1:왼쪽
        self.hp = 10
        self.stance = -1  # 1: 상단, -1: 하단
        self.state = 'Idle'

        self.image = load_image('./image/Gabby_Jay.png')
        self.sprite_idx = 'Idle_-1_1'
        self.frame = random.randint(0, 9)
        self.frame_per_action = NOR_PER_ACTION

        self.img_h = self.image.h  # 이미지 전체 높이
        self.clip_x = self.clip_y = self.clip_w = self.clip_h = 0
        self.output_size_w = self.output_size_h = 0

        self.build_behavior_tree()

    def get_bb(self):
        return self.x - self.clip_w, self.y - self.clip_h, self.x + self.clip_w, self.y + self.clip_h

    def update(self):
        self.frame = (self.frame + OUT_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % self.frame_per_action
        self.sprite_index = f'{self.state}_{self.stance}_{int(self.frame) + 1}'
        self.output_size_w = self.clip_w * 3
        self.output_size_h = self.clip_h * 3
        self.bt.run()
        pass


    def draw(self):
        sx, sy = sprite[self.sprite_index][0]
        ex, ey = sprite[self.sprite_index][1]
        self.clip_x, self.clip_y, self.clip_w, self.clip_h = game_framework.carculate_image_position(self, sx, sy, ex, ey)

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

    def frame_reset(self):
        self.frame = 0

    def stance_dir_set(self):
        self.stance = random.choice([1, -1])
        self.dir = random.choice([1, -1])
        self.frame_per_action = NOR_PER_ACTION
        return BehaviorTree.SUCCESS

    def Idle(self):
        self.state = 'Idle'
        self.frame_per_action = NOR_PER_ACTION
        if int(self.frame) == self.frame_per_action - 1:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def Move(self):
        self.frame_per_action = NOR_PER_ACTION
        self.state = 'Move'
        self.stance = 0
        if int(self.frame) == self.frame_per_action - 1:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def Attack(self):
        self.state = 'Atk'
        if self.stance == -1:
            self.frame_per_action = ATK_PER_ACTION
        if int(self.frame) == self.frame_per_action - 1:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def Stun(self):
        #기절 상태
        self.state = 'Stun'
        self.stance = 0
        self.frame_per_action = NOR_PER_ACTION
        if self.frame == self.frame_per_action - 1:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def Defend(self):
        self.state = 'Def'
        self.frame_per_action = ONE_PER_ACTION
        if self.frame == self.frame_per_action - 1:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def Hit(self):
        self.frame_per_action = ONE_PER_ACTION
        self.state = 'Hit'
        if self.frame == self.frame_per_action - 1:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def move_chk(self):
        #이동 중 피격
        if self.state == 'Move':
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def atk_ing_chk(self):
        #공격 도중 피격
        if self.state == 'Atk':
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def stance_check(self):
        #boy의 dir 확인
        if common.boy.stance == -1 and self.stance == -1:
            return BehaviorTree.SUCCESS
        elif common.boy.stance == 1 and self.stance == 1:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def boy_atk_chk(self):
        #boy가 공격 중인지 확인
        if common.boy.atk == True:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL


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

        a_frame_reset = Action('Frame reset', self.frame_reset)
        a_stance_dir_set = Action('Set stance and direction', self.stance_dir_set)
        a_Idle = Action('IDLE', self.Idle)
        a_Move = Action('MOVE', self.Move)
        a_Atk = Action('ATTACK', self.Attack)
        #스탠스 활용

        a_Def = Action('DEFEND', self.Defend)
        a_Hit = Action('HIT', self.Hit)
        a_Stun = Action('STUN', self.Stun)
        #boy의 dir 확인으로 방어 성공 여부 판단
        c_move_chk = Condition('move chk', self.move_chk)
        c_stance_chk = Condition('stance chk', self.stance_check)
        c_atk_ing_chk = Condition('atk ing chk', self.atk_ing_chk)
        c_boy_atk_chk = Condition('boy atk chk', self.boy_atk_chk)

        root = stun_chk = Sequence('Stun chk', c_atk_ing_chk ,a_Stun)
        root = def_chk = Sequence('Def chk', c_stance_chk, a_Def)

        root = Idle = Sequence('Idle', a_frame_reset, a_Idle)
        root = Move = Sequence('Move', a_frame_reset, a_Move)
        root = Atk = Sequence('Atk', a_frame_reset,a_Atk)
        root = Non_Hit = Sequence('Non_Hit', a_stance_dir_set, Idle, Atk, Move)

        root = Hit = Selector('Hit', c_move_chk, stun_chk, def_chk, a_Hit)
        root = Hit_chk = Sequence('Hit chk', c_boy_atk_chk, Hit)

        root = Hit_or_Non_Hit = Selector('Hit or Non_Hit', Hit_chk, Non_Hit)

        root = Sequence('Enemy BT', a_frame_reset, Hit_or_Non_Hit)

        self.bt = BehaviorTree(root)