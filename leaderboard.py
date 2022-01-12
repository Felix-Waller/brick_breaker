from tkinter import Canvas
from colour import Colour


class Leaderboard:
    def __init__(self, root):
        self.canvas = Canvas(
            root, width=260, height=720, bg=Colour.side_backgound,
            highlightthickness=0)
        self.canvas.place(x=1010, y=0)
        self.get_data()

    def update(self, game, name, score):
        if name:
            name = name.replace(" ", "")

            if game == 1:
                file_name = "assets/leaderboard1.txt"
            elif game == 2:
                file_name = "assets/leaderboard2.txt"
            else:
                file_name = "assets/leaderboard3.txt"

            with open(file_name, "r") as file:
                scores = [line.split() for line in file]

            set = False

            # Update score if already played
            for i in scores:
                if i[0] == name:
                    set = True
                    if float(i[1]) > float(score):
                        i[1] = score
                        break

            # Add score if new user
            if not set:
                scores.append([name, score])

            scores = [' '.join(x) + "\n" for x in scores]

            with open(file_name, "w") as file:
                file.writelines(scores)

            self.get_data()

    def get_data(self):
        self.canvas.delete('all')
        self.canvas.create_text(
            20, 30, text="LEADERBOARD", font=("Purisa", 20),
            fill=Colour.text_colour, anchor="w")

        self.canvas.create_text(
            20, 60, text="LEVEL 1", font=("Purisa", 14),
            fill=Colour.text_colour, anchor="w")
        # Level 1
        try:
            with open("assets/leaderboard1.txt") as file:
                leaderboard = sorted(
                    [line.split() for line in file], key=lambda x: float(x[1]))
            for i in range((len(leaderboard) if
                            len(leaderboard) < 10 else 10)):
                self.canvas.create_text(
                    20, 85 + 18 * i, text=f"{i + 1}. {leaderboard[i][0]}",
                    font=("Purisa", 11), fill=Colour.text_colour, anchor="w")
                self.canvas.create_text(
                    240, 85 + 18 * i, text=f"{leaderboard[i][1]}",
                    font=("Purisa", 11), fill=Colour.text_colour, anchor="e")
            if len(leaderboard) == 0:
                self.canvas.create_text(
                    20, 85, text="Nothing yet!", font=("Purisa", 11),
                    fill=Colour.text_colour, anchor="w")
        except FileNotFoundError:
            with open("assets/leaderboard1.txt", "w") as file:
                file.write("")

        # Level 2
        try:
            self.canvas.create_text(
                20, 270, text="LEVEL 2", font=("Purisa", 14),
                fill=Colour.text_colour, anchor="w")
            with open("assets/leaderboard2.txt") as file:
                leaderboard = sorted(
                    [line.split() for line in file], key=lambda x: float(x[1]))
            for i in range((len(leaderboard) if
                            len(leaderboard) < 10 else 10)):
                self.canvas.create_text(
                    20, 295 + 18 * i, text=f"{i + 1}. {leaderboard[i][0]}",
                    font=("Purisa", 11), fill=Colour.text_colour, anchor="w")
                self.canvas.create_text(
                    240, 295 + 18 * i, text=f"{leaderboard[i][1]}",
                    font=("Purisa", 11), fill=Colour.text_colour, anchor="e")
            if len(leaderboard) == 0:
                self.canvas.create_text(
                    20, 295, text="Nothing yet!", font=("Purisa", 11),
                    fill=Colour.text_colour, anchor="w")
        except FileNotFoundError:
            with open("assets/leaderboard2.txt", "w") as file:
                file.write("")

        # Level 3
        try:
            self.canvas.create_text(
                20, 480, text="LEVEL 3", font=("Purisa", 14),
                fill=Colour.text_colour, anchor="w")
            with open("assets/leaderboard3.txt") as file:
                leaderboard = sorted(
                    [line.split() for line in file],
                    key=lambda x: float(x[1]))
            for i in range((len(leaderboard) if
                            len(leaderboard) < 10 else 10)):
                self.canvas.create_text(
                    20, 505 + 18 * i, text=f"{i + 1}. {leaderboard[i][0]}",
                    font=("Purisa", 11), fill=Colour.text_colour, anchor="w")
                self.canvas.create_text(
                    240, 505 + 18 * i, text=f"{leaderboard[i][1]}",
                    font=("Purisa", 11), fill=Colour.text_colour, anchor="e")
            if len(leaderboard) == 0:
                self.canvas.create_text(
                    20, 505, text="Nothing yet!", font=("Purisa", 11),
                    fill=Colour.text_colour, anchor="w")
        except FileNotFoundError:
            with open("assets/leaderboard3.txt", "w") as file:
                file.write("")
