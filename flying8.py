import math as m
from tkinter import *


def motion(event):
    tempX = int(event.x);
    tempY = int(event.y)
    ballX = can.coords(ball)[2] - 20;
    ballY = can.coords(ball)[3] - 20
    distance = m.sqrt((tempX - ballX) ** 2 + (tempY - ballY) ** 2)

    if distance > 2:
        can.move(ball, (tempX - ballX) / distance, (tempY - ballY) / distance)
        root.after(10, motion, event)
    else:
        return 0


root = Tk()
root.title("Движение")
w = root.winfo_screenwidth() # ширина экрана
h = root.winfo_screenheight() # высота экрана
w = w//2 # середина экрана
h = h//2
w = w - 200 # смещение от середины
h = h - 200
root.geometry('300x300+{}+{}'.format(w, h))

can = Canvas(width=300, height=300, bg="lightgreen")
can.pack()

ball = can.create_oval(0, 100, 40, 140, fill="green")
root.bind('<Button-1>', motion)

root.mainloop()
