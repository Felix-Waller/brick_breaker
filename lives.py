from colour import Colour


class Lives:
    def __init__(self, canvas):
        self.canvas = canvas
        self.lives_count = 5
        self.lives = self.canvas.create_text(
            700, 30, text=f"Lives: {self.lives_count}", font=("Purisa", 20),
            fill=Colour.text_colour, anchor="e")

    def decrement(self):
        self.lives_count -= 1
        self.canvas.itemconfigure(
            self.lives, text=f"Lives: {self.lives_count}")
