from pico2d import *

import game_world

sprite_size = {'ring1': [[0, 0], [431, 175]],
               'ring2': [[0, 256], [431, 431]],
               'ring3': [[0, 512], [431, 687]],
               'ring4': [[0, 768], [431, 944]],
               }

class Grass:
    def __init__(self):

        self.image = load_image('./image/Boxing_Rings.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(400, 30)
        self.image.draw(1200, 30)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return 0, 0, 1600-1, 60

    def handle_collision(self, group, other):
        pass