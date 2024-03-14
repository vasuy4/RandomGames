import datetime
import random
import time
import tkinter as tk
from tkinter.messagebox import showinfo, showerror
from tkinter import ttk
from PIL import Image, ImageTk
from os import getcwd


def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k


class PieChart:
    def __init__(self, root, data: list, colors, colorsName, start_angle=90, len_track=1000):
        self.root = root
        self.root.geometry('1600x830')
        self.canvas = tk.Canvas(root, width=1600, height=830)
        self.canvas.pack()
        self.data = data
        self.colors = colors
        self.colorsName = colorsName
        self.start_angle = start_angle
        self.total = sum(data)
        self.lengthData = len(data)
        self.luckyMulti = [0 for _ in range(self.lengthData)]
        self.scoreboard = dict(zip(colors, [0 for _ in range(len(data))]))
        self.positionColor = dict(zip(colors, [0 for _ in range(len(data))]))
        self.lenRaceTrack = len_track
        self.horse_images = {}
        for i in range(len(data)):
            name_file = "{direct}/images/horses/{color}.png".format(direct=getcwd(), color=colors[i])
            img = Image.open(name_file)
            img = img.resize((20, 20))
            horseImage = ImageTk.PhotoImage(img)
            self.horse_images[colors[i]] = horseImage

            name_face_file = "{direct}/images/horses/{color}Face.png".format(direct=getcwd(), color=colors[i])
            imgFace = Image.open(name_face_file)
            imgFace = imgFace.resize((20, 20))
            faceImage = ImageTk.PhotoImage(imgFace)
            self.horse_images[colors[i] + "Face"] = faceImage

        self.draw_pie_chart()

    def draw_pie_chart(self):
        self.canvas.delete("all")
        end_angle = self.start_angle
        for idx, value in enumerate(self.data):
            slice_angle = 360 * value / self.total
            self.canvas.create_arc(10, 10, 790, 790, start=end_angle, extent=slice_angle, fill=self.colors[idx])

            end_angle += slice_angle

        self.random_data()
        self.draw_legend()
        self.draw_scoreboard()
        self.draw_columns()
        end = self.draw_racetrack()
        if not end:
            self.total = sum(self.data)
            self.root.after(1, self.draw_pie_chart)
        else:
            showinfo(title="WIN!", message=f"{end} winner!")
            showerror(title="Предупреждение от антивируса!", message="На вашем компьютере обнаружен троян!")

    def random_data(self):
        for i_elem in range(self.lengthData):
            if self.colors[i_elem] != get_key(self.scoreboard, max(self.scoreboard.values())):
                self.data[random.randint(0, self.lengthData - 1)] += random.random() / 5
                self.data[i_elem] += 1 / self.data[i_elem]

            sortedScoreboard = dict(sorted(self.scoreboard.items(), key=lambda item: item[1], reverse=True))
            places = dict()
            i_place = 1
            for color, score in sortedScoreboard.items():
                places[color] = i_place  # цвет и место в рейтинге гонки, 1-ое место -> i_place=1
                i_place += 1

            if max(places.values()) > 6 and self.lenRaceTrack < 5001:
                minus = random.randint(0, int(places[self.colors[i_elem]] / 2))
            else:
                minus = 0

            chance_multi = random.randint(0, 19 - minus)
            if chance_multi % 5 == 0:
                self.data[i_elem] *= 1 + places[self.colors[i_elem]] / 100
            elif chance_multi == 13:
                self.data[i_elem] *= random.random()
            if chance_multi == 7:
                self.data[i_elem] *= (random.random() + 1) + self.luckyMulti[i_elem] / 3
                self.luckyMulti[i_elem] += 1
                if self.luckyMulti[i_elem] > 1:
                    s = "{} Combo x{} for {}\n".format(datetime.datetime.now().time(), self.luckyMulti[i_elem], self.colors[i_elem])
                    print(s, end='')
            else:
                self.luckyMulti[i_elem] = 0
            if self.data[i_elem] < 1000:
                self.data[i_elem] *= random.randint(1, 15)

        remain_scores = self.data[:]
        sum_scores = sum(self.data)
        threeLargest = 0
        while remain_scores:
            for idx, value in enumerate(self.data):
                if remain_scores and value == max(remain_scores):
                    threeLargest += 1
                    plus_score = 3/100 * (max(remain_scores) / sum_scores * 100)
                    self.scoreboard[self.colors[idx]] += plus_score + random.random() / 2
                    remain_scores.remove(value)
                    if threeLargest <= 3 and random.randint(1, 10000) == 3:
                        plus_score = random.random() * 200 * random.randint(-1, 1)
                        self.scoreboard[self.colors[idx]] += plus_score
                        print("{} EXTRA SUPER {} for {}".format(datetime.datetime.now().time(), plus_score, self.colors[idx]))
        if random.randint(1, 10000) == 100:
            plus_score = random.random() * 450
            randomIndex = random.randint(0, self.lengthData - 1)
            self.scoreboard[self.colors[randomIndex]] += plus_score
            print("{} ULTRA EXTRA SUPER {} for {}".format(datetime.datetime.now().time(), plus_score,
                                                          self.colors[randomIndex]))

        if random.randint(1, 10**6) == 77:
            plus_score = random.random() * random.randint(999, 1111)
            randomIndex = random.randint(0, self.lengthData - 1)
            self.scoreboard[self.colors[randomIndex]] += plus_score
            print("{} GODLIKE MEGA ULTRA EXTRA SUPER LUCKY {} for {}".format(datetime.datetime.now().time(), plus_score,
                                                          self.colors[randomIndex]))

    def draw_racetrack(self):
        x = 820
        y = 410
        old_y = y
        finish = 1550
        diff = finish - x
        winner = False
        percent100 = self.lenRaceTrack

        for color, score in self.scoreboard.items():
            scorePercent = score / percent100 * 100
            now_position = diff / 100 * scorePercent + x
            if self.positionColor[color] == 0:
                self.positionColor[color] = x
            self.positionColor[color] = now_position

            horseImage = self.horse_images[color]
            self.canvas.create_image(now_position, y, image=horseImage, anchor='nw')

            y += 30
            if now_position >= finish:
                self.canvas.create_text(finish - 20, old_y - 20, text=f"FINISH\n  {percent100}", fill=color,
                                        font=("Arial", 11), anchor="w")
                self.canvas.create_rectangle(finish+20, old_y, finish + 22, old_y + 30 * self.lengthData, fill=color)
                winner = self.colorsName[color]
        if winner:
            return winner
        self.canvas.create_text(finish-20, old_y-20, text=f"FINISH\n  {percent100}", fill='black', font=("Arial", 11), anchor="w")
        self.canvas.create_rectangle(finish+20, y, finish + 22, old_y, fill='black')

    def draw_columns(self):
        x = 880
        y = 5
        diff = self.canvas.winfo_width() - 50 - x
        sorted_dict = dict(sorted(self.scoreboard.items(), key=lambda item: item[1], reverse=True))
        percent100 = list(sorted_dict.values())[0]
        for color, score in sorted_dict.items():
            scorePercent = score / percent100 * 100
            plus = diff / 100 * scorePercent
            self.canvas.create_rectangle(x, y, x + plus, y + 20, fill=color)
            y += 30

    def draw_scoreboard(self):
        x = 800
        y = 5
        sorted_dict = dict(sorted(self.scoreboard.items(), key=lambda item: item[1], reverse=True))
        for color, score in sorted_dict.items():
            horseImage = self.horse_images[color + "Face"]
            self.canvas.create_image(x, y, image=horseImage, anchor='nw')

            self.canvas.create_text(x + 30, y + 10, text=f"{round(score, 2)}", fill="black", font=("Arial", 11), anchor="w")
            y += 30

    def draw_legend(self):
        x = 10
        y = 800
        new_dict = {}
        for idx, value in enumerate(self.data):
            new_dict[self.colors[idx]] = value

        sort_dict = dict(sorted(new_dict.items(), key=lambda item: item[1], reverse=True))
        total_sum = sum(self.data)
        for color, value in sort_dict.items():
            percent = value / total_sum * 100
            self.canvas.create_rectangle(x, y, x + 20, y + 20, fill=color)
            self.canvas.create_text(x + 30, y + 10, text=f"{round(percent, 2)}%", fill="black", font=("Arial", 11), anchor="w")
            x += 85


def create_pie_chart(root, data, colors, startBtn, entry_len_race, labelChoose, colorLabels, imageLabels, colorsName):
    len_track = entry_len_race.get()
    if not len_track:
        len_track = 2500
    else:
        len_track = int(len_track)
    startBtn.destroy()
    entry_len_race.destroy()
    labelChoose.destroy()
    for i_label in colorLabels:
        i_label.destroy()
    for i_label in imageLabels:
        i_label.destroy()

    pie_chart = PieChart(root, data, colors, len_track=len_track, colorsName=colorsName)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('860x860')

    colors = ['red', 'green', 'lightblue', 'orange', 'pink', 'yellow', 'silver', 'indigo', 'cyan', 'snow', 'springgreen', 'chocolate']
    colorsName = {'red': 'Blood', 'green': 'Nature', 'lightblue': 'Ice', 'orange': 'Flame', 'pink': 'Rose', 'yellow': 'Lemon',
                  'silver':'Steel dick', 'indigo':'Night', 'cyan':'Wave', 'snow':'Snow', 'springgreen':'Toxic', 'chocolate':'Chocolate'}
    data = [1000 for _ in range(len(colors))]


    colorLabels = list()
    imageLabels = []

    image_files = ['{}/images/horses/'.format(getcwd()) + color + 'Face.png' for color in colors]
    images = [tk.PhotoImage(file=image_file) for image_file in image_files]

    row_index = 0
    column_index = 0

    for i_color, image in zip(colors, images):
        name = colorsName[i_color]
        labelColor = ttk.Label(root, text=name, font='Times 20', background=i_color)
        labelColor.grid(row=column_index, column=2 * (row_index % 3), padx=5, pady=5)
        colorLabels.append(labelColor)

        labelImage = ttk.Label(root, image=image)
        labelImage.grid(row=column_index+1, column=2 * (row_index % 3), padx=5, pady=5)
        imageLabels.append(labelImage)

        row_index += 1
        if row_index % 3 == 0:
            column_index += 2

    labelChoose = ttk.Label(root, text='Length track:', font='Times 20')
    labelChoose.grid(row=0, column=5)

    entry_len_race = tk.Entry(root, width=20)
    entry_len_race.grid(row=1, column=5)

    startBtn = tk.Button(root, text="START", font='Times 20', command=lambda: create_pie_chart(root, data, colors, startBtn,
                                                                                               entry_len_race, labelChoose,
                                                                                               colorLabels, imageLabels, colorsName))
    startBtn.grid(row=2, column=5)

    root.mainloop()