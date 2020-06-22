from src.data.interface_repository import IRepository
from src.data.vertex import Vertex

class VertexRepository(IRepository):
    def __init__(self, vertex_params_finder):
        self.vertices = self.__parsing_mesh(vertex_params_finder)

    def __parsing_mesh(self, vertex_params_finder):
        vertices = []
        for index in range(vertex_params_finder.length()):
            vertex_params = vertex_params_finder.get_vertex_params(index)
            new_vertex = Vertex(index, vertex_params)
            vertices.append(new_vertex)
        return vertices

    def create(self, item):
        self.vertices.append(item)

    def delete(self, item):
        item_index = item.get_index()
        del self.vertices[item_index]
        for index in range(item_index, len(self.vertices)):
            ori_index = self.vertices[index].get_index()
            self.vertices[index].set_index(ori_index)

    def update(self, item, params):
        item.params = params

    def get_by_index(self, index):
        return self.vertices[index]

    def get_all(self):
        return self.vertices