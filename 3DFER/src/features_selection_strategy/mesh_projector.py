import numpy as np
import trimesh
from src.plane_equation import PlaneEquation

class MeshProjector(object):
    def __init__(self, mesh, sample_feq=1):
        self.mesh = mesh  # type of == trimesh
        self.sample_feq = 1
        self.sample_points = []
        self.triangles = self.mesh.triangles  #####

        self.z = [] # 2d matrix
        self.pixels_gradients = []

    def fit(self):
        self.sample_points = self.__get_sample_points()
        for row in self.sample_points:
            z_row = []
            for sample_point in row:
                depth = 0
                # find the triangle where the point is in
                for triangle in self.triangles:
                    if self.__is_point_in_triangle(triangle, sample_point):
                        # get depth
                        # print('sample point', sample_point)
                        # print('triangle', triangle)
                        depth = MeshProjector.project_point_on_3d_plane(sample_point, triangle)[2]
                        break
                # add values of depth in z_row
                z_row.append(depth)
            # add row in z
            self.z.append(z_row)
        print('z =', self.z)
        return self.z

    def __get_sample_points(self):
        x = np.array([vertices[0] for vertices in self.mesh.vertices])
        y = np.array([vertices[1] for vertices in self.mesh.vertices])

        self.x_max = x[np.argmax(x)]
        self.x_min = x[np.argmin(x)]
        self.y_max = y[np.argmax(y)]
        self.y_min = y[np.argmin(y)]

        if (self.x_max - self.x_min) % 14 != 0:
            self.x_max -= (self.x_max - self.x_min) % 14
        if (self.y_max - self.y_min) % 20 != 0:
            self.y_max -= (self.y_max - self.y_min) % 20

        x_sample_freq = (self.x_max - self.x_min) / 14
        y_sample_freq = (self.y_max - self.y_min) / 20

        sample_points = []
        y = self.y_min
        while (y <= (self.y_max + 0.0001)):
            x = self.x_min
            temp = []
            while (x <= (self.x_max + 0.0001)):
                temp.append([x, y, 0])
                x += x_sample_freq
            sample_points.append(temp)
            y += y_sample_freq
        return np.array(sample_points)

    def __is_point_in_triangle(self, triangle, point):
        # consider x,y
        new_triangle = triangle.copy()
        for i in range(3):
            new_triangle[i][2] = 0
        # print('new triangle', new_triangle)
        total_area = trimesh.triangles.area([new_triangle])[0]  ####
        # print('total area =', total_area)
        v1 = new_triangle[0]
        v2 = new_triangle[1]
        v3 = new_triangle[2]
        three_distinct_area = trimesh.triangles.area([[v1, v2, point], [v1, v3, point], [v2, v3, point]], sum=True)
        # print('sum area =', three_distinct_area)
        return (three_distinct_area > total_area - 0.1) and (three_distinct_area < total_area + 0.1)

    @staticmethod
    def project_point_on_3d_plane(sample_point, triangle):
        normals = trimesh.triangles.normals([triangle])
        plane_equ = PlaneEquation(normals[0][0], triangle[0])
        # print(plane_equ.get_z(sample_point[0], sample_point[1]))
        project_point = [sample_point[0], sample_point[1], plane_equ.get_z(sample_point[0], sample_point[1])]
        # print("normal:", normals[0][0], "plane origin", triangle[1], "project point", project_point)

        return project_point