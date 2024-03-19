import datetime
import random
import time
import tkinter as tk
from tkinter.messagebox import showinfo, showerror
from tkinter import ttk
from PIL import Image, ImageTk
from os import getcwd

from typing import Any, List, Dict


def get_key(d: Dict[Any, Any], value: Any):
    """Получить ключ по значению"""
    for k, v in d.items():
        if v == value:
            return k


class PieChart:
    def __init__(self, root: tk.Tk, data: List[int], colors: List[str], colorsName: Dict[str, str], start_angle=90,
                 len_track=1000):
        """
        Инициализация класса меню гонки
        :param root: корень окна ткинтера
        :param data: список скоростей коней (сравнивается в процентах)
        :param colors: список цветов коней
        :param colorsName: словарь, где ключ - цвет, значение - имя коня
        :param start_angle: начальный угол круговой диаграммы
        :param len_track: длина гоночной трассы
        """
        self.root = root
        self.root.geometry('1600x830')
        self.canvas = tk.Canvas(root, width=1600, height=830)
        self.canvas.pack()
        self.data = data
        self.colors = colors
        self.colorsName = colorsName
        self.start_angle = start_angle
        self.total = sum(data)  # сумма всех скоростей
        self.lengthData = len(data)  # количество коней
        self.luckyMulti = [0 for _ in range(self.lengthData)]  # дополнительный коэф. умножения
        self.bonusChance = [1 for _ in range(self.lengthData)]  # увеличение шанса пока не случится x2 Multi
        self.scoreboard = dict(zip(colors, [0 for _ in range(len(data))]))  # таблица лидеров (ключ - цвет, знач - пройденный участок)
        self.positionColor = dict(zip(colors, [0 for _ in range(len(data))]))  # словарь коней (ключей) с их расположением в окне в пикселях (знач)
        self.lenRaceTrack = len_track  # длина гоночной трассы
        self.horse_images = {}  # изображение коней
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

        self.totalIterations = 0  # счётчик прошедших итераций (для статистики)
        self.totalMultiChance = 0  # счётчик случившихся мультибонусов (тоже для статистики)
        self.draw_pie_chart()  # начинаем отображение гонки

    def draw_pie_chart(self):
        """Регулярное обновление круговой диаграммы, пока кто-то не финиширует и запуск остальных функций"""
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
            print("Iters: {}, Count chance: {}, Average chance: {}%".format(self.totalIterations,
                                                                            self.totalMultiChance, self.totalMultiChance / self.totalIterations * 100))
            showinfo(title="WIN!", message=f"{end} winner!")
            showerror(title="Предупреждение от антивируса!", message="На вашем компьютере обнаружен троян!")

    def random_data(self):
        self.totalIterations += 1
        if self.lenRaceTrack > 9001:
            limiterChance = 999
        elif self.lenRaceTrack > 7001:
            limiterChance = 150
        elif self.lenRaceTrack > 5001:
            limiterChance = 25
        elif self.lenRaceTrack > 4001:
            limiterChance = 9
        else:
            limiterChance = 2
        all_summ_data = sum(self.data)
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

            if random.randint(1, limiterChance) == 1:
                if self.data[i_elem] > 5000000:
                    self.data[i_elem] /= random.randint(1000, 1500)
                    for i in range(self.lengthData - 1):
                        self.data[i] /= 1000
                if self.data[i_elem] > 1550000:
                    self.data[i_elem] /= random.randint(100, 150)
                    for i in range(self.lengthData // 2):
                        self.data[random.randint(0, self.lengthData - 1)] /= 3

            if random.randint(1, limiterChance) == 1:
                if self.data[i_elem] / all_summ_data > 0.95:
                    self.data[i_elem] /= max(self.data) / min(self.data)
                elif self.data[i_elem] / all_summ_data > 0.85:
                    self.data[i_elem] /= max(2.5, max(self.data) / (min(self.data) * 10))
                elif self.data[i_elem] / all_summ_data > 0.7:
                    self.data[i_elem] /= 2
                elif self.data[i_elem] / all_summ_data > 0.6:
                    self.data[i_elem] /= 1.4

            chance_multi = random.randint(0, 179 - minus)
            if chance_multi % 5 == 0:
                self.data[i_elem] *= 1 + places[self.colors[i_elem]] / 100
            elif chance_multi == 13:
                self.data[i_elem] *= random.random()
            if chance_multi == 7 or random.randint(1, 77777 // self.bonusChance[i_elem]) == 1:
                self.totalMultiChance += 1

                self.data[i_elem] *= (random.random() + 1) + self.luckyMulti[i_elem] / (1.5 + minus * 2)
                self.luckyMulti[i_elem] += 1
                if self.luckyMulti[i_elem] > 1:
                    print(self.bonusChance, self.bonusChance[i_elem])
                    self.bonusChance[i_elem] = 1
                    s = "{} Combo x{} for {}\n".format(datetime.datetime.now().time(), self.luckyMulti[i_elem], self.colors[i_elem])
                    print(s, end='')
            else:
                self.bonusChance[i_elem] += 1
                self.luckyMulti[i_elem] = 0
            if self.data[i_elem] < 500:
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
            print("{} ULTRA EXTRA SUPER +{} for {}".format(datetime.datetime.now().time(), plus_score,
                                                          self.colors[randomIndex]))

        if random.randint(1, 10**6) == 77:
            plus_score = random.random() * random.randint(999, 1111)
            randomIndex = random.randint(0, self.lengthData - 1)
            self.scoreboard[self.colors[randomIndex]] += plus_score
            print("{} GODLIKE MEGA ULTRA EXTRA SUPER LUCKY +{} for {}".format(datetime.datetime.now().time(), plus_score,
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
            #self.canvas.create_text(x + 30, y + 10, text=f"{round(value, 2)}", fill="black", font=("Arial", 11), anchor="w")
            x += 85


def create_pie_chart(root: tk.Tk, data: List[int], colors: List[str], startBtn: tk.Button, entry_len_race: tk.Entry,
                     labelChoose: tk.Label, colorLabels: List[tk.Label], imageLabels: List[ttk.Label],
                     colorsName: Dict[str, str]):
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


def start_horse_race(rootM):
    # rootM = tk.Tk()
    rootM.geometry('860x860')

    colorsM = ['red', 'green', 'lightblue', 'orange', 'pink', 'yellow', 'silver', 'indigo', 'cyan', 'snow', 'springgreen', 'chocolate']
    colorsNameM = {'red': 'Blood', 'green': 'Nature', 'lightblue': 'Ice', 'orange': 'Flame', 'pink': 'Rose', 'yellow': 'Lemon',
                  'silver':'Steel dick', 'indigo':'Night', 'cyan':'Wave', 'snow':'Snow', 'springgreen':'Toxic', 'chocolate':'Chocolate'}
    dataM = [500 for _ in range(len(colorsM))]

    colorLabelsM = list()
    imageLabelsM = []

    image_filesM = ['{}/images/horses/'.format(getcwd()) + color + 'Face.png' for color in colorsM]
    imagesM = [tk.PhotoImage(file=image_file) for image_file in image_filesM]
    row_index = 0
    column_index = 0

    for i_color, image in zip(colorsM, imagesM):
        name = colorsNameM[i_color]
        labelColor = ttk.Label(rootM, text=name, font='Times 20', background=i_color)
        labelColor.grid(row=column_index, column=2 * (row_index % 3), padx=5, pady=5)
        colorLabelsM.append(labelColor)

        labelImage = ttk.Label(rootM, image=image)
        labelImage.grid(row=column_index+1, column=2 * (row_index % 3), padx=5, pady=5)
        imageLabelsM.append(labelImage)

        row_index += 1
        if row_index % 3 == 0:
            column_index += 2

    labelChooseM = ttk.Label(rootM, text='Length track:', font='Times 20')
    labelChooseM.grid(row=0, column=5)

    entry_len_raceM = tk.Entry(rootM, width=20)
    entry_len_raceM.grid(row=1, column=5)

    startBtnM = tk.Button(rootM, text="START", font='Times 20', command=lambda: create_pie_chart(rootM, dataM, colorsM, startBtnM,
                                                                                               entry_len_raceM, labelChooseM,
                                                                                               colorLabelsM, imageLabelsM, colorsNameM))
    startBtnM.grid(row=2, column=5)

    rootM.mainloop()

if __name__ == "__main__":
    rootM = tk.Tk()
    start_horse_race(rootM)