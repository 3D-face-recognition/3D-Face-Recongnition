class BoundaryVertexChecker():
    def __init__(self, vertex_params_finder):
        self.vertex_params_finder = vertex_params_finder

    def is_boundary_vertex(self, vertex_index):
        vertex_params = self.vertex_params_finder.get_vertex_params(vertex_index)
        return len(vertex_params.get_one_ring_vertices()) != len(vertex_params.get_one_ring_triangles())