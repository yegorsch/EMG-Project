import Tkinter as tk
from Tkinter import Text, END

class TextWindow:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.text_view = Text(master, height=4, font=("Helvetica", 11))
        self.text_view.pack()
        self.text_view.insert(END, "Just a text Widget\nin two lines\n")

    def set_text(self, text):
        self.text_view.delete(1.0, END)
        self.text_view.insert(END, text)
        self.text_view.pack()


class CircleWindow:

    def __init__(self, root):
        self.master = root
        self.height = 250
        self.width= 500
        self.radius = 30
        self.canvas = tk.Canvas(root, height=self.height, width=self.height)
        # canvas.delete("all")
        self.initialCoords = [150, 30, 180, 60]
        self.canvas.create_oval(self.initialCoords)
        self.canvas.pack()
    #
    # def _create_circle(self, x, y, r, **kwargs):
    #     return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)
    def move_circle(self, by):
        x = self.width * by
        # x0 = anchor
        # y0 = 0
        # x1 = anchor + self.radius * 2
        # y1 = x1 + self.radius * 2
        y = 40
        self.canvas.delete("all")
        self.canvas.create_oval([x - self.radius, y - self.radius, x + self.radius, y + self.radius])



    #def draw_circle(self):

