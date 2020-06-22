import networkx as nx

from src.data.vertex_params import VertexParams


class VertexParamsFinder():
    def __init__(self, mesh):
        self.mesh = mesh
        self.vertices_params = self.__parsing_mesh(mesh)

    def get_vertex_params(self, index):
        return self.vertices_params[index]

    def __parsing_mesh(self, mesh):
        vertices_params = []
        all_one_ring_vertices = self.__get_all_one_ring_vertices(mesh)
        all_one_ring_triangles = self.__get_all_one_ring_triangles(mesh)
        for index in range(len(all_one_ring_vertices)):
            vertices_params.append(VertexParams(self.mesh.vertices[index],
                                                all_one_ring_vertices[index],
                                                all_one_ring_triangles[index]))
        return vertices_params

    def __get_all_one_ring_triangles(self, mesh):
        triangles = mesh.faces
        all_one_ring_triangles = [[] for i in range(len(mesh.vertices))]
        for triangle in triangles:
            for vertex in triangle:
                all_one_ring_triangles[vertex].append(list(triangle))
        return all_one_ring_triangles

    def __get_all_one_ring_vertices(self, mesh):
        graph = nx.from_edgelist(mesh.edges_unique)
        all_one_ring_vertices = [list(graph[i].keys()) for i in range(len(mesh.vertices))]
        return all_one_ring_vertices

    def length(self):
        return len(self.vertices_params)