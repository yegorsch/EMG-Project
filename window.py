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
        self.draw_circle()

    def draw_circle(self):
        arc = self.canvas.create_oval(0, 0, 40, 40)

        self.canvas.pack()