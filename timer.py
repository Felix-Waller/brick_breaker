import time
from tkinter.constants import ANCHOR
from colour import Colour


class Timer:
    def __init__(self, root, canvas):
        self.root = root
        self.canvas = canvas
        self.start_time = 0
        self.loaded_time = 0
        self.current_time = 0
        self.final_time = 0
        self.paused = False
        self.time_paused = 0
        self.timer = self.canvas.create_text(
            20, 30, text="Time: 0", font=("Purisa", 20),
            fill=Colour.text_colour, anchor="w")

    def load(self, data):
        self.loaded_time = data["time"]
        self.final_time = data["final"]
        self.canvas.itemconfigure(
            self.timer, text="Time: " + self.format(self.loaded_time))

    def format(self, time):
        secs = time // 1000000000
        ms = time // 1000000 - secs * 1000
        return f"{secs}.{ms}"

    def start(self):
        self.start_time = time.time_ns()
        self.count()

    def stop(self):
        self.final_time = self.format(
            self.current_time + self.loaded_time - self.start_time -
            self.time_paused)

    def pause(self, paused):
        self.paused = paused
        if not self.paused:
            self.time_paused += time.time_ns() - self.current_time
            self.count()

    def count(self):
        self.current_time = time.time_ns()
        if self.paused:
            return
        if self.final_time == 0:
            self.canvas.itemconfigure(
                self.timer,
                text="Time: " +
                self.format(
                    self.current_time +
                    self.loaded_time - self.start_time - self.time_paused))
            self.root.after(10, self.count)
        else:
            self.canvas.itemconfigure(
                self.timer, text="Time: " + self.final_time)
