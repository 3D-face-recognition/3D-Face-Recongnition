class FeaturesSelection(object):
    def __init__(self, selector):
        self.selector = selector
        
    def fit(self):
        return self.selector.select_features()

    def change_strategy(self, strategey):
        self.selector = strategey