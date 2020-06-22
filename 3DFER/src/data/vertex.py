class Vertex():
    def __init__(self, index, params):
        self.index = index
        self.params = params

    def get_index(self):
        return self.index

    def set_index(self, index):
        self.index = index

    def get_pos(self):
        return self.params.get_pos()

    def set_pos(self, pos):
        self.params.set_pos(pos)

    def get_one_ring_vertices(self):
        return self.params.get_one_ring_vertices()

    def set_one_ring_vertices(self, one_ring_vertices):
        self.params.set_one_ring_vertices(one_ring_vertices)

    def get_one_ring_triangles(self):
        return self.params.get_one_ring_triangles()

    def set_one_ring_triangles(self, one_ring_triangles):
        self.params.set_one_ring_triangles(one_ring_triangles)