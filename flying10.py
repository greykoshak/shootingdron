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


class PositionDrone:
    def __init__(self, obj_drone):
        self.my_drone = obj_drone
        self.points = list()  # Координаты движения дрона
        obj_drone.canvas.bind('<Button-1>', self.drawing_circle)

    def drawing_point(self):
        ind = len(self.points) - 1
        self.my_drone.canvas.create_oval(self.points[ind][0] - 2, self.points[ind][1] + 2,
                                         self.points[ind][0] + 2, self.points[ind][1] - 2, fill="black")

    def drawing_circle(self, event):
        self.points.append((int(event.x), int(event.y)))
        print("{:5.2f} {:5.2f}".format(int(event.x), int(event.x)))
        radius = self.my_drone.max_radius()

        self.my_drone.canvas.create_oval(self.points[0][0] - radius, self.points[0][1] + radius,
                                         self.points[0][0] + radius, self.points[0][1] - radius, fill="yellow", width=2)
        self.drawing_point()
        self.my_drone.canvas.bind('<Button-1>', self.drawing_ellipse)

    def drawing_ellipse(self, event):
        temp_x = int(event.x)
        temp_y = int(event.y)

        if self.is_belong_to_area(temp_x, temp_y):
            self.points.append((temp_x, temp_y))
            self.drawing_point()

            # Считаем энергию, которую затратил дрон для полета в эту точку и сделал фото
            ind = len(self.points) - 1
            coord = (self.points[ind][0], self.points[ind][1], self.points[ind - 1][0], self.points[ind - 1][1])
            delta = self.my_drone.distance(coord)
            delta_energy = delta * self.my_drone.delta_e_flying + self.my_drone.delta_e_shooting
            print("dist {:9.2f} energy {:9.2f}".format(delta, delta_energy))

            self.my_drone.set_full_charge(delta_energy)
            e1 = self.my_drone.get_full_charge()
            focus_a = (e1 - self.my_drone.delta_e_shooting) / (2 * self.my_drone.delta_e_flying) - delta / 2
            x = (e1 - self.my_drone.delta_e_shooting) / (2 * self.my_drone.delta_e_flying)
            focus_b = (x * x - delta * delta / 4) ** 0.5
            print("a: {:5.2f} b: {:5.2f} e1: {:5.2f}".format(2 * focus_a + delta, 2 * x, e1))

            self.my_drone.canvas.create_oval(self.points[0][0] - focus_b, self.points[0][1] + focus_a,
                            self.points[ind][0] + focus_b, self.points[ind][1] - focus_a, outline="blue", width=2)
        else:
            print("Not belong")

    def is_belong_to_area(self, temp_x, temp_y):
        if len(self.points) == 1:
            radius = self.my_drone.max_radius()
            return ((temp_x - self.points[0][0]) ** 2 + (temp_y - self.points[0][1]) ** 2) <= radius ** 2
        else:
            ind = len(self.points) - 1

            # Расстояние до фокуса а
            coord = (self.points[ind][0], self.points[ind][1], temp_x, temp_x)
            focus_a = self.my_drone.distance(coord)

            # Расстояние до фокуса b
            coord = (self.points[0][0], self.points[0][1], temp_x, temp_x)
            focus_b = self.my_drone.distance(coord)

            # Вычисленная точка на эллипсе
            e1 = self.my_drone.get_full_charge()
            border = (e1 - self.my_drone.delta_e_shooting) / (2 * self.my_drone.delta_e_flying)
            print("a: {:5.2f} b: {:5.2f} border: {:5.2f}".format(focus_a, focus_b, 2 * border))

            return focus_a + focus_b + self.my_drone.delta_e_shooting <= 2 * border


def main():
    root = Tk()
    # root.attributes("-fullscreen", True)
    root.title("Движение")

    can = Canvas(root, width=1400, height=820, bg="lightgreen")
    can.pack(fill='both', expand=True)

    my_drone = Drone(can)
    print("Радиус: {}, Энергии: {}".format(my_drone.max_radius(), my_drone.get_full_charge()))
    PositionDrone(my_drone)

    root.mainloop()


if __name__ == '__main__':
    main()
