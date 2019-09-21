from tkinter import *

root = Tk()
root.title("Прямовал")


def add_window():
    def paint():
        xx1 = x1.get()
        xx2 = x2.get()
        yy1 = y1.get()
        yy2 = y2.get()
        if var.get() == 2:
            c.create_oval(xx1, yy1, xx2, yy2)
        elif var.get() == 1:
            c.create_rectangle(xx1, yy1, xx2, yy2)
        a.destroy()

    a = Toplevel()
    a.title("Фигура")
    a.resizable(False, False)
    Label(a, text="x1").grid(row=0, column=0)
    Label(a, text="y1").grid(row=0, column=2)
    Label(a, text="x2").grid(row=1, column=0)
    Label(a, text="y2").grid(row=1, column=2)
    x1 = Entry(a, width=5)
    x1.grid(row=0, column=1, sticky=W)
    y1 = Entry(a, width=5)
    y1.grid(row=0, column=3, sticky=W)
    x2 = Entry(a, width=5)
    x2.grid(row=1, column=1, sticky=W)
    y2 = Entry(a, width=5)
    y2.grid(row=1, column=3, sticky=W)
    var = IntVar()
    Radiobutton(a, text="Прямоугольник", variable=var, value=1).grid(row=2, columnspan=4)
    Radiobutton(a, text="Овал", variable=var, value=2).grid(row=3, columnspan=4, sticky=W)
    Button(a, text="Нарисовать", command=paint).grid(row=4, columnspan=4)
    a.geometry('+{}+{}'.format(w + width_root, h))  # размещение доп.окна справа от основного


c = Canvas(root, width=500, height=500, bg="white")
c.grid()
Button(text="Добавить фигуру", width=20, command=add_window).grid()
# размещение окна по центру
root.update_idletasks()
s = root.geometry()
s = s.split('+')
s = s[0].split('x')
width_root = int(s[0])
height_root = int(s[1])
w = root.winfo_screenwidth()
h = root.winfo_screenheight()
w = w // 2
h = h // 2
w = w - width_root // 2
h = h - height_root // 2
root.geometry('+{}+{}'.format(w, h))
root.mainloop()
