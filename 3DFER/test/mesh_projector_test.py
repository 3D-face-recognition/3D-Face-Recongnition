import unittest
import trimesh
import logging
from math import cos, sin, pi
from src.features_selection_strategy.mesh_projector import \
    MeshProjector


class MeshProjectorTest(unittest.TestCase):
    def setUp(self):
        self.mesh = trimesh.Trimesh([[0, 0, 0],
                                     [5, 0, 0],
                                     [2.5, 2.5 * sin(pi / 3), 0],
                                     [-2.5, 2.5 * sin(pi / 3), 0],
                                     [-5, 0, 0],
                                     [-2.5, -2.5 * sin(pi / 3), 0],
                                     [2.5, -2.5 * sin(pi / 3), 0]],
                                    [[0, 1, 2],
                                     [0, 2, 3],
                                     [0, 3, 4],
                                     [0, 4, 5],
                                     [0, 5, 6],
                                     [0, 6, 1]])
        self.hog_pre = MeshProjector(self.mesh)

    def test_vertices_x_and_y_max_min(self):
        x_max = 5
        x_min = -5
        y_max = 2.5 * sin(pi / 3)
        y_min = -2.5 * sin(pi / 3)
        self.hog_pre._MeshProjector__get_sample_points()
        self.assertEqual(x_max, self.hog_pre.x_max)
        self.assertEqual(x_min, self.hog_pre.x_min)
        self.assertEqual(y_max, self.hog_pre.y_max)
        self.assertEqual(y_min, self.hog_pre.y_min)

    def test_is_a_point_in_triangle(self):
        point1 = [30, 30, 0]
        point2 = [2.5, 2.5 * sin(pi / 3) / 3, 0]
        triangle = [[0, 0, 0], [5, 0, 0], [2.5, 2.5 * sin(pi / 3), 0]]
        self.assertFalse((self.hog_pre._MeshProjector__is_point_in_triangle(triangle, point1)))
        self.assertTrue((self.hog_pre._MeshProjector__is_point_in_triangle(triangle, point2)))

    # with problem
    def test_project_sample_point_on_3d_plane(self):
        triangle = [[0, 0, 0], [1, 0, 0], [0.5, 0.5, 0]]
        project_point = MeshProjector.project_point_on_3d_plane([0.5, 0.1, 100], triangle)
        self.assertListEqual(list(project_point), [0.5, 0.1, 0])

    def test_depth_matrix(self):
        self.hog_pre.fit()
        print(self.hog_pre.sample_points)


if __name__ == '__main__':
    unittest.main()