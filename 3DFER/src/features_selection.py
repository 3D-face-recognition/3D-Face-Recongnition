class FeaturesSelection(object):
    def __init__(self, selector):
        self.selector = selector
        
    def fit(self):
        return self.selector.preprocess()

    def change_strategy(self, strategey):
        self.selector = strategey