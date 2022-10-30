from datetime import datetime
from tkinter import *


class Time:
    def __init__(self, window, font):
        self.window = window
        self.font = font
        self.time = datetime.now().strftime("%H:%M:%S")
        self.time_label = Label(self.window, text=self.time, font=self.font, bg="orange", highlightcolor="navy",
                                highlightthickness=5, highlightbackground="navy")

    def update_time(self):
        self.time = datetime.now().strftime("%H:%M:%S")

    def draw(self):
        self.time_label.pack(pady=10)

    def update(self):
        self.update_time()
        self.time_label.config(text=self.time)
