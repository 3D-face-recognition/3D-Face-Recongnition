import abc

class IProcessingFilter(abc.ABC):
    @abc.abstractmethod
    def filtering(self):
        return NotImplemented

    @abc.abstractmethod
    def get_mesh(self):
        return NotImplemented

    @abc.abstractmethod
    def get_unit_of_work(self):
        return NotImplemented