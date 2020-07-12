class PlaneEquation():
    # ax + by + cz + d = 0
    def __init__(self, normal, point):
        self.a = 0
        self.b = 0
        self.c = 0
        self.d = 0
        self.__calculate_plane_equation(normal, point)

    def __calculate_plane_equation(self, normal, point):
        self.a = normal[0]
        self.b = normal[1]
        self.c = normal[2]
        self.d = -self.a * point[0] - self.b * point[1] - self.c * point[2]

    def get_z(self, x, y):
        z = (-self.a * x - self.b * y - self.d) / self.c
        return z

