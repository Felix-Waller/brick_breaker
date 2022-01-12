#! /usr/bin/env python3

"""
COMP16321 Coursework
Brick-breaker star-collector game
Screen resolution: 1280x720
by Felix Waller

main.py contains:
    the main tkinter window
    the left-hand menu
    handling of essential keybinds
"""

import os
from tkinter import Button, Canvas, Label, PhotoImage, Tk
from tkinter import simpledialog, filedialog, messagebox
import pickle
from colour import Colour
from game_canvas import GameCanvas
from leaderboard import Leaderboard


def button_left():
    """Rebind key to move paddle left"""
    while True:
        btn = simpledialog.askstring(
            title="Move Left",
            prompt="Enter single key. Must be alphanumeric or space.")
        if not btn:
            break
        if len(btn) == 1:
            btn = btn.lower()
            if btn.isalnum() and btn not in [canvas.paddle_right_key,
                                             pause_key, boss_key]:
                left_button["text"] = f"MOVE LEFT: {btn}"
                root.unbind(canvas.paddle_left_key)
                canvas.paddle_left_key = btn
                root.bind(canvas.paddle_left_key, canvas.paddle_left)
                break
            elif btn == " ":
                left_button["text"] = "MOVE LEFT: <space>"
                root.unbind(canvas.paddle_left_key)
                canvas.paddle_left_key = "<space>"
                root.bind(canvas.paddle_left_key, canvas.paddle_left)
                break


def button_right():
    """Rebind key to move paddle right"""
    while True:
        btn = simpledialog.askstring(
            title="Move Right",
            prompt="Enter single key. Must be alphanumeric or space.")
        if not btn:
            break
        if len(btn) == 1:
            btn = btn.lower()
            if btn.isalnum() and btn not in [canvas.paddle_left_key,
                                             pause_key, boss_key]:
                right_button["text"] = f"MOVE RIGHT: {btn}"
                root.unbind(canvas.paddle_right_key)
                canvas.paddle_right_key = btn
                root.bind(canvas.paddle_right_key, canvas.paddle_right)
                break
            elif btn == " ":
                right_button["text"] = "MOVE RIGHT: <space>"
                root.unbind(canvas.paddle_right_key)
                canvas.paddle_right_key = "<space>"
                root.bind(canvas.paddle_right_key, canvas.paddle_right)
                break


def button_pause_change():
    """Rebind pause key"""
    global pause_key
    while True:
        btn = simpledialog.askstring(
            title="Pause",
            prompt="Enter single key. Must be alphanumeric or space.")
        if not btn:
            break
        if len(btn) == 1:
            btn = btn.lower()
            if btn.isalnum() and btn not in [canvas.paddle_left_key,
                                             canvas.paddle_right_key,
                                             boss_key]:
                root.unbind(pause_key)
                pause_button_change["text"] = f"PAUSE: {btn}"
                pause_key = btn
                root.bind(pause_key, pause)
                break
            elif btn == " ":
                root.unbind(pause_key)
                pause_button_change["text"] = "PAUSE: <space>"
                pause_key = "<space>"
                root.bind(pause_key, pause)
                break


def button_boss_change():
    """Rebind boss key"""
    global boss_key
    while True:
        btn = simpledialog.askstring(
            title="Boss",
            prompt="Enter single key. Must be alphanumeric or space.")
        if not btn:
            break
        if len(btn) == 1:
            btn = btn.lower()
            if btn.isalnum() and btn not in [canvas.paddle_left_key,
                                             canvas.paddle_right_key,
                                             pause_key]:
                root.unbind(boss_key)
                boss_button["text"] = f"BOSS: {btn}"
                boss_key = btn
                root.bind(boss_key, boss)
                break
            elif btn == " ":
                root.unbind(boss_key)
                boss_button["text"] = "BOSS: <space>"
                boss_key = "<space>"
                root.bind(boss_key, boss)
                break


def button_retry():
    if canvas.current_level:
        temp = canvas.current_level
        canvas.ball.game_over()
        if temp == 1:
            canvas.level1()
        elif temp == 2:
            canvas.level2()
        else:
            canvas.level3()


def button_save():
    global paused
    paused = False
    pause(None)
    name = simpledialog.askstring(
        title="Save Game", prompt="Enter save file name.")
    if name:
        name = name.replace(" ", "_")
        data = canvas.save(pause_key, boss_key)
        try:
            with open(f"saves/{name}.obj", "wb") as file:
                pickle.dump(data, file)
        except:
            os.mkdir("saves")
            with open(f"saves/{name}.obj", "wb") as file:
                pickle.dump(data, file)


def button_load():
    global paused
    global pause_key, boss_key
    global left_button, right_button, pause_button_change, boss_button
    global levels_unlocked
    paused = False
    pause(None)
    file_name = filedialog.askopenfilename(initialdir="saves")
    if file_name:
        with open(file_name, "r+b") as file:
            try:
                data = pickle.load(file)
            except:
                messagebox.showinfo("Error", "Error opening save file")
                return
            left_button["text"] = "MOVE LEFT: " + data["keybinds"]["left"]
            right_button["text"] = "MOVE RIGHT: " + data["keybinds"]["right"]

            root.unbind(pause_key)
            pause_key = data["keybinds"]["pause"]
            pause_button_change["text"] = "PAUSE: " + data["keybinds"]["pause"]
            root.bind(pause_key, pause)

            root.unbind(boss_key)
            boss_key = data["keybinds"]["boss"]
            boss_button["text"] = "BOSS: " + data["keybinds"]["boss"]
            root.bind(boss_key, boss)

            canvas.levels_unlocked = data["unlocked"]
            canvas.level_unlock()
            canvas.load(data)

        if not canvas.current_level and paused:
            paused = False
            paused_text.destroy()
            pause_button.configure(text="PAUSE")
        else:
            paused = False
            pause(None)


def button_pause():
    pause(None)


def pause(event):
    if canvas.current_level:
        global paused
        global paused_text
        paused = not paused
        if paused_text:
            paused_text.destroy()
        if paused:
            paused_text = Button(
                root, text="PAUSED", font=("Purisa", 40),
                fg=Colour.text_colour, bg=Colour.button_colour,
                command=button_pause)
            paused_text.place(x=640, y=360, anchor="center")
            pause_button.configure(text="UNPAUSE")
        else:
            pause_button.configure(text="PAUSE")
        canvas.timer.pause(paused)
        canvas.ball.pause(paused)
        canvas.paddle.pause(paused)


def boss(event):
    """Switch to an image to disguise the game"""
    if not paused:
        pause(event)
    global boss_bool
    global boss_canvas
    boss_bool = not boss_bool
    if boss_bool:
        root.unbind("<space>")
        boss_canvas = Canvas(root, width=1280, height=720)
        boss_canvas.place(x=0, y=0)
        boss_canvas.create_text(10, 10, text="text")
        boss_canvas.create_image(640, 360, image=boss_image)
        root.title("Firefox")
    else:
        root.bind("<space>", pause)
        boss_canvas.destroy()
        root.title("Brick Breaker Star Collector")

# Keybind defaults
paddle_left_key = "a"
paddle_right_key = "d"
pause_key = "<space>"
boss_key = "b"

# Create window
root = Tk()
root.title("Brick Breaker Star Collector")
root.geometry(f"1280x720")
root.resizable(False, False)
root.configure(bg=Colour.side_backgound)

# Create leaderboard
leaderboard = Leaderboard(root)

# Create menu
menu_title = Label(
    root, text="MENU", font=("Purisa", 20), fg=Colour.text_colour,
    bg=Colour.side_backgound)
menu_title.place(x=130, y=25, anchor="center")
pause_button = Button(
    root, text="PAUSE", font=("Purisa", 11), fg=Colour.text_colour,
    bg=Colour.button_colour, command=button_pause)
pause_button.place(x=130, y=70, width=150, height=40, anchor="center")
save_button = Button(
    root, text="SAVE", font=("Purisa", 11), fg=Colour.text_colour,
    bg=Colour.button_colour, command=button_save)
save_button.place(x=130, y=120, width=150, height=40, anchor="center")
load_button = Button(
    root, text="LOAD", font=("Purisa", 11), fg=Colour.text_colour,
    bg=Colour.button_colour, command=button_load)
load_button.place(x=130, y=170, width=150, height=40, anchor="center")
retry_button = Button(
    root, text="RETRY", font=("Purisa", 11), fg=Colour.text_colour,
    bg=Colour.button_colour, command=button_retry)
retry_button.place(x=130, y=220, width=150, height=40, anchor="center")

controls_title = Label(
    root, text="CONTROLS", font=("Purisa", 20), fg=Colour.text_colour,
    bg=Colour.side_backgound)
controls_title.place(x=130, y=270, anchor="center")
left_button = Button(
    root, text=f"MOVE LEFT: {paddle_left_key}", font=("Purisa", 11),
    fg=Colour.text_colour, bg=Colour.button_colour, command=button_left)
left_button.place(x=130, y=320, width=150, height=40, anchor="center")
right_button = Button(
    root, text=f"MOVE RIGHT: {paddle_right_key}", font=("Purisa", 11),
    fg=Colour.text_colour, bg=Colour.button_colour, command=button_right)
right_button.place(x=130, y=370, width=150, height=40, anchor="center")
pause_button_change = Button(
    root, text=f"PAUSE: {pause_key}", font=("Purisa", 11),
    fg=Colour.text_colour, bg=Colour.button_colour,
    command=button_pause_change)
pause_button_change.place(x=130, y=420, width=150, height=40, anchor="center")
boss_button = Button(
    root, text=f"BOSS: {boss_key}", font=("Purisa", 11), fg=Colour.text_colour,
    bg=Colour.button_colour, command=button_boss_change)
boss_button.place(x=130, y=470, width=150, height=40, anchor="center")

# Boss canvas
boss_canvas = None
boss_bool = False
boss_image = PhotoImage(file="assets/boss.png")

levels_unlocked = 1

paused = False
paused_text = None

# Main game canvas
canvas = GameCanvas(
    root, levels_unlocked, leaderboard, paddle_left_key, paddle_right_key)

# Bind default keys
root.bind(pause_key, pause)
root.bind(boss_key, boss)

root.mainloop()
