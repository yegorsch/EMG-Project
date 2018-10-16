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
        self.max = 2
        self.min = 0.5
        self.master = root
        self.height = 250
        self.width= 300
        self.canvas = tk.Canvas(root, height=self.height, width=self.height)
        # canvas.delete("all")
        self.initialCoords = [150, 30, 180, 60]
        self.canvas.create_oval(self.initialCoords)
        self.canvas.pack()

    def move_circle(self, by):
        if by < 0.5:
            by = -by - 2
        else:
            by += 2
        self.initialCoords = [self.initialCoords[0] + by, self.initialCoords[1], self.initialCoords[2] + by, self.initialCoords[3] + by]
        self.canvas.delete("all")
        self.canvas.create_oval(self.initialCoords)



    #def draw_circle(self):

