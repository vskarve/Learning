import pygame
from .scroll_bar import Scroll_bar
from ..options import Interface_options

class Interface:
    def __init__(self, x:int, y:int, height: int, options):
        self.has_scroll_bar: bool = options.has_scroll_bar
        self.scroll_speed: int = options.scroll_speed
        self.scroll_bar = Scroll_bar(options.bar_options, options.thumb_options)

    def handle_event(self, event) -> None:
        pass

    def setattr(self, key, value):   
        interface_fields = Interface_options.interface_fields

        if key in interface_fields:
            super().__setattr__(key, value)
        else:
            self.scroll_bar.setattr(key, value)
    
    @classmethod
    def get_field_names(cls):
        return Interface_options.get_fields_names()