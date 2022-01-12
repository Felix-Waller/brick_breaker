class Brick:
    colours = ["green", "yellow", "red", "gray", "black"]

    def __init__(self, root, canvas, x, y):
        self.root = root
        self.canvas = canvas
        self.width = 40
        self.height = 10
        self.strength = 4
        self.coords = [x, y, x + self.width, y + self.height]
        self.brick = self.canvas.create_rectangle(
            self.coords[0], self.coords[1], self.coords[2],
            self.coords[3], fill=Brick.colours[self.strength - 1])

    def collision(self, strong):
        self.strength -= 1
        if strong or self.strength == 0:
            self.canvas.delete(self.brick)
        else:
            self.canvas.itemconfig(
                self.brick, fill=Brick.colours[self.strength - 1])
