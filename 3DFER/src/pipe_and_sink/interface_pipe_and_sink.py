import abc

class IPipeAndSink(abc.ABC):
    @abc.abstractmethod
    def set_next(self, pipe_and_sink):
        return NotImplemented

    @abc.abstractmethod
    def put(self, unit_of_work):
        return NotImplemented