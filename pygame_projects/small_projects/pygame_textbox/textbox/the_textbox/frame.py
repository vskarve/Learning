import pygame

class Frame:
    def __init__(self, x: int, y: int, width: int, height: int, extra_options):
        self.options = extra_options

        self.rectangle = pygame.Rect(x, y, width, height)

    def draw(self, root):
        pygame.draw.rect(root, self.options.frame_color, self.rectangle, self.options.frame_thickness)