import pygame

class Text_handler:
    def __init__(self, max_width: int, font):
        self.max_width = max_width
        self.font = font

        self.text = ""
        self.split_text = []

    def add_text(self, text: str) -> None:
        if self.text:
            self.text += "\n" + text
        else:
            self.text = text
        self.split_text.extend(self._wrap_text(text))

    def continue_text(self, text: str) -> None:
        self.text += text
        wrap = self.split_text.pop() + text
        self.split_text.extend(self._wrap_text(wrap))

    def clear_text(self) -> None:
        self.text = ""
        self.split_text.clear()

    def get_text(self) -> str:
        return self.text
    
    def get_paragraphs(self) -> list[str]:
        return self.split_text
    
    def count_lines(self) -> int:
        return len(self.split_text)

    def _wrap_text(self, text: str) -> list[str]:
        
        lines = []

        for paragraph in text.split("\n"):
            if paragraph == "":
                #keeps the black line
                lines.append("")
                continue
            
            lines.extend(self._wrap_paragraph(paragraph))

        return lines
    
    def _wrap_paragraph(self, paragraph: str) -> list[str]:
        words = paragraph.split(" ")
        lines = []
        current_line = ""

        for word in words:
            if not current_line:
                candidate = word
            else:
                candidate = current_line + " " + word

            if self._fits(candidate):
                current_line = candidate
            else:
                if current_line:
                    lines.append(current_line)
                    current_line = ""

                if not self._fits(word):
                    split_parts = self._split_long_word(word)
                    lines.extend(split_parts[:-1])
                    current_line = split_parts[-1]
                else:
                    current_line = word

        if current_line:
            #If loop ends and still chars in current_line
            lines.append(current_line)

        return lines
    
    def _split_long_word(self, word: str) -> list[str]:
        parts = []
        current = ""

        for char in word:
            candidate = current + char
            if self._fits(candidate + "-"):
                current = candidate
            else:
                parts.append(current + "-")
                current = char
        
        if current:
            parts.append(current)

        return parts

    def _fits(self, text: str) -> bool:
        return self.font.size(text)[0] <= self.max_width