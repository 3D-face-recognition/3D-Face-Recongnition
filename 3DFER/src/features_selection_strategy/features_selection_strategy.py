import abc


class FeaturesSelectionStrategy(abc.ABC):
    @abc.abstractmethod
    def select_features(self):
        pass
