from dataclasses import dataclass, fields
from typing import Literal

@dataclass
class Canvas_options:
    background_color: tuple = (0, 0, 0)

    text_size: int = 12
    font: str = "Arial"
    text_color: tuple = (255, 255, 255)
    highlight_marker_color: tuple = None
    antialias: bool = True
    line_spacing = None

    x_indent: int = 1

    auto_scroll: bool = True
    sticky_bottom: bool = False

@dataclass
class Frame_options:
    frame_color: tuple = (255, 0, 0)
    frame_thickness:int = 3

@dataclass
class Bar_options:
    bar_orientation: Literal["vertical", "horizontal"] = "vertical"
    bar_side: Literal["left", "right", "top", "bottom"] = "left"

    bar_color: tuple[int, int, int] = (255, 0, 0)

    displacement: int = 10

@dataclass
class Thumb_options:
    thumb_scale: float = 0.25
    thumb_padding: int = 3
    
    thumb_color: tuple[int, int, int] = (0, 255, 0)

    def __post_init__(self):
        self.thumb_scale = max(0.05, min(1, self.thumb_scale))

class Interface_options:

    interface_fields = {"has_scroll_bar", "scroll_speed"}

    def __init__(self, **kwargs):
        self.has_scroll_bar: bool = True 
        self.scroll_speed: int = 10

        bar_fields = {f.name for f in fields(Bar_options)}
        thumb_fields = {f.name for f in fields(Thumb_options)}

        unknown = set(kwargs) - (bar_fields | thumb_fields | Interface_options.interface_fields)
        if unknown:
            raise ValueError(f"Unknown keys {unknown}")
        
        bar_kwargs = {k:v for k, v in kwargs.items() if k in bar_fields}
        thumb_kwargs = {k:v for k, v in kwargs.items() if k in thumb_fields}
        interface_kwargs = {k:v for k, v in kwargs.items() if k in Interface_options.interface_fields}

        self.bar_options: Bar_options = Bar_options(**bar_kwargs)
        self.thumb_options: Thumb_options = Thumb_options(**thumb_kwargs)

        for k, v in interface_kwargs.items():
            setattr(self, k, v)

    @classmethod
    def get_fields_names(cls):
        keys = cls.interface_fields | {f.name for f in fields(Bar_options)} | {f.name for f in fields(Thumb_options)}
        return keys



class Input_Options:
    def __init__(self, **kwargs):
        frame_fields = {f.name for f in fields(Frame_options)}
        canvas_fields = {f.name for f in fields(Canvas_options)}
        interface_fields = Interface_options.get_fields_names()

        unknown = set(kwargs) - (frame_fields | canvas_fields | interface_fields)
        if unknown:
            raise ValueError(f"Unknown keys {unknown}")
        
        frame_kwargs = {k:v for k, v in kwargs.items() if k in frame_fields}
        canvas_kwargs = {k:v for k, v in kwargs.items() if k in canvas_fields}
        interface_kwargs = {k:v for k, v in kwargs.items() if k in interface_fields}

        self.frame_options = Frame_options(**frame_kwargs)
        self.canvas_options = Canvas_options(**canvas_kwargs)
        self.interface_options = Interface_options(**interface_kwargs)