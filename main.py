from tkinter import *  # tkinter import
from labels import Labels


class Window:  # main class object
    def __init__(self):
        self.root = Tk()  # window attribute
        self.root.geometry("600x500")  # setting resolution for window
        self.root.title("Alarm Clock")  # setting window title
        self.root.resizable(False, False)  # not resizable in width or height
        self.root.config(background="light blue")

        self.labels = Labels(self.root)
        self.draw()
        self.update()  # calling own update function
        self.root.iconbitmap("icon.ico")
        mainloop()

    def draw(self):
        self.labels.draw()

    def update(self):
        self.labels.update()
        self.root.after(100, self.update)


if __name__ == "__main__":
    Window()
