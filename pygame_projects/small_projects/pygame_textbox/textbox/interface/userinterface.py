import pygame
import time

from .scroll_bar import Scroll_bar
from ..options import Interface_options

class Interface:
    def __init__(self, x:int, y:int, parent_textbox, height: int, options):
        self.options = options.user_options
        self.current_scroll_speed = self.options.scroll_speed

        self.time_last_scroll = 0

        self.parent_textbox = parent_textbox
        self.scroll_bar = Scroll_bar(options.bar_options, options.thumb_options)

    def handle_event(self, event) -> None:
        if self.options.mouse_scroll and event.type == pygame.MOUSEWHEEL:
            self.set_current_scroll_speed()
            self.parent_textbox.scroll_by(event.y * self.current_scroll_speed)


    def set_current_scroll_speed(self):
        delta_time = time.time() - self.time_last_scroll
        self.time_last_scroll = time.time()

        if delta_time < self.options.scroll_timeout:
            self.current_scroll_speed *= self.options.scroll_acceleration
        else:
            self.current_scroll_speed = self.options.scroll_speed

        print(self.current_scroll_speed)
    
    def scroll_damping(self):
        if self.options.scroll_inertia:
            pass
    
    @classmethod
    def get_field_names(cls):
        return Interface_options.get_fields_names()