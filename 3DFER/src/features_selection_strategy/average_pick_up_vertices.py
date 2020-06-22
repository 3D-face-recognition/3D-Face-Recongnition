import numpy as np
from src.features_selection_strategy.features_selection_strategy import FeaturesSelectionStrategy


class AveragePickUpVertices(FeaturesSelectionStrategy):
    def __init__(self, mesh, quantity=40):
        self.mesh = mesh
        self.quantity = quantity
        self.vertices = None

    def select_features(self):
        selected_index = []
        iter_time = 0
        dtype = [('x', float), ('y', float), ('z', float)]
        vertices_seq = np.array([tuple(vertices) for vertices in self.mesh.vertices], dtype=dtype)
        vertices_seq = np.array([list(vertices) for vertices in np.sort(vertices_seq, order=['y', 'x', 'z'])])
        for index, point in enumerate(vertices_seq):
            if len(selected_index) >= self.quantity:
                break
            if self.__is_maintain_distance(point, vertices_seq[selected_index], 30):
                selected_index.append(index)

        # draw the points on mesh
        # print("length of selected: ", len(selected_index))
        self.__visual_selected_points(self.mesh, vertices_seq[selected_index])
        return vertices_seq[selected_index]

    # private
    def __count_distance(self, p1, p2):
        return np.power(np.sum(np.square(np.array(p1) - np.array(p2))), 0.5)

    def __is_maintain_distance(self, point, selected_points, distance):
        for selected_point in selected_points:
            if self.__count_distance(point, selected_point) < distance:
                return False
        return True

    def __visual_selected_points(self, mesh, selected_points, selected_color=[255, 0, 0, 0],
                                 not_selected_color=[0, 255, 0, 0]):
        for vertices in selected_points:
            index, j = np.where(mesh.vertices == vertices)
            mesh.visual.vertex_colors[index[0]] = selected_color