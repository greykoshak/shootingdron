from tkinter import *


class CanvasDron:
    def __init__(self):
        w = root.winfo_screenwidth()  # ширина экрана
        h = root.winfo_screenheight()  # высота экрана
        w = w // 2  # середина экрана
        h = h // 2
        w = w - 200  # смещение от середины
        h = h - 200
        root.geometry('500x500+{}+{}'.format(w, h))


class PositionDron:
    def __init__(self, radius=10):
        self.radius = radius
        root.bind('<Button-1>', self.drawing_oval)
        self.tempX = 0
        self.tempY = 0

    def drawing_oval(self, event):
        self.tempX = int(event.x);
        self.tempY = int(event.y)
        can.create_oval(self.tempX - radius, self.tempY + radius, self.tempX + radius, self.tempY - radius,
                        fill="yellow")
        root.bind('<Button-1>', self.set_title)

    def set_title(self, event):
        root.title("Левая кнопка мыши")


root = Tk()
root.title("Движение")

can = Canvas(width=500, height=500, bg="lightgreen")
can.pack()

CanvasDron()
radius = 100
PositionDron(radius)

root.mainloop()
