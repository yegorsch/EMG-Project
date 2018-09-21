import Tkinter as tk
from Tkinter import Text, END

class TextWindow:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.text_view = Text(master, height=4, font=("Helvetica", 60))
        self.text_view.pack()
        self.text_view.insert(END, "Just a text Widget\nin two lines\n")

    def set_text(self, text):
        self.text_view.delete(1.0, END)
        self.text_view.insert(END, text)
        self.text_view.pack()
