from src.features_selection_strategy.features_selection_strategy import FeaturesSelectionStrategy


class OnlyPickNose(FeaturesSelectionStrategy):
    def __init__(self, mesh, nose_index=100):
        self.mesh = mesh
        self.nose_index = nose_index

    def select_features(self):
        return [self.mesh.vertices[self.nose_index]]
