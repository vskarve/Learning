import pygame
from dataclasses import dataclass

@dataclass
class Textbox_options:
    background_color: tuple = (0, 0, 0)

    frame_color: tuple = (0, 0, 0)
    frame_thickness:int = 0

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

        self.x_position = dimensions[0]
        self.y_position = dimensions[1]
        self.width = dimensions[2]
        self.height = dimensions[3]

    def draw(self):
        font = pygame.font.SysFont(self.options.font, self.options.text_size)
        message = self.text.split(self.options.endline_character)

        for i, line in enumerate(message):
            image = font.render(line, self.options.smooth, self.options.text_color, self.options.highlight_marker_color)
            self.surface.blit(image, (self.x_position, self.y_position + font.get_height()*i))
    
    def append_text(self, text: str):
        self.text += text

    def set_text(self, text:str):
        self.text = text
    
    def erase_text(self):
        self.text = ""



def main():
    pygame.init()

    win = pygame.display.set_mode((500, 500))

    textbox = Textbox(win, (50, 50, 100, 100))
    textbox.set_text("HEJ PÅ DIG")

    running = True
    while running:
        win.fill((34, 122, 70))
        textbox.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
        pygame.display.update()
    
    pygame.quit()

if __name__ == "__main__":
    main()