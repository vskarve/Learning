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

class Textbox:
    def __init__(self, surface: pygame.surface, dimensions: tuple[int, int, int, int], **kwargs):
        self.surface = surface
        self.options: Textbox_options = Textbox_options(**kwargs)
        self.text: str = ""
        self.split_text: list = []

        self.x_position = dimensions[0]
        self.y_position = dimensions[1]
        self.width = dimensions[2]
        self.height = dimensions[3]

        self.background = pygame.Rect(self.x_position, self.y_position, self.width, self.height)
        self.frame = self.background.inflate(2*self.options.frame_thickness, 2*self.options.frame_thickness)

    def draw(self):
        self._draw_box()
        self._draw_text()
    
    def append_text(self, text: str):
        self.text += text
        self._format_text()

    def set_text(self, text:str):
        self.text = text
        self._format_text()
    
    def erase_text(self):
        self.text = ""
        self._format_text()

    def set_position(self, x: int, y: int):
        self.x_position = x
        self.y_position = y
        self.background = pygame.Rect(self.x_position, self.y_position, self.width, self.height)
        self.frame = self.background.inflate(2*self.options.frame_thickness, 2*self.options.frame_thickness)

    def move(self, dx: int, dy:int):
        self.x_position += dx
        self.y_position += dy
        self.background.x += dx
        self.background.y += dy
        self.frame.x += dx
        self.frame.y += dy

    def _format_text(self):
        self.split_text = self.text.split(self.options.endline_character)
        #Uppdatera denna så att den delar upp texten efter längd också

    def _draw_text(self):
        font = pygame.font.SysFont(self.options.font, self.options.text_size)

        for i, line in enumerate(self.split_text):
            image = font.render(line, self.options.smooth, self.options.text_color, self.options.highlight_marker_color)
            self.surface.blit(image, (self.x_position, self.y_position + font.get_height()*i))

    def _draw_box(self):
        pygame.draw.rect(self.surface, self.options.frame_color, self.frame)
        pygame.draw.rect(self.surface, self.options.background_color, self.background)



def main():
    pygame.init()

    win = pygame.display.set_mode((500, 500))

    textbox = Textbox(win, (50, 50, 100, 100))
    textbox.set_text("HEJ PÅ DIG")

    running = True
    while running:
        pygame.time.delay(100)
        win.fill((34, 122, 70))
        textbox.set_text(random_string(5))
        textbox.move(1, 1)
        textbox.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
        pygame.display.update()
    
    pygame.quit()

if __name__ == "__main__":
    main()