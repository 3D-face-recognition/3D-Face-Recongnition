import abc

class IRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, item):
        return NotImplemented

    @abc.abstractmethod
    def delete(self, item):
        return NotImplemented

    @abc.abstractmethod
    def update(self, item, params):
        return NotImplemented

    @abc.abstractmethod
    def get_by_index(self, index):
        return NotImplemented

    @abc.abstractmethod
    def get_all(self):
        return NotImplemented