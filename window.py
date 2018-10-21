import Tkinter as tk
from Tkinter import Text, END
from collections import deque
import numpy as np

class TextWindow:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.text_view = Text(master, height=1, font=("Helvetica", 180))
        self.text_view.pack()
        self.text_view.insert(END, "Just a text Widget\nin two lines\n")

    def set_text(self, text):
        self.text_view.delete(1.0, END)
        self.text_view.insert(END, text)
        self.text_view.pack()


class CircleWindow:

    def __init__(self, root):
        self.master = root
        self.height = 100
        self.width = 800
        self.radius = 20
        self.by_values = deque(maxlen=4)
        self.canvas = tk.Canvas(root, height=self.height, width=self.width)
        # canvas.delete("all")
        self.initialCoords = [150, 30, 180, 60]
        self.canvas.create_oval(self.initialCoords)
        self.canvas.pack()

    def color(self, by):
        n = self.width * by
        R = int(abs((255 * n) / self.width))
        G = int(abs((255 * (self.width - n)) / self.width))
        return '#%02x%02x%02x' % (R, G, 0)

    def calc_coords(self, by):
        self.by_values.append(by)
        avg_by = np.mean(self.by_values)
        avg_by = 1 - avg_by
        x = self.width * avg_by
        y = self.height / 2 + self.radius / 2
        return [x - self.radius, y - self.radius, x + self.radius, y + self.radius]

    def move_circle(self, by):
        if by < 0 or by > 1:
            return
        self.canvas.delete("all")
        color = self.color(by)
        self.canvas.create_oval(self.calc_coords(by), outline=color, fill=color)

