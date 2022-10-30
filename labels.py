from tkinter import *
from clock import Time
from alarm import Alarm

LARGE_FONT = "Consolas 30"
MEDIUM_FONT = "Consolas 20"
SMALL_FONT = "Consolas 15"


class Labels:
    def __init__(self, window):
        self.window = window
        self.title = Label(self.window, text="Alarm Clock", font=LARGE_FONT + " bold italic underline",
                           bg="light blue", fg="navy")  # title label
        self.time = Time(self.window, LARGE_FONT)
        self.alarm_frame = LabelFrame(self.window, text="Alarms", font=SMALL_FONT + " bold italic underline",
                                      bg="orange", fg="navy", highlightbackground="navy", highlightthickness=2,
                                      highlightcolor="navy", bd=0, labelanchor=N)
        self.alarm = Alarm(self.window, self.alarm_frame, self.time)

    def draw(self):  # drawing all widgets
        self.title.pack()
        self.time.draw()
        self.alarm_frame.pack()
        self.alarm.draw()

    def update(self):
        self.time.update()
        self.alarm.update()
