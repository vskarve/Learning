from dataclasses import dataclass, fields, is_dataclass
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
    end_line_padding:int = 0

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

@dataclass
class Userinterface_options:
    has_scroll_bar: bool = True 
    scroll_speed: int = 10
    scroll_acceleration: float = 1.6
    mouse_scroll: bool = True
    scroll_timeout: float = 0.1
    scroll_inertia: bool = False
    scroll_deacceleration: float = 0.75

class Data_manager:
    def split_and_check_kwargs(self, *args):
        '''Takes in class pointers and lastly kwargs, returns in passed order splitted kwargs'''
        outputed_kwargs = []

        dataclasses = args[:-1]
        kwargs = args[-1]

        organized_fields = []
        all_fields = set()
        for dataclass in dataclasses:
            if is_dataclass(dataclass):
                field_names = {f.name for f in fields(dataclass)}
            else:
                field_names = dataclass.get_field_names()
            organized_fields.append(field_names)
            outputed_kwargs.append({k:v for k, v in kwargs.items() if k in field_names})
            all_fields.update(field_names)
        
        unknown = set(kwargs) - all_fields
        if unknown:
            raise ValueError(f"Unknown keys {unknown}")
        
        return outputed_kwargs


class Interface_options(Data_manager):
    def __init__(self, **kwargs):
        bar_kwargs, thumb_kwargs, user_kwargs = self.split_and_check_kwargs(Bar_options, Thumb_options, Userinterface_options, kwargs)

        self.user_options: Userinterface_options = Userinterface_options(**user_kwargs)        
        self.bar_options: Bar_options = Bar_options(**bar_kwargs)
        self.thumb_options: Thumb_options = Thumb_options(**thumb_kwargs)


    @classmethod
    def get_field_names(cls):
        keys = {f.name for f in fields(Userinterface_options)} | {f.name for f in fields(Bar_options)} | {f.name for f in fields(Thumb_options)}
        return keys



class Input_Options(Data_manager):
    def __init__(self, **kwargs):
        frame_kwargs, canvas_kwargs, interface_kwargs = self.split_and_check_kwargs(Frame_options, Canvas_options, Interface_options, kwargs)

        self.frame_options = Frame_options(**frame_kwargs)
        self.canvas_options = Canvas_options(**canvas_kwargs)
        self.interface_options = Interface_options(**interface_kwargs)