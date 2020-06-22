import numpy as np

class HoleFinder():
    def __init__(self, unit_of_work):
        self.HOLE_FRONT = 0
        self.HOLE_BACK = 1
        self.NOT_IN_HOLE = -1

        self.unit_of_work = unit_of_work
        self.holes = self.__find_holes(unit_of_work.get_boundary_vertices())

    def get_holes(self):
        print(self.holes)
        return self.holes

    def __find_holes(self, boundary_vertices):
        holes = []
        for i in range(len(boundary_vertices)):
            self.__merge_hole(holes, [boundary_vertices[i]], self.NOT_IN_HOLE)
        return holes

    def __merge_hole(self, holes, hole, direction):
        head = self.__get_head(hole, direction)
        one_ring_vertices = self.unit_of_work.get_one_ring_vertices(head)
        link_hole, direction = self.__get_link_hole(one_ring_vertices, head, hole, holes)
        if direction == self.NOT_IN_HOLE and len(hole) != 1:
            return
        # test_hole = [head]
        # test_hole.extend(link_hole)
        # if not self.__is_hole_valid(test_hole, self.unit_of_work.get_one_ring_triangles(head)):
        #     holes.append([head])
        #     return
        self.__link_two_holes(hole, link_hole, holes, direction)
        if direction != self.NOT_IN_HOLE:
            self.__merge_hole(holes, link_hole, direction)

    def __get_head(self, hole, direction):
        if (direction == self.HOLE_FRONT) or (direction == self.NOT_IN_HOLE):
            return hole[0]
        else:
            return hole[-1]

    def __get_link_hole(self, one_ring_vertices, head, hole, holes):
        for hole_index, link_hole in enumerate(holes):
            direction = self.__get_hole_direction(one_ring_vertices, link_hole)
            if direction == self.NOT_IN_HOLE:
                continue
            if hole in holes:
                continue
            test_hole = [head]
            test_hole.extend(link_hole)
            if not self.__is_hole_valid(test_hole, self.unit_of_work.get_one_ring_triangles(head)):
                continue
            return holes[hole_index], direction
        return [], self.NOT_IN_HOLE

    def __get_hole_direction(self, one_ring_vertices, hole):
        if hole[0] in one_ring_vertices:
            return self.HOLE_FRONT
        elif hole[-1] in one_ring_vertices:
            return self.HOLE_BACK
        else:
            return self.NOT_IN_HOLE

    def __is_hole_valid(self, hole, one_ring_triangles):
        if not self.__is_line_use_over_twice(hole, one_ring_triangles):
            return False
        return True
        # hole_set = set(hole)
        # associate_triangle_count = 0
        # for one_ring_triangle in one_ring_triangles:
        #     if hole_set.issubset(one_ring_triangle):
        #         associate_triangle_count += 1
        #     one_ring_triangle_set = set(one_ring_triangle)
        #     if one_ring_triangle_set.issubset(hole_set):
        #         return False
        # return associate_triangle_count < 2

    def __is_line_use_over_twice(self, hole, one_ring_triangles):
        one_ring_vertices = [one_ring_vertex for one_ring_triangle in one_ring_triangles for one_ring_vertex in one_ring_triangle]
        lines = {}
        for vertex in hole[1:]:
            lines[vertex] = 1
        for one_ring_vertex in one_ring_vertices:
            if one_ring_vertex not in lines:
                continue
            lines[one_ring_vertex] += 1
            if lines[one_ring_vertex] > 2:
                return False
        return True

    def __link_two_holes(self, hole, link_hole, holes, direction):
        if direction == self.NOT_IN_HOLE:
            holes.append(hole)
        elif direction == self.HOLE_FRONT:
            for vertex in hole[::-1]:
                link_hole.insert(0, vertex)
        else:
            link_hole.extend(hole)