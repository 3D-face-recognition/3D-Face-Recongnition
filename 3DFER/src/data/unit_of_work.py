import numpy as np
from src.vertex_params_finder import VertexParamsFinder
from src.data.vertex_repository import VertexRepository
from src.data.boundary_vertex_repository import BoundaryVertexRepository


class UnitOfWork():
    def __init__(self, mesh):
        vertex_params_finder = VertexParamsFinder(mesh)
        self.vertex_repository = VertexRepository(vertex_params_finder)
        self.boundary_vertex_repository = BoundaryVertexRepository(vertex_params_finder)

    def get_boundary_vertices(self):
        return self.boundary_vertex_repository.get_all()

    def get_one_ring_vertices(self, index):
        vertex = self.vertex_repository.get_by_index(index)
        one_ring_vertices = vertex.get_one_ring_vertices()
        return one_ring_vertices

    def get_one_ring_triangles(self, index):
        vertex = self.vertex_repository.get_by_index(index)
        one_ring_triangles = vertex.get_one_ring_triangles()
        return one_ring_triangles

    def get_vertices_pos(self):
        vertices = self.vertex_repository.get_all()
        return [vertex.get_pos() for vertex in vertices]

    # unsure
    def get_faces(self):
        vertices = self.vertex_repository.get_all()
        one_ring_triangles_3d = [vertex.get_one_ring_triangles() for vertex in vertices]
        one_ring_triangles_2d = []
        for one_ring_triangles in one_ring_triangles_3d:
            for one_ring_triangle in one_ring_triangles:
                if one_ring_triangle in one_ring_triangles_2d:
                    continue
                one_ring_triangles_2d.append(one_ring_triangle)
        return one_ring_triangles_2d

    def refresh(self, mesh):
        vertex_params_finder = VertexParamsFinder(mesh)
        self.vertex_repository = VertexRepository(vertex_params_finder)
        self.boundary_vertex_repository = BoundaryVertexRepository(vertex_params_finder)