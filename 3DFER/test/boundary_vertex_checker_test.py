import unittest
import trimesh
from src.vertex_params_finder import VertexParamsFinder
from src.boundary_vertex_checker import BoundaryVertexChecker

class BoundaryVertexCheckerTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.mesh = trimesh.Trimesh([[-0.5, -0.5, -0.5],
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
        #         vertices_params = VerticesParams(self.mesh)
        vertex_params_finder = VertexParamsFinder(self.mesh)
        self.boundary_vertex_checker = BoundaryVertexChecker(vertex_params_finder)

    def test_if_vertex_not_boundary_vertex_then_should_be_false(self):
        self.assertFalse(self.boundary_vertex_checker.is_boundary_vertex(0))
        self.assertFalse(self.boundary_vertex_checker.is_boundary_vertex(2))
        self.assertFalse(self.boundary_vertex_checker.is_boundary_vertex(4))
        self.assertFalse(self.boundary_vertex_checker.is_boundary_vertex(5))
        self.assertFalse(self.boundary_vertex_checker.is_boundary_vertex(6))

    def test_if_vertex_is_boundary_vertex_then_should_be_true(self):
        self.assertTrue(self.boundary_vertex_checker.is_boundary_vertex(1))
        self.assertTrue(self.boundary_vertex_checker.is_boundary_vertex(3))
        self.assertTrue(self.boundary_vertex_checker.is_boundary_vertex(7))


if __name__ == '__main__':
    unittest.main()