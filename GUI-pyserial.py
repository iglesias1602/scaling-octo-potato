import tkinter as tk
import tkinter.font as tkFont
import serial
import time


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

        self.ser = serial.Serial('COM3', 9600, write_timeout=1, timeout=1)


        self.GMessage_414 = tk.Label(self)
        ft = tkFont.Font(family='Times', size=10)
        self.GMessage_414["font"] = ft
        self.GMessage_414["fg"] = "#333333"
        self.GMessage_414["anchor"] = "w"
        self.GMessage_414["text"] = ""
        self.GMessage_414.place(x=20, y=100, width=200, height=50)

        self.GLabel_limit = tk.Label(self)
        ft = tkFont.Font(family='Times', size=10)
        self.GLabel_limit["font"] = ft
        self.GLabel_limit["fg"] = "#333333"
        self.GLabel_limit["anchor"] = "w"
        self.GLabel_limit["text"] = "Current limit: N/A"
        self.GLabel_limit.place(x=20, y=150, width=200, height=25)

        self.userInput = tk.Entry(self)
        self.userInput["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=10)
        self.userInput["font"] = ft
        self.userInput["fg"] = "#333333"
        self.userInput["justify"] = "center"
        self.userInput["text"] = "Entry"
        self.userInput.insert(0, "999")  # Set default value
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

    def change_color(self, distance: int, limit: int):
        if distance >= limit + 1:
            self.image_1.delete("all")
            self.create_circle(20, 20, 15, self.image_1, "beige")

            self.image_2.delete("all")
            self.create_circle(20, 20, 15, self.image_2, "red")
        else:
            self.image_1.delete("all")
            self.create_circle(20, 20, 15, self.image_1, "green")

            self.image_2.delete("all")
            self.create_circle(20, 20, 15, self.image_2, "beige")

    def read_from_serial(self):
        # Check if there is data waiting to be read
        if self.ser.in_waiting > 0:
            # Read data from serial port
            distance_str = self.ser.readline().decode().strip()
            limit = getattr(self, 'limit', 0)

            # Insert data into label
            try:
                distance = int(distance_str)
                print(distance_str)
                self.GMessage_414["text"] = f"The object is at {distance} cm"
                self.change_color(int(distance), int(limit))
            except ValueError:
                #print("value error: ", str(limit))
                print(distance_str)
                distance = 0
                self.GMessage_414["text"] = f"The object is at {distance} cm"
                self.change_color(int(distance), 0)

            if distance_str == "Limit updated":
                print("Limit updated successfully")

        # Schedule this function to be run again after 100ms
        self.after(50, self.read_from_serial)

    def getInputBoxValue(self):
        return self.userInput.get().strip()

    def send_limit(self, limit):
        limit_str = str(limit)
        #self.ser.write(str(limit_str).encode() + b'\n')
        command = f"{limit_str}\r\n"
        self.ser.write(command.encode())
        time.sleep(0.1)

    def GButton_897_command(self):
        limit = self.getInputBoxValue()
        if limit:
            try:
                self.limit = limit
                self.GLabel_limit["text"] = f"Current limit: {self.limit}"
                self.send_limit(limit)
            except ValueError:
                print("Invalid limit value")
                self.limit = 0

    @staticmethod
    def create_circle(x, y, r, canvas, colour):  # center coordinates, radius
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        return canvas.create_oval(x0, y0, x1, y1, fill=colour)


if __name__ == "__main__":
    app = App()
    app.read_from_serial()
    app.mainloop()
