from src.features_selection_strategy.features_selection_strategy import FeaturesSelectionStrategy
from src.features_selection_strategy.mesh_projector import MeshProjector

class LocalBinaryPatterns(FeaturesSelectionStrategy):
    def __init__(self, trimesh):
        self.preprocessor = MeshProjector(trimesh)
        self.image = None
        self.local_binary_patterns = []

    def select_features(self):
        self.image = self.preprocessor.fit()
        if not self.__is_image_size_available():
            print('Image size incorrect')
            return
        row_num = len(self.image)
        col_num = len(self.image[0])
        for row_idx in range(1, row_num, 3):
            for col_idx in range(1, col_num, 3):
                self.local_binary_patterns.append(self.__calculate_lbp(row_idx, col_idx))
        print(self.local_binary_patterns)
        return self.local_binary_patterns

    def __is_image_size_available(self):
        print('col len =', len(self.image))
        print('row len =', len(self.image[0]))
        if len(self.image) % 2 != 1:
            return False
        col_num = len(self.image[0])
        for row in self.image:
            if len(row) % 2 != 1:
                return False
            if len(row) != col_num:
                return False
        return True

    def __calculate_lbp(self, row_idx, col_idx):
        base_z = self.image[row_idx][col_idx]
        lbp = []
        for lbp_col_idx in range(col_idx - 1, col_idx + 2):
            lbp.append(self.__calculate_pattern(self.image[row_idx - 1][lbp_col_idx], base_z))
        lbp.append(self.__calculate_pattern(self.image[row_idx][col_idx + 1], base_z))
        for lbp_col_idx in range(col_idx + 1, col_idx - 2, -1):
            lbp.append(self.__calculate_pattern(self.image[row_idx + 1][lbp_col_idx], base_z))
        lbp.append(self.__calculate_pattern(self.image[row_idx][col_idx - 1], base_z))
        s_lbp = [str(pattern) for pattern in lbp]
        a_lbp = "".join(s_lbp)
        return int(a_lbp, 2)

    def __calculate_pattern(self, target_z, base_z):
        if target_z > base_z:
            return 1
        else:
            return 0