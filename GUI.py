import tkinter as tk
import tkinter.font as tkFont

import PIL
from PIL import Image, ImageTk


class App(tk.Tk):
    def __init__(self):
        # setting title
        super().__init__()
        self.title("Proximity sensor")
        # setting window size
        width = 423
        height = 190
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(alignstr)
        self.resizable(width=False, height=False)

        self.GMessage_414 = tk.Label(self)
        ft = tkFont.Font(family='Times', size=10)
        self.GMessage_414["font"] = ft
        self.GMessage_414["fg"] = "#333333"
        self.GMessage_414["anchor"] = "w"
        self.GMessage_414["text"] = "The object is at Unknown cm:"
        self.GMessage_414.place(x=20, y=100, width=200, height=50)

        # self.GMessage_414 = tk.Message(self)
        # ft = tkFont.Font(family='Times', size=10)
        # self.GMessage_414["font"] = ft
        # self.GMessage_414["fg"] = "#333333"
        # self.GMessage_414["justify"] = "center"
        # self.GMessage_414["text"] = "None"
        # self.GMessage_414.place(x=120, y=100, width=50, height=50)

        self.userInput = tk.Entry(self)
        self.userInput["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=10)
        self.userInput["font"] = ft
        self.userInput["fg"] = "#333333"
        self.userInput["justify"] = "center"
        self.userInput["text"] = "Entry"
        self.userInput.place(x=20, y=60, width=215, height=30)

        self.GButton_897 = tk.Button(self)
        self.GButton_897["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times', size=10)
        self.GButton_897["font"] = ft
        self.GButton_897["fg"] = "#000000"
        self.GButton_897["justify"] = "center"
        self.GButton_897["text"] = "Send"
        self.GButton_897.place(x=240, y=60, width=66, height=30)
        self.GButton_897["command"] = self.GButton_897_command

        self.GLabel_466 = tk.Label(self)
        ft = tkFont.Font(family='Times', size=10)
        self.GLabel_466["font"] = ft
        self.GLabel_466["fg"] = "#333333"
        # GLabel_466["justify"] = "left"
        self.GLabel_466["text"] = "Introduce a value:"
        self.GLabel_466.place(x=20, y=20, width=175, height=30)

        self.image_1 = tk.Canvas(self)
        self.create_circle(20, 20, 15, self.image_1, "beige")
        self.image_1.place(x=330, y=20, width=40, height=40)

        self.image_2 = tk.Canvas(self)
        self.create_circle(20, 20, 15, self.image_2, "beige")
        self.image_2.place(x=330, y=70, width=40, height=40)

    def change_color(self, valueInput):
        if valueInput == '30':
            self.image_1 = tk.Canvas(self)
            self.create_circle(20, 20, 15, self.image_1, "green")
            self.image_1.place(x=330, y=20, width=40, height=40)

            self.image_2 = tk.Canvas(self)
            self.create_circle(20, 20, 15, self.image_2, "beige")
            self.image_2.place(x=330, y=70, width=40, height=40)
        else:
            self.image_1 = tk.Canvas(self)
            self.create_circle(20, 20, 15, self.image_1, "beige")
            self.image_1.place(x=330, y=20, width=40, height=40)

            self.image_2 = tk.Canvas(self)
            self.create_circle(20, 20, 15, self.image_2, "red")
            self.image_2.place(x=330, y=70, width=40, height=40)

    def getInputBoxValue(self):
        getInput = self.userInput.get()
        print(getInput)
        return getInput

    def GButton_897_command(self):
        nexStep = self.getInputBoxValue()
        return self.change_color(nexStep)

    @staticmethod
    def create_circle(x, y, r, canvas, colour):  # center coordinates, radius
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        return canvas.create_oval(x0, y0, x1, y1, fill=colour)


if __name__ == "__main__":
    app = App()
    app.mainloop()
