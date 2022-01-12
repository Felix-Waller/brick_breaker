from tkinter import Button, Canvas, Label
from ball import Ball
from brick import Brick
from colour import Colour
from lives import Lives
from paddle import Paddle
from star import Star
from timer import Timer


class GameCanvas:
    def __init__(self, root, levels_unlocked, leaderboard,
                 paddle_left_key, paddle_right_key):
        self.root = root
        self.levels_unlocked = levels_unlocked
        self.current_level = 0
        self.leaderboard = leaderboard
        self.msg = "Welcome"
        self.paddle_right_key = paddle_right_key
        self.paddle_left_key = paddle_left_key
        self.paddle_speed = 0
        self.canvas = Canvas(
            self.root, width=720, height=720, bd=4,
            relief="groove", bg=Colour.canvas_background)
        self.canvas.pack()
        self.ball = None
        self.label = Label(
            self.canvas, text=self.msg, font=("Purisa", 20),
            bg=Colour.canvas_background, fg=Colour.text_colour)
        self.level1_button = Button(
            self.canvas, text="Play Level 1", font=("Purisa", 14),
            fg=Colour.text_colour, bg=Colour.button_colour,
            command=self.level1)
        self.level2_button = Button(
            self.canvas, text="Play Level 2", font=("Purisa", 14),
            fg=Colour.text_colour, bg=Colour.button_colour,
            command=self.level2,
            state="disabled")
        self.level3_button = Button(
            self.canvas, text="Play Level 3", font=("Purisa", 14),
            fg=Colour.text_colour, bg=Colour.button_colour,
            command=self.level3,
            state="disabled")
        self.root.bind(self.paddle_left_key, self.paddle_left)
        self.root.bind(self.paddle_right_key, self.paddle_right)
        self.level_unlock()

    def paddle_right(self, event):
        self.paddle_speed = 5

    def paddle_left(self, event):
        self.paddle_speed = -5

    def save(self, pause_key, boss_key):
        """Save game data to dictionary"""
        if self.current_level:
            data = {
                "ball": {
                    "coords": self.ball.coords,
                    "facing": self.ball.facing,
                    "speed": self.ball.speed,
                    "stored_facing": self.ball.stored_facing,
                    "score": self.ball.score,
                    "lives": self.ball.lives},
                "paddle": {
                    "speed": self.paddle.speed,
                    "coords": self.paddle.coords},
                "timer": {
                    "time": self.timer.current_time - self.timer.start_time -
                    self.timer.time_paused,
                    "final": self.timer.final_time},
                "stars": [],
                "bricks": [],
                "keybinds": {
                    "left": self.paddle_left_key,
                    "right": self.paddle_right_key,
                    "pause": pause_key,
                    "boss": boss_key},
                "level": self.current_level,
                "unlocked": self.levels_unlocked}

            for star in self.stars:
                data["stars"].append({"coords": star.coords, "hit": star.hit})

            for brick in self.bricks:
                if brick.strength:
                    data["bricks"].append(
                        {"strength": brick.strength, "coords": brick.coords})
        else:
            data = {
                "keybinds": {
                    "left": self.paddle_left_key,
                    "right": self.paddle_right_key,
                    "pause": pause_key,
                    "boss": boss_key},
                "level": self.current_level,
                "unlocked": self.levels_unlocked}

        return data

    def loaded_level(self, data):
        """Load a level from a dictionary"""
        self.current_level = data["level"]

        self.label.place_forget()
        self.level1_button.place_forget()
        self.level2_button.place_forget()
        self.level3_button.place_forget()

        self.canvas.delete("all")

        self.bricks = [Brick(
            self.root, self.canvas, brick["coords"][0],
            brick["coords"][1]) for brick in data["bricks"]]

        for brick in range(len(self.bricks)):
            self.bricks[brick].strength = data["bricks"][brick]["strength"] + 1
            self.bricks[brick].collision(False)

        self.stars = []
        for star in range(3):
            if not data["stars"][star]["hit"]:
                self.stars.append(Star(
                    self.root, self.canvas,
                    data["stars"][star]["coords"][0],
                    data["stars"][star]["coords"][1]))

        self.paddle = Paddle(self.root, self, 0, 0)
        self.paddle.load(data["paddle"])

        self.timer = Timer(self.root, self.canvas)
        self.timer.load(data["timer"])

        lives = Lives(self.canvas)
        lives.lives_count = data["ball"]["lives"] + 1
        lives.decrement()

        self.ball = Ball(
            self.root, self, self.leaderboard,
            self.bricks, self.stars, self.paddle, self.timer, lives)
        self.ball.load(data["ball"])

    def load(self, data):
        self.paddle_left_key = data["keybinds"]["left"]
        self.paddle_right_key = data["keybinds"]["right"]

        self.root.bind(self.paddle_left_key, self.paddle_left)
        self.root.bind(self.paddle_right_key, self.paddle_right)

        if data["level"]:
            self.loaded_level(data)
        else:
            self.current_level = data["level"]
            self.levels_unlocked = data["unlocked"]

    def level1(self):
        """Display level 1"""
        self.current_level = 1
        self.label.place_forget()
        self.level1_button.place_forget()
        self.level2_button.place_forget()
        self.level3_button.place_forget()

        brick_coords = [[340 + 20 * i, 360 - 10 * i] for i in range(12)]
        brick_coords.extend([[320 - 20 * i, 350 - 10 * i] for i in range(11)])

        self.bricks = [
            Brick(self.root, self.canvas, i[0], i[1]) for i in brick_coords]

        self.stars = [
            Star(self.root, self.canvas, 200, 200),
            Star(self.root, self.canvas, 360, 200),
            Star(self.root, self.canvas, 520, 200)]

        self.paddle = Paddle(self.root, self, 360, 620)
        self.paddle_speed = 0
        self.paddle.move()

        self.timer = Timer(self.root, self.canvas)
        self.timer.start()

        lives = Lives(self.canvas)
        self.ball = Ball(
            self.root, self, self.leaderboard, self.bricks, self.stars,
            self.paddle, self.timer, lives)
        self.ball.move()

    def level2(self):
        """Display level 2"""
        self.current_level = 2
        self.label.place_forget()
        self.level1_button.place_forget()
        self.level2_button.place_forget()
        self.level3_button.place_forget()

        brick_coords = [[184 + 16 * i, 40 + 10 * i] for i in range(27)]
        brick_coords.extend([[104 + 16 * i, 100 + 10 * i] for i in range(26)])
        brick_coords.extend([[160 - 16 * i, 50 + 10 * i] for i in range(5)])
        brick_coords.extend([[576 - 16 * i, 310 + 10 * i] for i in range(4)])

        self.bricks = [
            Brick(self.root, self.canvas, i[0], i[1]) for i in brick_coords]

        self.stars = [
            Star(self.root, self.canvas, 200, 100),
            Star(self.root, self.canvas, 360, 200),
            Star(self.root, self.canvas, 520, 300)]

        self.paddle = Paddle(self.root, self, 360, 620)
        self.paddle_speed = 0
        self.paddle.move()

        self.timer = Timer(self.root, self.canvas)
        self.timer.start()

        lives = Lives(self.canvas)

        self.ball = Ball(
            self.root, self, self.leaderboard, self.bricks, self.stars,
            self.paddle, self.timer, lives)
        self.ball.move()

    def level3(self):
        """Display level 3"""
        self.current_level = 3
        self.label.place_forget()
        self.level1_button.place_forget()
        self.level2_button.place_forget()
        self.level3_button.place_forget()

        brick_coords = [
            [320, 50], [360, 50],
            [300, 60], [340, 60], [380, 60],
            [280, 70], [400, 70],
            [280, 80], [400, 80],
            [260, 90], [420, 90],
            [260, 100], [420, 100],
            [280, 110], [400, 110],
            [280, 120], [400, 120],
            [300, 130], [340, 130], [380, 130],
            [320, 140], [360, 140],

            [480, 150], [520, 150],
            [460, 160], [500, 160], [540, 160],
            [440, 170], [560, 170],
            [440, 180], [560, 180],
            [420, 190], [580, 190],
            [420, 200], [580, 200],
            [440, 210], [560, 210],
            [440, 220], [560, 220],
            [460, 230], [500, 230], [540, 230],
            [480, 240], [520, 240],

            [160, 240], [200, 240],
            [140, 250], [180, 250], [220, 250],
            [120, 260], [240, 260],
            [120, 270], [240, 270],
            [100, 280], [260, 280],
            [100, 290], [260, 290],
            [120, 300], [240, 300],
            [120, 310], [240, 310],
            [140, 320], [180, 320], [220, 320],
            [160, 330], [200, 330],
        ]
        self.bricks = [
            Brick(self.root, self.canvas, i[0], i[1]) for i in brick_coords]

        self.stars = [
            Star(self.root, self.canvas, 200, 290),
            Star(self.root, self.canvas, 360, 100),
            Star(self.root, self.canvas, 520, 200)]

        self.paddle = Paddle(self.root, self, 360, 620)
        self.paddle_speed = 0
        self.paddle.move()

        self.timer = Timer(self.root, self.canvas)
        self.timer.start()

        lives = Lives(self.canvas)

        self.ball = Ball(
            self.root, self, self.leaderboard, self.bricks, self.stars,
            self.paddle, self.timer, lives)
        self.ball.move()

    def update_unlocked_levels(self):
        """Unlocks levels as player progresses"""
        if self.current_level == 1 and self.levels_unlocked < 2:
            self.levels_unlocked = 2
        elif self.current_level == 2 and self.levels_unlocked < 3:
            self.levels_unlocked = 3

    def level_unlock(self):
        """Activates level buttons as levels are unlocked"""
        if self.levels_unlocked > 1:
            self.level2_button["state"] = "normal"
        if self.levels_unlocked > 2:
            self.level3_button["state"] = "normal"
        self.canvas.delete("all")
        self.level_select()

    def level_select(self):
        """Display level select screen"""
        self.label.configure(text=self.msg)
        self.current_level = 0
        self.label.place(x=360, y=120, anchor="center")
        self.level1_button.place(x=360, y=240, anchor="center")
        self.level2_button.place(x=360, y=360, anchor="center")
        self.level3_button.place(x=360, y=480, anchor="center")
