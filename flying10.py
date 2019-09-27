from tkinter import *


class Drone:
    def __init__(self):
        self.full_charge = 600  # Полный заряд дрона
        self.delta_e_flying = 1  # Расход энергии на единицу пройденного расстояния
        self.delta_e_shooting = 4  # Расход энергии на рдин снимок

    # l - кортеж, координаты начальной точки (x1, y1) и конечной точки (x2, y2)
    # l = (x1, y1, x2, y2)
    # Возвращает расстояние между точками
    @staticmethod
    def distance(l: tuple) -> float:
        return (abs(l[2] - l[0]) ** 2 + abs(l[3] - l[1]) ** 2) ** 0.5

    # Максимальное расстояние полета (туда и обратно) + один снимок
    # Зависит от начальной энергии и расхода на единицу полета и снимок
    # Возвращает радиус круга
    def max_radius(self) -> float:
        max_distance = (self.full_charge - self.delta_e_shooting) / self.delta_e_flying
        return max_distance / 2

    def get_full_charge(self):
        return self.full_charge

    def set_full_charge(self, new_value):
        self.full_charge = new_value
        print("Остаток энергии: {}".format(self.get_full_charge()))
        return


class CanvasDrone:
    def __init__(self):
        w = root.winfo_screenwidth()  # ширина экрана
        h = root.winfo_screenheight()  # высота экрана
        w = w // 2  # середина экрана
        h = h // 2
        w = w - 300  # смещение от середины
        h = h - 350
        root.geometry('900x700+{}+{}'.format(w, h))


class PositionDrone:
    def __init__(self, obj_drone):
        self.my_drone = obj_drone
        self.radius = self.my_drone.max_radius()
        self.points = list()  # Координаты движения дрона
        root.bind('<Button-1>', self.drawing_circle)

    def drawing_point(self):
        ind = len(self.points) - 1
        can.create_oval(self.points[ind][0] - 2, self.points[ind][1] + 2,
                        self.points[ind][0] + 2, self.points[ind][1] - 2, fill="black")

    def drawing_circle(self, event):
        self.points.append((int(event.x), int(event.y)))
        self.drawing_point()
        can.create_oval(self.points[0][0] - self.radius, self.points[0][1] + self.radius,
                        self.points[0][0] + self.radius, self.points[0][1] - self.radius)
        root.bind('<Button-1>', self.drawing_ellipse)

    def drawing_ellipse(self, event):
        tempX = int(event.x)
        tempY = int(event.y)
        self.points.append((tempX, tempY))

        if self.is_belong_to_circle(tempX, tempY):
            print("Belong {} {}".format(tempX, tempY))
            print(self.points)

            self.drawing_point()
            # Считаем энергию, которую затратил дрон для полета в эту точку и сделал фото
            self.my_drone.set_full_charge(550)

        else:
            print("Not belong")

    def is_belong_to_circle(self, tempX, tempY):
        return ((tempX - self.points[0][0]) ** 2 + (tempY - self.points[0][1]) ** 2) \
               <= self.radius ** 2


root = Tk()
root.title("Движение")

can = Canvas(width=900, height=700, bg="lightgreen")
can.pack()

CanvasDrone()
my_drone = Drone()
print("Радиус: {}, Энергии: {}".format(my_drone.max_radius(), my_drone.get_full_charge()))

PositionDrone(my_drone)

root.mainloop()
