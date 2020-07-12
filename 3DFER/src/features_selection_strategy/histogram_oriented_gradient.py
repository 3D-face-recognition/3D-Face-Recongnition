from abc import ABC

from src.features_selection_strategy.features_selection_strategy import FeaturesSelectionStrategy
from src.features_selection_strategy.mesh_projector import MeshProjector
from src.features_selection_strategy.pixel import Pixel
import numpy as np
from math import atan, pi


class HistogramOrientedGradient(FeaturesSelectionStrategy, ABC):
    def __init__(self, trimesh, cell_size=6, cell_dimension=9, block_size=3):
        self.preprocessor = MeshProjector(trimesh)
        self.cell_size = cell_size
        self.bin = cell_dimension
        self.block_size = block_size
        self.img = None
        self.cells = None
        self.blocks = None

    def select_features(self):
        self.img = self.preprocessor.fit()
        print("project img:\n", self.img)
        pixel_img = self.__transfer_value_to_pixel()
        self.cells = self.__statistic_histogram(pixel_img)
        self.blocks = self.__get_blocks_flatten(self.cells)

        return np.array(self.blocks).flatten()

    def __transfer_value_to_pixel(self):
        self.img = np.pad(self.img, [(1, 1), (1, 1)], mode="constant")
        pixel_img = []
        for row_idx in range(1, len(self.img)-1):
            row_pixel = []
            for col_idx in range(1, len(self.img[0])-1):
                gradient, alpha = self.__count_pixel_info(row_idx, col_idx)
                pixel = Pixel(self.img[row_idx][col_idx], gradient, alpha)
                row_pixel.append(pixel)
            pixel_img.append(row_pixel)
        return pixel_img

    def __count_pixel_info(self, x_index, y_index):
        # gradient
        gradient_y = self.img[x_index+1][y_index] - self.img[x_index-1][y_index]
        gradient_x = self.img[x_index][y_index+1] - self.img[x_index][y_index-1]
        gradient = pow(gradient_x ** 2 + gradient_y ** 2, 0.5)

        # alpha
        if gradient_x == 0:
            alpha = pi/2
        else:
            alpha = atan(gradient_y/gradient_x)
        return gradient, alpha

    def __statistic_histogram(self, pixel_img):
        cells = []
        for row_idx in range(0, len(pixel_img) - self.cell_size, self.cell_size):
            row_cells = []
            for col_idx in range(0, len(pixel_img[0]) - self.cell_size, self.cell_size):
                cell_pixel = self.__get_pixel_in__cell(pixel_img, row_idx, col_idx)
                histogram = self.__histogram_cell_gradient(cell_pixel)
                cells.append(histogram)
            if len(row_cells) != 0:
                cells.append(row_cells)

        return cells

    def __get_pixel_in__cell(self, pixel_img, row_idx, col_idx):
        if len(pixel_img) - row_idx > self.cell_size:
            row_range = self.cell_size
        else:
            row_range = len(pixel_img) - row_idx

        if len(pixel_img[0]) - col_idx > self.cell_size:
            col_range = self.cell_size
        else:
            col_range = len(pixel_img[0]) - col_idx

        cell_pixel = []
        for i in range(0, row_range):
            for j in range(0, col_range):
                cell_pixel.append(pixel_img[row_idx+i][col_idx+j])
        return cell_pixel

    def __histogram_cell_gradient(self, cell_pixel):
        hist = np.zeros( self.bin)
        for pixel in cell_pixel:
            bin_index = self.__angle_to_bin_index(pixel.alpha)
            hist[bin_index] += pixel.gradient
        return hist

    def __angle_to_bin_index(self, alpha):
        if alpha > pi:
            alpha = alpha - pi
        angles = [pi/self.bin * i for i in range(1, self.bin+1)]
        for idx, angle in enumerate(angles):
            if alpha <= angle:
                return idx

    def __get_blocks_flatten(self, cells):
        blocks = []
        for row_idx in range(len(cells) - self.block_size):
            for col_idx in range(len(cells) - self.block_size):
                blocks += list(self.__get_block_flatten(cells, row_idx, col_idx))
        return blocks

    def __get_block_flatten(self, cells, row_idx, col_idx):
        block_cells = []
        for i in range(self.block_size):
            for j in range(self.block_size):
                block_cells.append(cells[row_idx+i][col_idx+j])
        return np.array(block_cells).flatten()