from src.data.interface_repository import IRepository
from src.boundary_vertex_checker import BoundaryVertexChecker

class BoundaryVertexRepository(IRepository):
    def __init__(self, vertex_params_finder):
        self.vertices = self.__parsing_mesh(vertex_params_finder)

    def __parsing_mesh(self, vertex_params_finder):
        vertices = []
        boundary_vertex_checker = BoundaryVertexChecker(vertex_params_finder)
        for index in range(vertex_params_finder.length()):
            if boundary_vertex_checker.is_boundary_vertex(index):
                vertices.append(index)
        return vertices

    def create(self, boundary_vertex_index):
        self.vertices.append(boundary_vertex_index)

    def delete(self, boundary_vertex_index):
        self.vertices.remove(boundary_vertex_index)

    def update(self, item, params):
        pass

    def get_by_index(self, index):
        return self.vertices[index]

    def get_all(self):
        return self.vertices