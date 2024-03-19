from race import start_horse_race
import tkinter as tk
from tkinter import ttk
from typing import List, Callable


def start_game(root: tk.Tk, start_func: Callable[[tk.Tk], None], objs: List[tk], obj: tk):
    for i_obj in objs:
        i_obj.destroy()
    obj.destroy()
    start_func(root)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('1600x800')
    objects = []

    labelChoose = ttk.Label(root, text="Choose game:", font='Times 20')
    labelChoose.grid(row=0, column=0)
    objects.append(labelChoose)

    btn_horse_race = tk.Button(root, text='Horses race', font='Times 20', command=lambda :start_game(root, start_horse_race, objects, btn_horse_race))
    btn_horse_race.grid(row=1, column=0)
    objects.append(btn_horse_race)

    btn_cars_race = tk.Button(root, text="Cars race", font='Times 20', command=lambda :start_game(root, start_horse_race, objects, btn_cars_race))
    btn_cars_race.grid(row=1, column=1)
    objects.append(btn_cars_race)

    root.mainloop()