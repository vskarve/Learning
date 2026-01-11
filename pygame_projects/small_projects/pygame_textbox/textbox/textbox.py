import pygame
from dataclasses import fields

from .the_textbox.canvas import Canvas
from .the_textbox.frame import Frame
from .interface.userinterface import Interface
from .options import Input_Options

class Textbox:
    def __init__(self, root, x: int, y: int, width: int, height: int, **kwargs):
        extra_options = Input_Options(**kwargs)
        if extra_options.canvas_options.line_spacing == None:
            extra_options.canvas_options.line_spacing = pygame.font.SysFont(extra_options.canvas_options.font, extra_options.canvas_options.text_size).get_linesize()

        canvas_width = width - 2 * extra_options.frame_options.frame_thickness
        canvas_height = height - 2 * extra_options.frame_options.frame_thickness

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.root = root
        self.canvas = Canvas(canvas_width, canvas_height, extra_options.canvas_options)
        self.frame = Frame(x, y, width, height, extra_options.frame_options)
        self.interface = Interface(x, y, self, height, extra_options.interface_options)

    def draw(self):
        self.update_processes()
        canvas_x_pos = self.frame.rectangle.x + self.frame.options.frame_thickness
        canvas_y_pos = self.frame.rectangle.y + self.frame.options.frame_thickness

        self.canvas.draw(self.root, canvas_x_pos, canvas_y_pos)
        self.frame.draw(self.root)

    def add_text(self, text):
        self.canvas.add_text(text)

    def config(self, **kwargs):
        frame_fields= {f.name for f in fields(self.frame.options)}
        canvas_fields = {f.name for f in fields(self.canvas.options)}
        interface_fields = {f for f in self.interface.get_field_names()}
        argument_keys = set(kwargs)

        unknown = argument_keys - (frame_fields | canvas_fields | interface_fields)

        if unknown:
            raise ValueError(f"Unknown keys {unknown}")
        
        for key in argument_keys & frame_fields:
            setattr(self.frame.options, key, kwargs[key])

        for key in argument_keys & canvas_fields:
            setattr(self.canvas.options, key, kwargs[key])
        
        for key in argument_keys & interface_fields:
            self.interface.setattr(key, kwargs[key])

    def handle_event(self, event):
        self.interface.handle_event(event)

    def scroll_by(self, dscroll):
        max_scroll = self.canvas.get_max_scroll(sticky_botton=self.canvas.options.sticky_bottom)
        min_scroll = self.canvas.get_min_scroll(sticky_botton=self.canvas.options.sticky_bottom)
        
        if self.canvas.scroll + dscroll > max_scroll:
            self.canvas.have_been_scrolled = True
            if self.canvas.scroll + dscroll > min_scroll:
                self.canvas.scroll = min_scroll
            else:
                self.canvas.scroll += dscroll
        else:
            self.canvas.scroll = max_scroll
            self.canvas.have_been_scrolled = False

    def update_processes(self):
        '''Runs every time textbox.draw is called, making other class processes happen over time'''
        self.interface.scroll_damping()
        
        
        



    
        