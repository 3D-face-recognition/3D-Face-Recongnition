import abc

class FeatureSelectionStrategy(abc.ABC):
    @abc.abstractmethod
    def select_features(self):
        pass