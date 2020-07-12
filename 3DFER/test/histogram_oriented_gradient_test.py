import unittest
import trimesh
from math import sin, cos, pi, atan
from src.features_selection_strategy.histogram_oriented_gradient import HistogramOrientedGradient


class HistogramOrientedGradientTest(unittest.TestCase):
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
        self.hog = HistogramOrientedGradient(trimesh)

    def test_transfer_values_to_pixels(self):
        self.hog.img = [[1, 2, 3], [4, 5, 6], [6, 7, 8]]
        pixel_img = self.hog._HistogramOrientedGradient__transfer_value_to_pixel()
        self.assertEqual(1, pixel_img[0][0].value)
        self.assertAlmostEqual(pow(20, 0.5), pixel_img[0][0].gradient)
        self.assertAlmostEqual(atan(4/2), pixel_img[0][0].alpha)

    def test__get_pixel_in__cell(self):
        # cell_size==6
        self.hog.img = [[i for i in range(10)], [3+i for i in range(10)], [5+i for i in range(10)]]
        pixel_img = self.hog._HistogramOrientedGradient__transfer_value_to_pixel()
        cell_pixel = self.hog._HistogramOrientedGradient__get_pixel_in__cell(pixel_img, 0, 0)
        self.assertEqual(0, cell_pixel[0].value)
        self.assertEqual(3, cell_pixel[6].value)
        self.assertEqual(5, cell_pixel[12].value)

    def test_angle_to_bin_index(self):
        alpha = 0
        self.assertEqual(0, self.hog._HistogramOrientedGradient__angle_to_bin_index(alpha))
        alpha = pi / 2
        self.assertEqual(4, self.hog._HistogramOrientedGradient__angle_to_bin_index(alpha))
        alpha = pi
        self.assertEqual(8, self.hog._HistogramOrientedGradient__angle_to_bin_index(alpha))


    def test_get_block_flatten(self):
        self.hog.img = [[j+j for i in range(20)] for j in range(20)]
        pixel_img = self.hog._HistogramOrientedGradient__transfer_value_to_pixel()
        cells = self.hog._HistogramOrientedGradient__statistic_histogram(pixel_img)
        print("Cells:", cells)
        block = self.hog._HistogramOrientedGradient__get_blocks_flatten(cells)
        print("Blocks:", block)
