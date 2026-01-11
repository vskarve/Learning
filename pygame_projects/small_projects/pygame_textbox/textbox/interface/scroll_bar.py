import pygame
from dataclasses import fields
from ..options import Interface_options, Bar_options, Thumb_options

class Bar:
    def __init__(self, options):
        self.options = options

class Thumb:
    def __init__(self, options):
        self.options = options

class Scroll_bar:
    def __init__(self, bar_options, thumb_options):
        self.bar = Bar(bar_options)
        self.thumb = Thumb(thumb_options)

    def setattr(self, key, value):
        bar_fields = {f.name for f in fields(Bar_options)}
        thumb_fields = {f.name for f in fields(Thumb_options)}

        if key in bar_fields:
            setattr(self.bar.options, key, value)
            self.bar.options.__post_init__()
        if key in thumb_fields:
            setattr(self.thumb.options, key, value)
            self.thumb.options.__post_init__()
