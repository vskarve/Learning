import pygame
from textbox.textbox import Textbox
from utils.utils import random_string
import random

def main():
    pygame.init()

    win = pygame.display.set_mode((500, 500))
    textbox = Textbox(win, 10, 10, 400, 300)
    textbox.add_text("HEJ PÅ dig\nHur mr duddddddddddddfffffff?")
    textbox.config(sticky_bottom = False)
    textbox.config(thumb_scale = 2.5)
    print(textbox.interface.scroll_bar.thumb.options.thumb_scale)
    count = 0
    running = True
    while running:
        if count % 10 == 0:
            textbox.add_text(random_string(random.randint(1, 18)))

        win.fill((34, 122, 70))
        textbox.draw()
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
        pygame.display.update()
        pygame.time.delay(30)
        count += 1
    
    pygame.quit()

if __name__ == "__main__":
    main()

#skapa get_attr i textbox