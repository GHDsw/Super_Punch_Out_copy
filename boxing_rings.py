from pico2d import load_image


class Rings:
    def __init__(self):
        self.image = load_image('test_ring.png')

    def draw(self):
        self.image.draw(400, 300)

    def update(self):
        pass
