from dataclasses import dataclass, fields

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
    sticky_botton: bool = False

    def get_fields(self):
        return fields(self)

@dataclass
class Frame_options:
    frame_color: tuple = (255, 0, 0)
    frame_thickness:int = 3

    def get_fields(self):
        return fields(self)

class Input_Options:
    def __init__(self, **kwargs):
        frame_fields = {f.name for f in fields(Frame_options)}
        canvas_fields = {f.name for f in fields(Canvas_options)}

        unknown = set(kwargs) - (frame_fields | canvas_fields)
        if unknown:
            raise ValueError(f"Unknown keys {unknown}")
        
        frame_kwargs = {k:v for k, v in kwargs.items() if k in frame_fields}
        canvas_kwargs = {k:v for k, v in kwargs.items() if k in canvas_fields}

        self.frame_options = Frame_options(**frame_kwargs)
        self.canvas_options = Canvas_options(**canvas_kwargs)