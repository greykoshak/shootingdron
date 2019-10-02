from tkinter import *


class Drone:
    def __init__(self, canvas):
        self.canvas = canvas
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
        self.full_charge -= new_value
        print("Остаток энергии: {:5.2f}".format(self.get_full_charge()))
        return


class DefCoord:
    points = [(800, 400), (500, 300), (900, 500), (900, 300), (900, 400), (700, 100), (500, 500)]

    @classmethod
    def get_area(cls):
        return cls.points


class CalcRoot:
    def __init__(self, obj_drone, coord: list):
        self.my_drone = obj_drone
        self.coord = coord
        obj_drone.canvas.bind('<Button-1>', self.drawing_root)

    def drawing_point(self, x, y, color):
        self.my_drone.canvas.create_oval(x - 3, y + 3, x + 3, y - 3, fill=color)

    def view_points(self):
        for point in self.coord:
            self.drawing_point(point[0], point[1], "blue")

    def drawing_root(self, event):
        temp_x = int(event.x)
        temp_y = int(event.y)
        self.drawing_point(temp_x, temp_y, "red")
        self.my_drone.canvas.bind('<Button-1>', "")


def main():
    root = Tk()
    root.title("Area Shooting")

    can = Canvas(root, width=1400, height=820, bg="lightgreen")
    can.pack(fill='both', expand=True)

    my_drone = Drone(can)
    print("Радиус: {}, Энергии: {}".format(my_drone.max_radius(), my_drone.get_full_charge()))

    # Получить массив координат для съемки
    coord = DefCoord.get_area()
    obj = CalcRoot(my_drone, coord)
    obj.view_points()

    root.mainloop()


if __name__ == '__main__':
    main()
