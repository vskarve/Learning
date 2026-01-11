import pygame
from .text_handler import Text_handler   # relative import from same package
from ..options import Canvas_options 

class Canvas:
    def __init__(self, width: int, height: int, options):
        self.options = options
        self.width = width
        self.height = height
        self.canvas_surface = pygame.Surface((width, height))
        self.scroll = 0
        self.have_been_scrolled = False

        self.font = pygame.font.SysFont(self.options.font, self.options.text_size)
        max_line_length = self.width - self.options.x_indent - self.options.end_line_padding
        self.text_handler = Text_handler(max_line_length, self.font)

    def draw(self, root, x: int, y: int):
        self.canvas_surface.fill(self.options.background_color)

        if self.options.auto_scroll and not self.have_been_scrolled:
            self.scroll = self.get_max_scroll(self.options.sticky_bottom)
        self.draw_text()

        root.blit(self.canvas_surface, (x, y))

    def add_text(self, text):
        self.text_handler.add_text(text)

    def draw_text(self):
        padx = self.options.x_indent
        pady = self.scroll

        paragraphs = self.text_handler.get_paragraphs()

        for line in paragraphs:

            text_surface = self.font.render(line, self.options.antialias, self.options.text_color)
            self.canvas_surface.blit(text_surface, (padx, pady))
            pady += self.options.line_spacing

    def set_scroll(self, scroll: int) -> None:
        self.scroll = scroll

    def add_scroll(self, dscroll: int) -> None:
        self.scroll += dscroll
    
    def get_max_scroll(self, sticky_botton = False) -> float:
        nr_lines = self.text_handler.count_lines()
        scroll = self.height - nr_lines * self.options.line_spacing

        if not sticky_botton:
            scroll = min(0, scroll)
        
        return scroll
    
    def get_min_scroll(self, sticky_botton = False):
        if not sticky_botton:
            return 0
        else:

            return max(0, self.get_max_scroll(sticky_botton))
    
    def get_scroll(self) -> int:
        return self.scroll