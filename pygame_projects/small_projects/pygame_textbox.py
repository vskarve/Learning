import pygame
from dataclasses import dataclass

##########################
import random
import string

def random_string(n):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=n))
############################

@dataclass
class Textbox_options:
    background_color: tuple = (0, 0, 0)

    frame_color: tuple = (255, 0, 0)
    frame_thickness:int = 3

    text_size: int = 12
    font: str = "Arial"
    text_color: tuple = (255, 255, 255)
    highlight_marker_color: tuple = None
    smooth: bool = True

    endline_character: str = "\n"
    x_indent: int = 1

class Textbox:
    def __init__(self, surface: pygame.surface, dimensions: tuple[int, int, int, int], **kwargs):
        self.surface = surface
        self.options: Textbox_options = Textbox_options(**kwargs)
        self.text: str = ""
        self.new_text: str = ""
        self.split_text: list = []

        self.x_position = dimensions[0]
        self.y_position = dimensions[1]
        self.width = dimensions[2]
        self.height = dimensions[3]
        self.scroll = 0

        self.box_surface = pygame.Surface((self.width, self.height))
        self.box_surface.fill(self.options.background_color)
        self.rect_frame = pygame.Rect(self.x_position, self.y_position, self.width, self.height)

        self.font = pygame.font.SysFont(self.options.font, self.options.text_size)

    def draw(self, auto_scroll: bool = True):
        if auto_scroll:
            pass

        self._update_text_surface()
        self.surface.blit(self.box_surface, (self.x_position, self.y_position))
        pygame.draw.rect(self.surface, self.options.frame_color, self.rect_frame, self.options.frame_thickness)
        print(self.text, self.split_text)
    
    def append_text(self, text: str):
        '''Adds to lates row, no space to previous text'''
        self.text += text

        if self.split_text:
            self.new_text = self.split_text[-1] + text
            self.split_text.pop()
        else:
            self.new_text = text
        self._format_text()
        
    def add_text(self, text:str):
        '''New row'''
        self.text += "\n" + text
        self.new_text = text
        self._format_text()

    def set_text(self, text:str):
        self.text = text
        self.new_text = text
        self.split_text.clear()
        self._format_text()
    
    def erase_text(self):
        self.text = ""
        self.new_text = ""
        self.split_text.clear()
        self._format_text()

    def set_position(self, x: int, y: int):
        self.x_position = x
        self.y_position = y
        self.rect_frame = pygame.Rect(self.x_position, self.y_position, self.width, self.height)

    def move(self, dx: int, dy:int):
        self.x_position += dx
        self.y_position += dy
        self.rect_frame.x += dx
        self.rect_frame.y += dy
    
    def _format_text(self):
        self.font = pygame.font.SysFont(self.options.font, self.options.text_size)
        #self.split_text = self.text.split(self.options.endline_character)
        max_line_length = self.width - (self.options.x_indent + 2 * self.options.frame_thickness)
        
        #Uppdatera denna så att den delar upp texten efter längd också

    def _update_text_surface(self):
        padx = self.options.x_indent + self.options.frame_thickness
        pady = self.scroll + self.options.frame_thickness
        self.box_surface.fill(self.options.background_color)
        for i, line in enumerate(self.split_text):
            image = self.font.render(line, self.options.smooth, self.options.text_color, self.options.highlight_marker_color)
            self.box_surface.blit(image, (padx, pady + self.font.get_linesize()*i))

    def _draw_box(self):
        pygame.draw.rect(self.surface, self.options.frame_color, self.frame)
        pygame.draw.rect(self.surface, self.options.background_color, self.background)



def main():
    pygame.init()

    win = pygame.display.set_mode((500, 500))

    textbox = Textbox(win, (50, 50, 100, 100))
    textbox.set_text("HEJ PÅ DIG\nHur")

    running = True
    while running:
        win.fill((34, 122, 70))
        textbox.append_text(random_string(2))
        textbox.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
        pygame.display.update()
        pygame.time.delay(1000)
    
    pygame.quit()

if __name__ == "__main__":
    main()