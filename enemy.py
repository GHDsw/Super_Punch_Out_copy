import random
import game_framework

from pico2d import *

from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
import common

time_out = lambda e: e[0] == 'TIMEOUT'
event_end = lambda e: e[0] == 'EVENT_END'
event_move = lambda e: e[0] == 'EVENT_MOVE'
event_hit = lambda e: e[0] == 'EVENT_HIT'
event_attack = lambda e: e[0] == 'EVENT_ATTACK'

# zombie Run Speed
PIXEL_PER_METER = (100.0 / 0.1)  # 10 pixel 1 cm
MOVE_SPEED_KMPH = 5.0  # Km / Hour
MOVE_SPEED_MPM = (MOVE_SPEED_KMPH * 1000.0 / 60.0)
MOVE_SPEED_MPS = (MOVE_SPEED_MPM / 60.0)
MOVE_SPEED_PPS = (MOVE_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 4.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 5.0
GIMMIK_PER_ACTION = 6
OUT_PER_ACTION = 12

sprite = {
    #'상태_스탠스_프레임': [[시작x, 시작y], [끝x, 끝y]]
    'Idle_-1_1': [[0, 0], [69, 168]], 'Idle_-1_2': [[70, 0], [132, 168]], 'Idle_1_1': [[133, 0], [212, 168]], 'Idle_1_2': [[213, 0], [277, 168]], 'Move_1': [[315, 0], [383, 168]], 'Move_2': [[384, 0],[453, 168]],

    'Def_1': [[0, 169], [70, 345]], 'Def_-1': [[71, 169], [135, 345]],

    'Atk_1_1': [[0, 346], [75, 527]], 'Atk_1_2': [[76, 346],[146, 527]],

    'Atk_-1_1': [[0, 528], [71, 702]], 'Atk_-1_2': [[72, 528], [154, 702]], 'Atk_-1_3': [[155, 528], [253, 702]],

    '1': [[0, 703], [58, 866]], '2': [[59, 703], [145, 866]], '3': [[146, 703], [252, 866]],

    '1': [[0, 867], [63, 1043]], '2': [[64, 867], [143, 1043]], '3': [[144, 867], [242, 1043]], '4': [[143, 867], [333, 1043]], '5': [[334, 867], [415, 1043]], '6': [[416, 867], [502, 1043]],

    '1': [[0, 1044], [73, 1236]], '2': [[74, 1044], [159, 1236]],

    'Stun_1': [[0, 1237], [73, 1393]], 'Stun_2': [[74, 1237], [152, 1393]],

    'intro_1': [[0, 1394], [65, 1575]], 'intro_2': [[66, 1394], [137, 1575]], 'intro_3': [[138, 1394], [231, 1575]], 'intro_4': [[232, 1394], [311, 1575]], '5': [[312, 1394], [402, 1575]], '6': [[403, 1394], [467, 1575]],

    'Stun_Hit': [[0, 1576], [59, 1768]], 'Hit_-1': [[60, 1576], [146, 1768]], 'Hit_1': [[147, 1576], [225, 1768]], '4': [[226, 1576], [330, 1768]], 'knockdown_1': [[331, 1576], [405, 1768]], 'knockdown_2': [[406, 1576], [501, 1768]],
    'knockdown_1_R': [[405, 1570], [331, 1768]],
    'knockdown_3': [[0, 1769], [102, 1944]], 'revive_1': [[103, 1769], [203, 1944]], 'revive_2': [[204, 1769], [306, 1944]], '4': [[307, 1769], [384, 1944]], '5': [[385, 1769], [450, 1944]],
}

class Enemy:

    images = None
    sound_gj_hit = None
    sound_gj_stun = None
    sound_gj_atk = None

    def __init__(self):

        self.x, self.y = self.origin_x, self.origin_y = self.start_x, self.start_y =400, 200
        self.dir = 0 # 1: 오른쪽, -1:왼쪽
        self.hp = 1600
        self.stance = -1  # 1: 상단, -1: 하단

        self.t = 0.0
        self.distance = math.sqrt((self.x - 1280) ** 2 + (self.y - 1024) ** 2)
        self.is_stunned = False
        self.stun_time = None

        self.knockdowned = False
        self.knockdown_x, self.knockdown_y = 100, 350
        self.knockdown_cnt = 0

        self.prev_state = None
        self.state = 'Idle'

        self.dead = False

        self.image = load_image('./image/Gabby_Jay.png')

        if not Enemy.sound_gj_hit:
            Enemy.sound_gj_hit = load_wav('./audio/effect/gj_hit.wav')
            Enemy.sound_gj_hit.set_volume(32)
        if not Enemy.sound_gj_stun:
            Enemy.sound_gj_stun = load_wav('./audio/effect/gj_stun.wav')
            Enemy.sound_gj_stun.set_volume(32)
        if not Enemy.sound_gj_atk:
            Enemy.sound_gj_atk = load_wav('./audio/effect/gj_atk.wav')
            Enemy.sound_gj_atk.set_volume(32)

        self.frame = 0
        self.sprite_index = 'Idle_-1_1'

        self.img_h = self.image.h  # 이미지 전체 높이
        self.clip_x = self.clip_y = self.clip_w = self.clip_h = 0
        self.output_size_w = self.output_size_h = 0

        self.build_behavior_tree()

    def get_bb(self):
        return self.x - self.clip_w, self.y - self.clip_h, self.x + self.clip_w, self.y + self.clip_h

    def update(self):
        self.frame = (self.frame + OUT_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.output_size_w = self.clip_w *3
        self.output_size_h = self.clip_h *3
        self.bt.run()

        if self.hp <= 0:
            self.knockdowned = True

        print(f'{self.state=} ')
        print(f'{self.stance=} ')
        print(f'{self.dir=} ')
        print(f'{self.hp=} ')
        print(f'{self.is_stunned=} ')
        print(f'{self.knockdowned=} ')
        print(f'{self.knockdown_cnt=} ')
        print(f'{self.dead=} ')
        pass


    def draw(self):
        # if self.frame > self.frame_per_action:
        #     self.frame = 0
        sx, sy = sprite[self.sprite_index][0]
        ex, ey = sprite[self.sprite_index][1]
        self.clip_x, self.clip_y, self.clip_w, self.clip_h = game_framework.carculate_image_position(self, sx, sy, ex, ey)
        if self.dir == 1:
            self.image.clip_composite_draw(self.clip_x, self.clip_y, self.clip_w, self.clip_h,
                                           0, '',
                                           self.x, self.y + 120,
                                           self.output_size_w, self.output_size_h)
        else:
            self.image.clip_composite_draw(self.clip_x, self.clip_y, self.clip_w, self.clip_h,
                                           0, 'h',
                                           self.x, self.y + 120,
                                           self.output_size_w, self.output_size_h)
        draw_rectangle(*self.get_bb())
        pass

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        pass

    def stance_dir_set(self):
        self.stance = random.choice([1, -1])
        self.dir = random.choice([1, -1])
        return BehaviorTree.SUCCESS

    def Idle(self):
        if self.prev_state != 'Idle':
            self.frame = 0.0
            self.prev_state = 'Idle'
        self.state = 'Idle'
        if int(self.frame) % 2 == 0:
            self.sprite_index = f'Idle_{self.stance}_1'
        else:
            self.sprite_index = f'Idle_{self.stance}_2'

        if self.knockdowned:
            return BehaviorTree.SUCCESS
        if self.frame < FRAMES_PER_ACTION - 1.0:
            return BehaviorTree.RUNNING
        else:
            return BehaviorTree.SUCCESS


    def Move(self):
        if self.prev_state != 'Move':
            self.frame = 0.0
            self.prev_state = 'Move'
        self.state = 'Move'
        if self.frame < 1:
            self.sprite_index = f'Move_1'
        else:
            self.sprite_index = f'Move_2'

        if self.knockdowned:
            return BehaviorTree.SUCCESS
        if int(self.frame) == FRAMES_PER_ACTION-1:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def Attack(self):
        if self.prev_state != 'Atk':
            self.frame = 0.0
            self.prev_state = 'Atk'
            self.sound_gj_atk.play()
        self.state = 'Atk'
        if self.frame < 1:
            self.sprite_index = f'Atk_{self.stance}_1'
        elif self.stance == -1 and self.frame >= 2:
            self.sprite_index = f'Atk_{self.stance}_3'
        else:
            self.sprite_index = f'Atk_{self.stance}_2'
            if common.boy.dir == 0:
                common.boy.hp -= 1

        if self.knockdowned:
            return BehaviorTree.SUCCESS
        if int(self.frame) == FRAMES_PER_ACTION-1:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def Stun(self):
        if self.prev_state != 'Stun':
            self.frame = 0.0
            self.prev_state = 'Stun'
            self.sound_gj_stun.play()
        self.state = 'Stun'
        if self.frame == self.frame % 2:
            self.sprite_index = f'Stun_1'
        else:
            self.sprite_index = f'Stun_2'
        if get_time() - self.stun_time > 5.0:
            self.is_stunned = False
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def Defend(self):
        if self.prev_state != 'Def':
            self.frame = 0.0
            self.prev_state = 'Def'
            self.sound_gj_atk.play()
        self.state = 'Def'
        self.sprite_index = f'Def_{self.stance}'
        if int(self.frame) == FRAMES_PER_ACTION - 1:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def Hit(self):
        if self.prev_state != 'Hit':
            self.frame = 0.0
            self.prev_state = 'Hit'
            self.hp -= 1
            self.sound_gj_hit.play()
        self.state = 'Hit'
        self.sprite_index = f'Hit_{-1*self.stance}'
        if int(self.frame) == FRAMES_PER_ACTION - 1:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def knockdown(self):
        if self.prev_state != 'knockdown':
            self.frame = 0.0
            self.prev_state = 'knockdown'
        self.state = 'knockdown'
        if self.y != self.knockdown_y:
            if self.t < 1.0:
                # self.pos = (1.0 - self.t) * self.start_pos + self.t * self.end_pos
                self.t += MOVE_SPEED_PPS * game_framework.frame_time / self.distance
                self.y = (1.0 - self.t) * self.start_y + self.t * (self.knockdown_y)
                if self.frame == 0:
                    self.sprite_index = f'knockdown_2'
                else:
                    self.dir = -1 * self.dir
            else:
                self.y = self.start_y = self.knockdown_y
                self.t = 0.0
                self.frame = 0
                if self.knockdown_cnt>=2:
                    self.dead = True
        else:
            self.sprite_index = f'knockdown_3'
        if not self.knockdowned:
            return BehaviorTree.FAIL
        elif self.sprite_index == f'knockdown_3' and int(self.frame) == FRAMES_PER_ACTION - 1:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def Revive(self):
        if self.prev_state != 'Revive':
            self.frame = 0.0
            self.prev_state = 'Revive'
        self.state = 'Revive'

        if self.frame < 1:
            self.sprite_index = f'revive_1'
        else:
            self.sprite_index = f'revive_2'

        if self.x != self.origin_x or self.y != self.origin_y:
            if self.t < 1.0:
                # self.pos = (1.0 - self.t) * self.start_pos + self.t * self.end_pos
                self.t += MOVE_SPEED_PPS * game_framework.frame_time / self.distance
                self.y = (1.0 - self.t) * self.start_y + self.t * (self.origin_y)
                self.x = (1.0 - self.t) * self.start_x + self.t * (self.origin_x)
            else:
                self.x = self.start_x = self.origin_x
                self.y = self.start_y = self.origin_y
                self.t = 0.0
        if (self.x == self.origin_x and self.y == self.origin_y) or self.dead:
            if not self.dead:
                self.knockdowned = False
                self.knockdown_cnt += 1
                self.hp = 1600 // (self.knockdown_cnt+1)
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
        if self.state == 'Atk' and common.boy.atk == True:
            self.is_stunned = True
            self.stun_time = get_time()
            self.hp -= 160
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def stunned_check(self):
        return BehaviorTree.SUCCESS if self.is_stunned else BehaviorTree.FAIL

    def stance_check(self):
        #boy의 dir 확인
        if common.boy.stance == -1 and self.stance == -1:
            return BehaviorTree.SUCCESS
        elif common.boy.stance == 1 and self.stance == 1:
            return BehaviorTree.SUCCESS
        else:
            self.hp -= 1
            return BehaviorTree.FAIL

    def boy_atk_chk(self):
        #boy가 공격 중인지 확인
        if common.boy.atk:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def build_behavior_tree(self):
        a_stance_dir_set = Action('Set stance and direction', self.stance_dir_set)
        a_Idle = Action('a_IDLE', self.Idle)
        a_Move = Action('a_MOVE', self.Move)
        a_Atk = Action('a_ATTACK', self.Attack)
        #스탠스 활용

        a_Def = Action('a_DEFEND', self.Defend)
        a_Hit = Action('a_HIT', self.Hit)
        a_Stun = Action('a_STUN', self.Stun)

        a_knockdown = Action('a_knockdown', self.knockdown)
        a_Revive = Action('a_Revive', self.Revive)

        a_move_chk = Action('move chk', self.move_chk)

        c_stance_chk = Condition('stance chk', self.stance_check)
        a_atk_ing_chk = Action('atk ing chk', self.atk_ing_chk)
        c_boy_atk_chk = Condition('boy atk chk', self.boy_atk_chk)
        c_is_stunned = Condition('is stunned', self.stunned_check)

        root = stun_chk = Sequence('Stun chk', c_is_stunned, a_Stun)
        root = def_chk = Sequence('Def chk', c_stance_chk, a_Def)

        root = Non_Hit = Sequence('Non_Hit', a_stance_dir_set, a_Idle, a_Move, a_Atk)

        root = Hit = Selector('Hit', a_move_chk, a_atk_ing_chk, def_chk, a_Hit)
        root = Hit_chk = Sequence('Hit chk', c_boy_atk_chk, Hit)

        root = Knockdown = Sequence('Knockdown', a_knockdown, a_Revive)

        root = Selector('Enemy BT', Knockdown, stun_chk, Hit_chk, Non_Hit)

        self.bt = BehaviorTree(root)