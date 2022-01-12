from tkinter import simpledialog, messagebox
import time
from colour import Colour


class Ball:
    def __init__(self, root, canvas, leaderboard, bricks,
                 stars, paddle, timer, lives_count):
        self.root = root
        self.canvas = canvas
        self.leaderboard = leaderboard
        self.bricks = bricks
        self.stars = stars
        self.timer = timer
        self.lives_count = lives_count
        self.paused = False
        self.star_ids = [star.star for star in stars]
        self.paddle = paddle
        self.coords = [354, 540, 374, 560]
        self.facing = [1, -1]
        self.speed = [4, 5]
        self.stored_facing = [1, -1]
        self.lives = 5
        self.last_collision_time = 0
        self.score = 0
        self.start_time = time.time_ns()
        self.elapsed_time = 0
        self.phasing = False
        self.is_invincible = False
        self.is_strong = False
        self.ball = self.canvas.canvas.create_oval(
            self.coords[0], self.coords[1], self.coords[2], self.coords[3],
            fill=Colour.ball, outline=Colour.ball, width=2)
        self.root.bind("<Control-p>", self.phase)
        self.root.bind("<Control-i>", self.invincible)
        self.root.bind("<Control-s>", self.strong)

    def phase(self, event):
        """Toggles the ball between phasing states
        to control whether it bounces on collision"""
        self.phasing = not self.phasing
        if self.phasing:
            # phase and strong cheats are mutually exclusive
            self.root.unbind("<Control-s>")
            self.canvas.canvas.itemconfigure(self.ball, fill=Colour.ball_phase)
        else:
            self.root.bind("<Control-s>", self.strong)
            self.canvas.canvas.itemconfigure(self.ball, fill=Colour.ball)

    def invincible(self, event):
        """Toggles the ball between is_invicible states
        to control whether the player loses a life when
        it hits the bottom of the screen"""
        self.is_invincible = not self.is_invincible
        if self.is_invincible:
            self.canvas.canvas.itemconfigure(
                self.ball,
                outline=Colour.ball_border_invincible)
        else:
            self.canvas.canvas.itemconfigure(self.ball, outline=Colour.ball)

    def strong(self, event):
        """Toggles the ball between is_strong states
        to control whether the ball instantly destroys bricks"""
        self.is_strong = not self.is_strong
        if self.is_strong:
            # phase and strong cheats are mutually exclusive
            self.root.unbind("<Control-p>")
            self.canvas.canvas.itemconfigure(self.ball,
                                             fill=Colour.ball_strong)
        else:
            self.root.bind("<Control-p>", self.phase)
            self.canvas.canvas.itemconfigure(self.ball, fill=Colour.ball)

    def load(self, data):
        """Load data from a dictionary"""
        self.coords = data["coords"]
        self.facing = (data["facing"] if data["facing"] != [0, 0]
                       else data["stored_facing"])
        self.speed = data["speed"]
        self.stored_facing = (data["stored_facing"] if data["stored_facing"] !=
                              [0, 0] else data["facing"])
        self.score = data["score"]
        self.lives = data["lives"]
        self.canvas.canvas.coords(self.ball, self.coords[0], self.coords[1],
                                  self.coords[2], self.coords[3])

    def game_over(self):
        self.canvas.canvas.delete("all")
        self.canvas.msg = "YOU LOSE!"
        self.canvas.level_unlock()
        self.paused = True

    def win(self):
        temp = self.canvas.current_level
        self.canvas.canvas.delete(self.ball)
        self.timer.stop()
        self.canvas.msg = f"YOU WIN!\nTime: {self.timer.final_time}"
        # Check if winning this level unlocks the next
        self.canvas.update_unlocked_levels()
        self.canvas.level_unlock()
        name = simpledialog.askstring(
            title="You Won!",
            prompt="Enter your name. Spaces will be removed.")
        self.leaderboard.update(temp, name, self.timer.final_time)

    def reset(self):
        self.canvas.canvas.coords(self.ball, 354, 540, 374, 560)
        self.coords = [354, 540, 374, 560]
        self.facing = [1, -1]
        self.speed = [4, 5]
        self.last_collision_time = 0
        self.root.after(1000, self.move)

    def out_of_bounds(self):
        self.lives -= 1
        self.lives_count.decrement()
        if self.lives == 0:
            self.game_over()
        else:
            self.reset()

    def check_collision(self):
        def bounce(coords):
            """Controls the movement
            subsequent to collision"""
            a = self.coords
            b = [coords[0] + self.speed[0], coords[1] + self.speed[1],
                 coords[2] - self.speed[0], coords[3] - self.speed[1]]

            if a[3] <= b[1]:
                self.facing[1] = -1
            elif a[1] >= b[3]:
                self.facing[1] = 1
            elif a[0] >= b[2]:
                self.facing[0] = 1
            else:
                self.facing[0] = -1

        def overlapping(coords):
            """Confirms if bounding boxes are overlapping
            rather than relying on tkinter's builtin method"""
            return ((self.coords[2] >= coords[0] and
                    self.coords[0] <= coords[2]) and
                    (self.coords[3] >= coords[1] and
                    self.coords[1] <= coords[3]))

        collisions = self.canvas.canvas.find_overlapping(
            self.coords[0], self.coords[1], self.coords[2], self.coords[3])
        collisions = [x for x in collisions if x is not self.ball]

        coords = None
        for id in collisions:
            if id == self.paddle.paddle:
                if overlapping(self.paddle.coords):
                    coords = self.paddle.coords
            # Ignore text at top of screen
            elif id == self.timer.timer or id == self.lives_count.lives:
                continue
            elif id in self.star_ids:
                for star in self.stars:
                    if star.star == id:
                        star.collision()
                        self.score += 1
                        if self.score == 3:
                            self.win()
                            return
        for brick in self.bricks:
            if brick.brick in collisions and not self.phasing:
                brick.collision(self.is_strong)
                coords = brick.coords

        if coords and not self.phasing:
            bounce(coords)

        if len(collisions) != 0:  # Reset collision timer
            self.last_collision_time = time.time_ns()

    def pause(self, paused):
        self.paused = paused
        if paused:
            self.stored_facing = self.facing
            self.facing = [0, 0]
        else:
            self.facing = self.stored_facing
            self.move()

    def move(self):
        if self.coords[2] >= 716 or self.coords[0] <= 4:
            self.facing[0] *= -1

        if self.coords[1] >= 696:
            if self.is_invincible:
                self.facing[1] *= -1
            else:
                self.out_of_bounds()
                return
        elif self.coords[1] <= 4:
            self.facing[1] *= -1

        self.a = time.time_ns()
        if self.a - self.last_collision_time >= 30000000:
            self.check_collision()

        self.canvas.canvas.move(self.ball, self.facing[0] * self.speed[0],
                                self.facing[1] * self.speed[1])
        self.coords = [self.coords[0] + self.facing[0] * self.speed[0],
                       self.coords[1] + self.facing[1] * self.speed[1],
                       self.coords[2] + self.facing[0] * self.speed[0],
                       self.coords[3] + self.facing[1] * self.speed[1]]

        if self.score != 3 and not self.paused:
            self.root.after(15, self.move)
