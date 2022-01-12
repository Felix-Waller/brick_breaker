from colour import Colour


class Paddle:
    def __init__(self, root, canvas, x, y):
        self.root = root
        self.canvas = canvas
        self.speed = 0
        self.width = 80
        self.height = 20
        self.coords = [x, y, x + self.width, y + self.height]
        self.paused = False
        self.paddle = self.canvas.canvas.create_rectangle(
            self.coords[0], self.coords[1], self.coords[2], self.coords[3],
            fill=Colour.paddle)
        self.root.bind("<Control-l>", self.long)

    def long(self, event):
        """Toggles the paddle between
        normal and long widths"""
        self.width = 160 if self.width == 80 else 80
        if self.width == 160:
            self.canvas.canvas.itemconfigure(
                self.paddle, fill=Colour.paddle_long)
            self.coords = [
                self.coords[0] - 40, self.coords[1],
                self.coords[2] + 40, self.coords[3]]
            if self.coords[0] < 0:
                self.coords[0] = 0
                self.coords[2] = 160
            elif self.coords[2] > 720:
                self.coords[0] = 560
                self.coords[2] = 720
        else:
            self.canvas.canvas.itemconfigure(self.paddle, fill=Colour.paddle)
            self.coords = [
                self.coords[0] + 40, self.coords[1],
                self.coords[2] - 40, self.coords[3]]
        self.canvas.canvas.coords(
            self.paddle, self.coords[0], self.coords[1], self.coords[2],
            self.coords[3])

    def load(self, data):
        self.canvas.paddle_speed = data["speed"]
        self.coords = data["coords"]
        self.canvas.canvas.coords(
            self.paddle, self.coords[0], self.coords[1], self.coords[2],
            self.coords[3])

    def pause(self, paused):
        self.paused = paused
        if not paused:
            self.move()

    def move(self):
        if self.paused:
            return

        if (self.coords[0] + self.canvas.paddle_speed < 720 - self.width +
           8 and self.coords[0] + self.canvas.paddle_speed > 4):
            self.canvas.canvas.move(self.paddle, self.canvas.paddle_speed, 0)
            self.coords[0] += self.canvas.paddle_speed
            self.coords[2] += self.canvas.paddle_speed
        self.root.after(15, self.move)
