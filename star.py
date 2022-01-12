from tkinter import PhotoImage


class Star:
    def __init__(self, root, canvas, x, y):
        self.root = root
        self.canvas = canvas
        self.hit = False
        self.coords = [x, y]
        self.image = PhotoImage(file="assets/star.png")
        self.star = self.canvas.create_image(
            x, y, image=self.image, anchor="center")

    def collision(self):
        self.canvas.delete(self.star)
        self.hit = True
