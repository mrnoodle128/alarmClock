from tkinter import *
import csv
from tkinter import ttk
import simpleaudio as sa
from datetime import datetime, timedelta

minutes = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17',
           '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35',
           '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53',
           '54', '55', '56', '57', '58', '59']

hours = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17',
         '18', '19', '20', '21', '22', '23']

LARGE_FONT = "Consolas 30"
MEDIUM_FONT = "Consolas 20"
SMALL_FONT = "Consolas 15"

filename = "alarms.csv"
audio_file = "alarm_sound.wav"


class Alarm:
    def __init__(self, window, alarm_frame, time):
        self.window = window
        self.time = time
        self.alarm_frame = alarm_frame
        self.hours = StringVar(value="12")
        self.minutes = StringVar(value="30")
        self.alarms = []
        self.checkboxes = []
        self.delete_buttons = []
        self.stop_buttons = []
        self.snooze_buttons = []
        self.sound = sa.WaveObject.from_wave_file(audio_file)
        self.playing_sound = None

        self.input_frame = LabelFrame(self.window, bg="orange", labelanchor=N, bd=0, text="Choose Time:",
                                      font=SMALL_FONT, highlightcolor="navy", highlightthickness=2,
                                      highlightbackground="navy")
        self.hours_box = ttk.Combobox(self.input_frame, textvariable=self.hours, state="readonly", values=hours,
                                      width=5)
        self.minutes_box = ttk.Combobox(self.input_frame, textvariable=self.minutes, state="readonly", values=minutes,
                                        width=5)
        self.no_alarms = Label(self.alarm_frame, text="No Alarms Yet :(", font=MEDIUM_FONT, bg="orange")
        self.placeholder = Label(self.alarm_frame, text="-------------", font=MEDIUM_FONT, bg="orange")
        self.confirm_button = Button(self.window, text="New Alarm", command=self.create_alarm,
                                     state=DISABLED if len(self.alarms) >= 5 else ACTIVE)

        self.alarm_data = self.load_alarms()

    def create_alarm(self):
        stop_button = Button(self.alarm_frame, text="Stop", command=lambda m=len(self.alarms): self.stop_alarm(m),
                             bg="light blue")
        snooze_button = Button(self.alarm_frame, text="Snooze", bg="light blue",
                               command=lambda m=len(self.alarms): self.snooze_alarm(m))
        delete_button = Button(self.alarm_frame, text="Delete", bg="light blue",
                               command=lambda m=len(self.alarms): self.delete_alarm(m))
        alarm = [Label(self.alarm_frame, text=f"{self.hours.get()}:{self.minutes.get()}", font=MEDIUM_FONT,
                       bg="orange"), IntVar(value=1), False]
        checkbox = Checkbutton(self.alarm_frame, onvalue=1, offvalue=0, text="Enabled", variable=alarm[1],
                               command=self.update_checkboxes, bg="orange", font=SMALL_FONT)
        self.alarms.append(alarm)
        self.checkboxes.append(checkbox)
        self.delete_buttons.append(delete_button)
        self.stop_buttons.append(stop_button)
        self.snooze_buttons.append(snooze_button)
        if len(self.alarms) >= 5:
            self.confirm_button.config(state="disabled")

        self.draw_alarms()

        self.alarm_data.append([self.hours.get(), self.minutes.get(), 1])
        self.save_alarms()

    def delete_alarm(self, index):
        self.alarms[index][0].destroy()
        self.checkboxes[index].destroy()
        self.delete_buttons[index].destroy()
        self.alarms.pop(index)
        self.checkboxes.pop(index)
        self.delete_buttons.pop(index)
        self.alarm_data.pop(index)
        for i, _ in enumerate(self.delete_buttons):
            self.delete_buttons[i].config(command=lambda m=i: self.delete_alarm(m))
        if len(self.alarms) >= 5:
            self.confirm_button.config(state="disabled")
        else:
            self.confirm_button.config(state=ACTIVE)
        self.save_alarms()
        self.draw_alarms()

    def stop_alarm(self, index):
        self.playing_sound.stop()
        self.alarms[index][0].config(bg="SystemButtonFace")
        self.stop_buttons[index].grid_forget()
        enable_time = datetime.now() + timedelta(minutes=1)
        try:
            self.alarms[index][3] = enable_time
        except IndexError:
            self.alarms[index].insert(3, enable_time)

    def snooze_alarm(self, index):
        self.playing_sound.stop()
        self.alarms[index][0].config(bg="light blue")
        self.stop_buttons[index].grid_forget()
        self.snooze_buttons[index].grid_forget()
        enable_time = datetime.now() + timedelta(minutes=1)
        snooze_time = datetime.now() + timedelta(minutes=5)
        try:
            self.alarms[index][3] = enable_time
        except IndexError:
            self.alarms[index].insert(3, enable_time)

        try:
            self.alarms[index][4] = snooze_time
        except IndexError:
            self.alarms[index].insert(4, snooze_time)

    def update_checkboxes(self):
        for i, _ in enumerate(self.alarms):
            if self.alarms[i][1].get() != self.alarm_data[i][2]:
                self.alarm_data[i][2] = self.alarms[i][1].get()
        self.save_alarms()

    def save_alarms(self):
        with open(filename, "w", newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(self.alarm_data)

    def load_alarms(self):
        with open(filename, "r", newline="") as f:
            csvfile = csv.reader(f)
            alarm_data = list(csvfile)

        for i, _ in enumerate(alarm_data):
            snooze_button = Button(self.alarm_frame, text="Snooze", bg="light blue",
                                   command=lambda m=len(self.alarms): self.snooze_alarm(m))
            stop_button = Button(self.alarm_frame, text="Stop", bg="light blue",
                                 command=lambda m=len(self.alarms): self.stop_alarm(m))
            delete_button = Button(self.alarm_frame, text="Delete", bg="light blue",
                                   command=lambda m=len(self.alarms): self.delete_alarm(m))
            alarm = [Label(self.alarm_frame, text=f"{alarm_data[i][0]}:{alarm_data[i][1]}", font=MEDIUM_FONT,
                           bg="orange"),
                     IntVar(value=alarm_data[i][2]), False]
            checkbox = Checkbutton(self.alarm_frame, onvalue=1, offvalue=0, text="Enabled", variable=alarm[1],
                                   command=self.update_checkboxes, bg="orange", font=SMALL_FONT)

            self.alarms.append(alarm)
            self.checkboxes.append(checkbox)
            self.delete_buttons.append(delete_button)
            self.stop_buttons.append(stop_button)
            self.snooze_buttons.append(snooze_button)

        self.draw_alarms()

        return alarm_data

    def draw_alarms(self):
        if not self.alarms:
            self.no_alarms.grid(column=0, row=0, padx=10)
        else:
            self.no_alarms.grid_forget()
        for i, _ in enumerate(self.alarms):
            self.alarms[i][0].grid(column=0, row=i, padx=10)
            self.checkboxes[i].grid(column=1, row=i, padx=10)
            self.delete_buttons[i].grid(column=2, row=i, padx=10)

    def draw(self):
        self.input_frame.pack(pady=10)
        self.hours_box.pack(side=LEFT, padx=10, pady=10)
        self.minutes_box.pack(side=RIGHT, padx=10, pady=10)
        self.confirm_button.pack()

    def update(self):
        self.time.update_time()
        for i, _ in enumerate(self.alarm_data):
            if f"{self.alarm_data[i][0]}:{self.alarm_data[i][1]}" == self.time.time[0:-3] and \
                    self.alarm_data[i][2] == 1 and not self.alarms[i][2]:
                self.playing_sound = self.sound.play()
                self.alarms[i][0].config(bg="red")
                self.alarms[i][2] = True
                self.stop_buttons[i].grid(column=3, row=i)
                self.snooze_buttons[i].grid(column=4, row=i)
            try:
                if datetime.now().strftime("%H:%M:%S") == self.alarms[i][3].strftime("%H:%M:%S"):
                    self.alarms[i][2] = False
                elif datetime.now().strftime("%H:%M:%S") == self.alarms[i][4].strftime("%H:%M:%S")\
                        and not self.alarms[i][2]:
                    self.playing_sound = self.sound.play()
                    self.alarms[i][0].config(bg="red")
                    self.alarms[i][2] = True
                    self.stop_buttons[i].grid(column=3, row=i, padx=10)
                    self.snooze_buttons[i].grid(column=4, row=i, padx=10)
            except IndexError:
                pass
