import pygame
from .scroll_bar import Scroll_bar

class Interface:
    def __init__(self):
        self.scroll_bar = Scroll_bar()

    def handle_event(self, event) -> None:
        pass