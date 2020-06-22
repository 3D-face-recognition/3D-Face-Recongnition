import numpy as np
import trimesh
import math
from src.filter.interface_processing_filter import IProcessingFilter
class ZCircleCroppingFilter(IProcessingFilter):
    def __init__(self, unit_of_work, r):
        self.unit_of_work = unit_of_work
        self.mesh = None
        self.nose_index = 0
        self.depth_sort_vertices = None
        self.r = r

    def get_mesh(self):
        return self.mesh

    def get_unit_of_work(self):
        return self.unit_of_work

    def get_nose_index(self):
        return self.nose_index

    def filtering(self):
        mesh = trimesh.Trimesh([self.unit_of_work.get_vertices_pos(), self.unit_of_work.get_faces()])
        self.__init_mesh_attributes(mesh)
        pre_sphere_vertex_num = 0
        for vertex in self.depth_sort_vertices:
            mesh = self.__get_sphere_mesh(self.mesh, vertex, self.r)
            cur_sphere_vertex_num = len(mesh.vertices)
            if cur_sphere_vertex_num - pre_sphere_vertex_num > 150:
                self.nose_index = self.__find_nose_index(mesh.vertices, vertex)
                self.mesh = mesh
                break
            pre_sphere_vertex_num = cur_sphere_vertex_num
        self.unit_of_work.refresh(mesh)

    def __init_mesh_attributes(self, mesh):
        self.mesh = mesh.copy()
        self.depth_sort_vertices = sorted(self.mesh.vertices, key=lambda vertice: vertice[2], reverse=True)

    def __get_sphere_mesh(self, origin_mesh, center_vertex, r):
        mesh = origin_mesh.copy()
        sphere_indexes = self.__get_sphere_indexes(mesh, center_vertex, r)
        mesh = self.__remove_faces(mesh, sphere_indexes)
        mesh = self.__remove_vertices(mesh)
        return mesh

    def __get_sphere_indexes(self, mesh, center_vertex, r):
        sphere_indexes = np.array([])
        for index, vertice in enumerate(mesh.vertices):
            if self.__euclidean_diatance(center_vertex, vertice, 3) < r:
                sphere_indexes = np.append(sphere_indexes, index)
        return sphere_indexes

    def __euclidean_diatance(self, l_vertex, r_vertex, dimensional):
        euclidean_distance = 0
        for d in range(dimensional):
            euclidean_distance += pow(l_vertex[d] - r_vertex[d], 2)
        euclidean_distance = math.sqrt(euclidean_distance)
        return euclidean_distance

    def __remove_faces(self, mesh, sphere_indexes):
        faces = np.empty((0, 3), int)
        for face in mesh.faces:
            if self.__is_face_composition_of_sphere_vertices(face, sphere_indexes):
                faces = np.append(faces, np.array([face]), axis=0)
        mesh.faces = faces
        return mesh

    def __is_face_composition_of_sphere_vertices(self, face, sphere_indexes):
        for vertex in face:
            if not (vertex in sphere_indexes):
                return False
        return True

    def __remove_vertices(self, mesh):
        mesh.remove_unreferenced_vertices()
        return mesh

    def __find_nose_index(self, vertices, vertex):
        for index in range(len(vertices)):
            if (np.array(vertices[index]) == np.array(vertex)).all():
                return index
        return -1