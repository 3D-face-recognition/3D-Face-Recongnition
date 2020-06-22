import unittest
import trimesh
from src.hole_finder import HoleFinder
from src.data.unit_of_work import UnitOfWork

class HoleFinderTest(unittest.TestCase):
    def test_if_1_triangle_hole_then_return_3_boundary_vertices(self):
        mesh = trimesh.Trimesh([[-0.5, -0.5, -0.5],
                                     [-0.5, -0.5, 0.5],
                                     [-0.5, 0.5, -0.5],
                                     [-0.5, 0.5, 0.5],
                                     [0.5, -0.5, -0.5],
                                     [0.5, -0.5, 0.5],
                                     [0.5, 0.5, -0.5],
                                     [0.5, 0.5, 0.5]],
                                    [[1, 3, 0],
                                     [4, 1, 0],
                                     [0, 3, 2],
                                     [2, 4, 0],
                                     [5, 1, 4],
                                     [5, 7, 1],
                                     [3, 7, 2],
                                     [6, 4, 2],
                                     [2, 7, 6],
                                     [6, 5, 4],
                                     [7, 5, 6]])
        unit_of_work = UnitOfWork(mesh)
        hole_finder = HoleFinder(unit_of_work)
        holes = hole_finder.get_holes()
        hole = holes[0]
        self.assertEqual(7, hole[0])
        self.assertEqual(3, hole[1])
        self.assertEqual(1, hole[2])

    def test_if_1_square_hole_then_return_4_boundary_vertices(self):
        mesh = trimesh.Trimesh([[-0.5, -0.5, -0.5],
                                [-0.5, -0.5, 0.5],
                                [-0.5, 0.5, -0.5],
                                [-0.5, 0.5, 0.5],
                                [0.5, -0.5, -0.5],
                                [0.5, -0.5, 0.5],
                                [0.5, 0.5, -0.5],
                                [0.5, 0.5, 0.5]],
                               [[1, 3, 0],
                                [4, 1, 0],
                                [0, 3, 2],
                                [2, 4, 0],
                                [5, 1, 4],
                                [3, 7, 2],
                                [6, 4, 2],
                                [2, 7, 6],
                                [6, 5, 4],
                                [7, 5, 6]])
        unit_of_work = UnitOfWork(mesh)
        hole_finder = HoleFinder(unit_of_work)
        holes = hole_finder.get_holes()
        hole = holes[0]
        self.assertEqual(7, hole[0])
        self.assertEqual(3, hole[1])
        self.assertEqual(1, hole[2])
        self.assertEqual(5, hole[3])

    def test_if_2_triangles_hole_then_return_2_holes(self):
        mesh = trimesh.Trimesh([[-0.5, -0.5, -0.5],
                                [-0.5, -0.5, 0.5],
                                [-0.5, 0.5, -0.5],
                                [-0.5, 0.5, 0.5],
                                [0.5, -0.5, -0.5],
                                [0.5, -0.5, 0.5],
                                [0.5, 0.5, -0.5],
                                [0.5, 0.5, 0.5]],
                               [[1, 3, 0],
                                [4, 1, 0],
                                [0, 3, 2],
                                [5, 1, 4],
                                [5, 7, 1],
                                [3, 7, 2],
                                [6, 4, 2],
                                [2, 7, 6],
                                [6, 5, 4],
                                [7, 5, 6]])
        unit_of_work = UnitOfWork(mesh)
        hole_finder = HoleFinder(unit_of_work)
        holes = hole_finder.get_holes()
        hole1 = holes[0]
        self.assertEqual(4, hole1[0])
        self.assertEqual(2, hole1[1])
        self.assertEqual(0, hole1[2])

        hole2 = holes[1]
        self.assertEqual(7, hole2[0])
        self.assertEqual(3, hole2[1])
        self.assertEqual(1, hole2[2])

    def test_if_2_square_hole_then_return_2_holes(self):
        mesh = trimesh.Trimesh([[-0.5, -0.5, -0.5],
                                [-0.5, -0.5, 0.5],
                                [-0.5, 0.5, -0.5],
                                [-0.5, 0.5, 0.5],
                                [0.5, -0.5, -0.5],
                                [0.5, -0.5, 0.5],
                                [0.5, 0.5, -0.5],
                                [0.5, 0.5, 0.5]],
                               [[1, 3, 0],
                                [4, 1, 0],
                                [0, 3, 2],
                                [5, 1, 4],
                                [3, 7, 2],
                                [2, 7, 6],
                                [6, 5, 4],
                                [7, 5, 6]])
        unit_of_work = UnitOfWork(mesh)
        hole_finder = HoleFinder(unit_of_work)
        holes = hole_finder.get_holes()
        hole1 = holes[0]
        self.assertEqual(6, hole1[0])
        self.assertEqual(2, hole1[1])
        self.assertEqual(0, hole1[2])
        self.assertEqual(4, hole1[3])

        hole2 = holes[1]
        self.assertEqual(7, hole2[0])
        self.assertEqual(3, hole2[1])
        self.assertEqual(1, hole2[2])
        self.assertEqual(5, hole2[3])

    def test_if_1_square_and_1_triangle_hole_then_return_2_different_holes(self):
        mesh = trimesh.Trimesh([[-0.5, -0.5, -0.5],
                                [-0.5, -0.5, 0.5],
                                [-0.5, 0.5, -0.5],
                                [-0.5, 0.5, 0.5],
                                [0.5, -0.5, -0.5],
                                [0.5, -0.5, 0.5],
                                [0.5, 0.5, -0.5],
                                [0.5, 0.5, 0.5]],
                               [[1, 3, 0],
                                [4, 1, 0],
                                [0, 3, 2],
                                [5, 1, 4],
                                [3, 7, 2],
                                [6, 4, 2],
                                [2, 7, 6],
                                [6, 5, 4],
                                [7, 5, 6]])
        unit_of_work = UnitOfWork(mesh)
        hole_finder = HoleFinder(unit_of_work)
        holes = hole_finder.get_holes()
        hole1 = holes[0]
        self.assertEqual(4, hole1[0])
        self.assertEqual(2, hole1[1])
        self.assertEqual(0, hole1[2])

        hole2 = holes[1]
        self.assertEqual(7, hole2[0])
        self.assertEqual(3, hole2[1])
        self.assertEqual(1, hole2[2])
        self.assertEqual(5, hole2[3])


if __name__ == '__main__':
    unittest.main()