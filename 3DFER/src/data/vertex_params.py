class VertexParams():
    def __init__(self, pos, one_ring_vertices, one_ring_triangles):
        self.pos = pos
        self.one_ring_vertices = one_ring_vertices
        self.one_ring_triangles = one_ring_triangles

    def get_pos(self):
        return self.pos

    def set_pos(self, pos):
        self.pos = pos

    def get_one_ring_vertices(self):
        return self.one_ring_vertices

    def set_one_ring_vertices(self, one_ring_vertices):
        self.one_ring_vertices = one_ring_vertices

    def get_one_ring_triangles(self):
        return self.one_ring_triangles

    def set_one_ring_triangles(self, one_ring_triangles):
        self.one_ring_triangles = one_ring_triangles